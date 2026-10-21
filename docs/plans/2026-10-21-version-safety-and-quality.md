# 计划：URE 学习迁移 + 产物质量优化（2026-10-21 起）

**目标**：继续完成一整轮「从 UREngine 学习并迁移」与「产物质量优化」，
在**不破坏 il2csharp 既有版本支持（v24–v38）**的前提下增加并完善 **v39** 支持。

**约束（用户 2026-10-21 明确）**：
> 需要同时在保留 il2csharp 原先那些支持版本的使用支持的情况下增加 v39 支持。
> 可以参考 `il2cpp`（源码）与 `Il2CppDumperNew/`（权威结构定义）。

这意味着每一项改动都要回答两个问题：

1. **它是否影响非 v39 版本的输出？** 若影响，必须证明是改进而非回归，
   或将其收敛为版本门控（`meta.v35` / `meta.version`）。
2. **它的依据是否来自结构证明，而不是猜测？** 见 CLAUDE.md 的
   decline-by-default 铁律。

---

## 1. 已完成（本轮，含提交）

| 项 | 提交 | 版本影响分析 |
| --- | --- | --- |
| P1-b `else { if } → else if` | `c99e579` | **版本无关**。纯结构改写：else 块整体是 ≥2 个顺序 lone-if 才折叠，仅移动花括号，不复制/删除/重排语句。任何版本语义相同。 |
| P0-a 类初始化守卫 `lock or [rsp],0` | `3be886b` | **结构无关版本**。屏障是 MSVC 生成的 x64 代码，v31/v38/v39 的 PE 里都有；门控是"本窗口已见过 `call rt_init_meta`"，而 `rt_init_meta` 本身是结构识别（非硬编码地址）。v31 若有同类屏障会被同样吞掉——这是改进。**但会移动 v31 golden 哈希**，见 §3。 |
| P1-a#1 EH helper noreturn 屏幕 64→512 | `1be6de0` | **版本无关，只会更严格**。判定改为 `{ret,int3/ud2,invalid}` 先到者决定，读窗放大到 512 条/8KiB。只会**多拒绝**冒充 helper 的普通函数。v31 真正的 helper 在 ≤8 条内判定，不受影响。**可能移动 v31 golden**，见 §3。 |
| P0-a f/u jcc 窗口 4→8、flag 窗口 24→64 | `8c86828` | **版本无关**。只放宽"看多远"，判据（白名单 + `saw_rt_call`）不变。会移动 v31 golden，见 §3。 |
| 全量基线普查 + 审计附录 A | `3a632b9` | 纯文档。 |

---

## 2. KLASS 偏移的版本标定（关键：结论是**不需要版本化**）

### 2.1 权威来源

`Il2CppDumperNew/Il2CppDumper/Outputs/HeaderConstants.cs` 按版本给出
`Il2CppClass` 的完整 C 结构：

- `HeaderV35Plus`（v35 及以上，含 v39）
- `HeaderV29`（v29–31 区间，il2csharp 当前 `KLASS_*` 的依据）
- `HeaderV27` / `HeaderV242` / `HeaderV241` / `HeaderV240` / `HeaderV22`

### 2.2 逐字段推导（x64，Il2CppType=16 字节，指针 8 字节）

`HeaderV29` 的 `Il2CppClass_1`：

```
image@0x00 gc_desc@0x08 name@0x10 namespaze@0x18
byval_arg@0x20(16) this_arg@0x30(16)
element_class@0x40  castClass@0x48 declaringType@0x50 parent@0x58
generic_class@0x60 typeMetadataHandle@0x68 interopData@0x70 klass@0x78
fields@0x80 events@0x88 properties@0x90 methods@0x98
nestedTypes@0xa0 implementedInterfaces@0xa8 interfaceOffsets@0xb0
=> _1 size = 0xB8   => static_fields@0xB8, rgctx_data@0xC0
```

`Il2CppClass_2`（起点 0xC8）推导得 `cctor_finished@0xE0`，
故 v31 代码里的 `KLASS_INITIALIZED=0xE4` 落在 `cctor_finished` 之后
的填充/`cctor_thread` 对齐区；`_2` 结束于 0x134，vtable 8 对齐起于 **0x138**。

**结果**：`element_class=0x40, static_fields=0xB8, vtable=0x138`。

### 2.3 `HeaderV35Plus` 与 `HeaderV29` 的差异

对比两段 C 结构，`Il2CppClass_1` 与 `Il2CppClass_2` 的字段**顺序、类型、
宽度完全一致**，仅两处表面差异：

