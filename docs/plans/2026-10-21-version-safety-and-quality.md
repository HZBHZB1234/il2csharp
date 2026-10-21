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
| P0-b KLASS 标定 | **已结案**（§2：无需版本化） | 但"`(byte*)this.getClass()+0x780` 静态字段读取"这个**渲染**问题仍在，见 §5 |
| A.3 GC 写屏障 | 未开始 | `data_X != 0` 的卡片标记屏障；38,764 个 `!=0` guard。需单独设计（不是删除，而是识别为屏障并渲染成托管无害形式或省略） |
| P1-a#2 委托缓存恢复 | 部分 | #1 已让委托链可达；缓存恢复的 `?? (x = new)` 折叠待查 |
| URE P0 `sub_` 失败原因注释 + `--publicize` 头部免责 | 未开始 | 见 `research-2026-10-21-urengine.md` §5 |
| P2 重复 getter 去重 / `[Address]` 形式化 | 未开始 | |
| 全 162 镜像构建（应用全部修复） | 未开始 | 现有 `limbus_out1` 是修复前基线 |
| C# 复刻版 | 未决 | 范围问题用户未回答 |

## 5. 下一个具体动作

`(byte*)this.getClass() + 0x780)[0]` 这类**静态字段读取**：
`0x780` 远超 vtable 结束位置，说明它是 `static_fields` 块内某字段的偏移。
当前渲染成原始指针算术。应做成：`static_fields` 基 + metadata 的
`fieldOffsets` 反查 → `TypeName.fieldName`。这是能看到的最大单点可读性收益之一。