1. `uint32_t cctor_finished;` → `uint32_t cctor_finished_or_no_cctor;`
   （同一位置，改名，偏移不变）
2. `VirtualInvokeData vtable[255];` → `vtable[32];`（数组声明上限，不影响首元素偏移）

因此 **v35+ 的 `element_class/static_fields/vtable` 与 v29–31 相同**。

### 2.4 v39 二进制上的独立实测（双重印证）

对 Limbus（v39，x64 PE）直接测量：

1. **`static_fields=0xB8`**：以 `cmp [reg+0xE4],imm`（已初始化的 guard）
   为锚，扫描其后"同 cell 重载后读 `[reg+K]`"的模式，K 直方图
   **0xB8 出现 3,225 次**（要求同 cell 重载仍 3,053 次），远超其它非零值。
2. **`vtable=0x138`**：所有 `call [reg+disp]` 的 `disp & 0xF` 直方图
   以 **0x8 绝对主导（135,916 次）**；`0x138 & 0xF = 8` 一致。

**结论：`KLASS_*` 常量在 v24–v39 全区间相同，无需版本化。**
（这也解答了审计 §8 悬而未决的 P0-b：不是"无法区分"，而是"根本不需要区分"——
之前只做了朴素的静态位移扫描，缺少运行时序列约束。）

---

## 3. 必须补的验证：v31 回归

四个提交里 P0-a#1、P1-a#1、P0-a f/u 都会**改变实际输出**（改进），
因此会移动 v31（Shift At Midnight）的 golden 哈希。当前 checkout 的
`testgame/` 为空，game 套件无法运行。

处理方式（按优先级）：

1. **优先**：找到本机可用的 v31 fixture（CLAUDE.md 记录在 `testgame/`，
   git-ignored）或 `temptools/Cpp2IL/TestFiles/Simple_2022_3_35`，
   跑 `python -m pytest -m game` 与 `tests/test_game_goldens.py`，
   逐一审阅移动的哈希，证明是本文档所述的改进（守卫消失 / 假 throw 消失），
   再按流程重钉。
2. **若 fixture 不可得**：为三类改动补**合成单元测试**
   （在 `tests/` 用 `struct.pack` 造最小 metadata/机器码 fixture），
   固定"v31 形状应当被正确处理"的期望，避免仅凭 v39 一个数据点下结论。
3. **落盘**：移动的哈希逐个记录到 `validation_reports/`，附前后对照。

---

## 4. 仍未做（按收益/风险排序）

| 项 | 状态 | 说明 |
| --- | --- | --- |
| P0-b KLASS 标定 | **已结案**（§2：无需版本化） | `(byte*)getClass()+0x780` 渲染问题见 §8 结论（不做） |
| A.3 GC 写屏障 | **已完成**（纯形状）`177d4ed` | 1,108/4k 纯形状删；非纯 683 保留 |
| P1-a#2 委托缓存恢复 | 部分 | #1 已让委托链可达；缓存恢复的 `?? (x = new)` 折叠待查 |
| URE §5.3.3 `--publicize`/`--raw-addr` 头部免责 | **已完成** `97e233b` | 零风险，默认树字节不变 |
| URE P1 状态机 Stage 1（识别+标注） | **已完成** `3c6ef10` | 1,863 识别，0 误报；只加类注释 |
| URE §5.3.1 `sub_` 失败原因注释 | 未开始（改 `--explain` opt-in） | 全量内联会膨胀，须可选 |
| 全量前后对比验证 | **进行中**（round 2） | 后台重建 `limbus_fixed1` + `compare_trees.py` |
| P2 重复 getter 去重 / `[Address]` 形式化 | 未开始 | |
| C# 复刻版 | 未决 | 范围问题用户未回答 |

## 5. Round 2 记录

**已完成（round 2）**：

- `3c6ef10` URE P1 状态机 Stage 1：给 `_Method_d__N` 类加
  `// state machine for Method` 注释。检测 = 名字正则 + 同 typedef 有
  MoveNext；实测 1,863 匹配、0 误报、306 漏认（可接受）。不改 body，
  golden 不动。不宣称 async/iterator（需 custom attribute 表，无廉价
  解码，错标即误识别）。

**进行中**：后台重建 `limbus_fixed1`（Assembly-CSharp 全量，应用本轮
全部修复），完成后用 `compare_trees.py` 对 `limbus_out1`（修复前）做
逐标记前后对比，产出真实证据（而非抽样外推）。

**Round 2 调查结论（记录以免重复）**：

- **P0-b `(byte*)this.getClass()+0x780`**：`r10=[rbx]`(klass) →
  `[r10+0x780]` 是 BSS 静态单元读取（由 `mov [BSS],rax` 填充）。
  `0x780` 超 vtable(0x138)，归属单一类型的最深基类静态字段，无廉价
  metadata 反查；仅 308 处，收益不抵风险。**不做**，除非接入
  `bss_usage_map` 的 klass 关联。
- **`(byte*)` 的 217k 主流**都是 `((byte*)objN + N)[0]`，`objN` 是类型
  未知的原生指针；CLAUDE.md 铁律要求保留 `object objN`（诚实标记），
  不能为好看改名。**不做**。
- **`unknown` 9,557 处**多为未定义池常量/未建模参数，是诚实标记，不强填。**不做**。
- **`sub_180010df0`（6,777 次）**已查明是 `List<T>` 索引器 getter
  （`[rcx+0x10]`=items, `[rcx+0x18]`=size, 双重边界检查）；
  **`sub_180002950`** 是同布局的 setter + 卡表屏障。可命名，但要
  emitter 特化渲染才有价值，留待后续。
- **jcc 窗口放宽复核**：`decompiler` 路径走 `_guards`（build.py），
  与 `Lifter.lift`（state.py, 死代码）无关；round 1 的修改点正确。

## 6. A.3 GC 写屏障：探查结论与实现（round 1）

### 6.1 真实身份（反汇编 + Boehm 源码双重确认）

典型内联块（mi 8 .ctor）：

`
cmp dword ptr [1894383ECh],0     ; Boehm GC 的增量/卡表启用开关（单一 BSS 单元）
mov [rax+20h],dil                ; ← 真正的托管赋值在这里，屏障之前
mov [rbx+10h],rax                ; ← 真正的引用字段写入也在这里
je  skip                          ; 未启用则跳过
lea r8,[rbx+10h]                  ; 被写入的引用地址
shr rdx,12h ; and edx,7FFFh       ; 卡片索引 = addr >> 12 & 0x7FFF
shr r8,0Ch  ; and r8d,3Fh         ; 卡内位
mov rax,[18946B420h+rdx*8]        ; 卡片表项
bts rcx,r8                        ; 置位
lock cmpxchg [18946B420h+rdx*8],rcx
jne retry                         ; 原子重试循环 → 被错误建模成空 while
`

>> 12 是 Boehm GC 的 PAGE_SHIFT：x86-64 上 HBLKSIZE=4096=2^12
（dwgc/include/private/gcconfig.h，CPP_WORDSZ=64），因此
ddr >> PAGE_SHIFT(12) 即卡片索引起点，& 0x3F（CPP_WORDSZ-1）是卡内位。
这是**布尔特 GC 的 cardmarking 写屏障**，纯运行时机制。

### 6.2 为什么可以安全省略

1. 屏障只写卡片表（GC 私有结构），**不改变任何托管可见状态**。
2. 真正的引用赋值在屏障**之前**已完成（反汇编证实）。
3. 形状与地址无关：4,000 方法抽样中 **1,108 个纯形状 guard 全部用同一单元
   data_1894383ec**；条件是 xpr >> 12 & 63 != 0，是 Boehm 卡表算法本身。
4. 只省略**纯形状**（guard 体内只有唯一一个空 while，while 条件含
   >> 12 & 63，无 else）；683 个混合形状（屏障后有别的语句）一律保留。

### 6.3 与版本安全

形状来自编译器插桩的 GC 屏障，v24–v39 的 Unity（同一 Boehm GC）
都一样；data_<hex> 是结构指纹（BSS 单元），不是硬编码地址。因此这是
**版本无关**的规则；对 v31 同理适用（会移动 golden，属改进）。

### 6.4 实现

在 il2cpp/dec/flow.py 增 _drop_gc_cardmark_barriers，
于 structure.py 的 _final_text/_structure 末尾调用（纯文本 stage，
与 drop_empty_init_guards 同级）。匹配：

`
if (data_<hex> != 0)            <- GUARD
{                               <- {
    while (<expr> >> 12 & 63 != 0)   <- WHILE（必须是唯一体语句）
    {                           <- {
    }                           <- }
}                               <- }
`

整块删除。非纯形状（体内还有其他语句）不动。

## 7. 下一个具体动作

(byte*)this.getClass() + 0x780)[0] 这类**静态字段读取**：
x780 远超 vtable 结束位置，说明它是 static_fields 块内某字段的偏移。
当前渲染成原始指针算术。应做成：static_fields 基 + metadata 的
ieldOffsets 反查 → TypeName.fieldName。这是能看到的最大单点可读性收益之一。