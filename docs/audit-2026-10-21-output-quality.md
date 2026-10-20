# 产出质量审计：缺陷与改进措施（2026-10-21）

**触发**：用户审阅 `limbus_out1` 导出后反馈"质量远远不及预期，大量 .cs 堆砌
难以分辨，内部逻辑解析差很多"。

**结论**：反馈属实。本文档记录**实证缺陷**（附真实样例）、根因判断、
以及按"投入产出比"排序的改进措施。本文只做审计与规划，**未改任何源码**。

审计脚本：`docs/probes/audit_quality.py`（40 文件确定性抽样）

---

## 1. 总体指标（先说数字，但数字不是重点）

40 文件 / 4,572 行抽样：

| 标记 | 计数 | 每百行 |
| --- | --- | --- |
| `objN` 使用 | 813 | **17.78** |
| `numN` 临时变量 | 310 | 6.78 |
| `(T*)` 指针转换 | 271 | 5.93 |
| `(byte*)` 转换 | 216 | 4.72 |
| `object objN` 声明 | 189 | 4.13 |
| `vectorN` 临时变量 | 42 | 0.92 |
| `sub_<va>` | 37 | 0.81 |
| `&取地址` | 37 | 0.81 |
| `realN` 临时变量 | 33 | 0.72 |
| `goto` | 32 | 0.70 |
| shared body 标记 | 29 | 0.63 |
| `IntPtr` | 12 | 0.26 |
| `unknown` | 5 | 0.11 |
| `/* nothing */` | **0** | 0.00 |

最差文件噪音密度 **58.6%**（`PassiveAbility_40001202.cs`，128 行里 75 个标记）。
最好文件 0%（`BATTLE_SKILLSLOT_TEXTALRAM_TYPE.cs`，9 行纯常量）。

**但真正的问题不是密度，是下面这几个具体缺陷。**

---

## 2. 缺陷 1：`obj1 |= 0` —— 类型未知被渲染成"或 0"（最严重）

真实样例（`CoinAbility_1041004_2.cs`，`OnSucceedAttack`）：

```csharp
unsafe
{
    if (data_189446c5f == 0)
    {
        object obj1;
        obj1 = obj1 | 0;      // ← 读一个未初始化的 object，然后 | 0
        obj1 |= 0;
    }
    if (!(action._model.HasAbility(298)))
    {
        ...
    }
```

`PassiveAbility_1051402.cs` 里同一形态出现 4 次：

```csharp
object obj3;
obj3 = obj3 | 0;
obj3 |= 0;
obj3 |= 0;
obj3 |= 0;
```

### 根因判断

这是 IL2CPP 的**类静态初始化守卫**：`if (data_XXX == 0) { ... }` 对应 C# 的
`static Foo() { }` 类初始化器首次执行。里面那些指令是 IL2CPP 生成的
字段零初始化 / type-info 装配，**源码里根本不存在**。

il2csharp 有两处相关机制但都没接上：

- `drop_empty_init_guards`（`dec/build.py` lift 后调用）—— 名字看正是为
  这个设计的，但只处理"空"的守卫；这里的守卫非空（有那几条 `|= 0`）
- `obj1 | 0`：`obj1` 是未定型（`kind='?'` + `_unk=True`），Lifter 对
  `or` 指令的类型提升失败，退化成了"对象或整数"

### 危害

这是**噪音放大器**：一个类初始化守卫污染整个方法体，读者第一眼看到
`obj1 = obj1 | 0` 会以为逻辑就是如此。而且它出现在 `if` 里，把后面的
真实逻辑全推到深层嵌套。

---

## 3. 缺陷 2：未定型变量 `object objN` 泛滥，且带坏下游

同一个文件里：

```csharp
object obj13 = ((byte*)this.getClass() + 0x780)[0];   // ← 读了个 object
int num5 = 1;
bool flag2 = this.GiveBuff(action, target, timing, isWinDuel, num5, 0);
```

`obj13` 赋值后**从未使用** —— 但它把整个方法拖进了 `unsafe` 块。

### 这里有两个独立问题

**(a) `((byte*)klass + 0x780)[0]` 是静态字段读取，但没解析出来。**

`this.getClass()` 返回 klass，`+0x780` 是静态字段区里的偏移。il2csharp 有
`KLASS_STATIC_FIELDS = 0xB8` 和 `sfblob` / `static_off_path` 机制
（`lifter/values.py:622-654`），但这里用了 `(byte*) + 绝对偏移` 的裸形式，
说明 `static_off_path` 没命中。

注意 0x780 远大于 `KLASS_STATIC_FIELDS=0xB8`，所以它要么是
"静态字段区 + 0x780"（即静态字段 #120 左右），要么是**别的字段**
（元数据大小 / vtable / 实例字段）。我前面标定 `KLASS_*` 时就没得出
决定性结论，这个 0x780 正是那个未决问题的直接后果。

**(b) 未使用的 `object` 把方法变成 `unsafe`。**

一个没人用的 `obj13` 导致整个方法必须包在 `unsafe {}` 里。死代码消除
（`_drop_dead_locals`）应该先跑掉它，但它的赋值含指针运算，被判为有副作用
或类型不定而保留。

---

## 4. 缺陷 3：闭包/委托缓存还原不完整，出现 `throw;` 悬空

`PassiveAbility_1051402.cs`：

```csharp
List_1<ConsumeBuffData> list11 = coin.GetConsumeData(true);
Predicate_1<ConsumeBuffData> predicate11 = PassiveAbility_1051402.__c.__9__23_0;
Predicate_1<ConsumeBuffData> predicate12 = predicate11;        // ← 无谓拷贝
if (predicate11 == null)
{
    PassiveAbility_1051402.__c obj13 = typeof(PassiveAbility_1051402.__c).__static_fields;
    PassiveAbility_1051402.__c obj14 = PassiveAbility_1051402.__c.__9;
    throw;                                                    // ← 悬空 throw
    object obj15 = sub_1840cac60/*shared body, 3 candidates*/(obj16, obj14, __c._OnBeforeStartCoin_b__23_0);
    PassiveAbility_1051402.__c.__9__23_0 = obj16;
}
ConsumeBuffData consumeBuffData1 = list11.Find(predicate12);
```

这段本该是 C# 的**委托缓存惯用法**：

```csharp
Predicate<ConsumeBuffData> predicate = __c.__9__23_0;
if (predicate == null)
{
    predicate = (__c.__9__23_0 = new Predicate<ConsumeBuffData>(__c._OnBeforeStartCoin_b__23_0));
}
```

### 三个具体缺陷

1. **`throw;` 是裸的** —— 这是 C++ 层抛出的"缓存未命中"异常路径
   （IL2CPP 的 `Delegate::Create` 失败分支），不是源码的 `throw;`。
   il2csharp 有 `rethrow_va` 机制识别真正的 C# `throw;`，这里没接上。
2. **`throw;` 之后的代码仍在** —— `sub_1840cac60(...)` 和
   `__9__23_0 = obj16` 是被 throw 挡死的代码。il2csharp 的
   `_prune_nonreturning` 应该处理，但 throw 的 noreturn 性没被证明。
3. **`obj16` 未声明就用** —— 说明 `sub_1840cac60` 的实参列表重建失败
   （返回值本该是委托，赋给 `obj16`）。

结果：读者看到一段**逻辑上不可能执行**的代码，且顺序错乱。

---

## 5. 缺陷 4：同一个属性被重复输出

```csharp
protected override bool _showOnLeftPassiveUI
{
    // RVA: 0x8CDA40 VA: 0x1808CDA40
    get { return false; }
}
```
在文件里出现了 **2 次**（相邻，RVA 完全相同）。

这是 getter 与属性体的重复发射。`PassiveAbility_1051402.cs` 627 行里
有这种重复。会让"这个方法改一处"的读者漏改另一处。

---

## 6. 缺陷 5：好的样例证明能力是有的（重要）

不是所有文件都差。`StageScript_9564Base.cs` 的 `CheckTrigger` 非常干净：

```csharp
public override void CheckTrigger(int triggerCode = 0)
{
    this._eventModel?.OnStageScriptTriggered(triggerCode);
    if (triggerCode == 956401)
    {
        this._triggered = true;
    }
    else
    {
        if (triggerCode == 956402)
        {
            this._endStageProgress = true;
            return;
        }
        if (triggerCode == 956400)
        {
            this._endGimmickSkill = true;
            return;
        }
    }
}
```

字段名、方法名、类型、`?.` 空条件、常量、控制流全部正确。
`else { if { } }` 没折叠成 `else if` 是小瑕疵（有 pass 但没触发）。

**这说明瓶颈不在整体能力，而在少数几类高频失败模式** ——
正是 §2/§3/§4 那三个。修它们的收益是全局的。

---

## 7. 改进措施（按投入产出比排序）

### P0-a：类初始化守卫的识别与清除

**预期收益**：最高。`if (data_XXX == 0)` 守卫 + `objN |= 0` 是全树分布的，
清掉后能同时消除大量 `object objN`、`unsafe` 块、和深层嵌套。

**做法**：
1. 识别 IL2CPP 类初始化守卫的结构：`if (data_<32hex> == 0)` 包围的块，
   块内是零初始化 / klass 装配
2. 该块的**净副作用**若为零（只写未使用的局部），整块删除
3. 若块内有真实副作用（如静态字段赋值），保留但把零初始化指令降为注释

**判定依据**：il2csharp 已有 `drop_empty_init_guards`，扩展它的判据即可。
**风险**：中。要证明"净副作用为零"才能删，拿不出证明就保留（decline-by-default）。

### P0-b：`KLASS_*` 偏移标定（Unity 6000.3）

**预期收益**：高。直接修掉 §3(a) 那类 `((byte*)klass + 0x780)[0]`。
0x780 这类偏移一旦能解析，就能变成具体静态字段名。

**做法**：用 §8 的方法重新标定。我前面试过静态位移扫描无法区分候选
（每个 16 对齐的 K 都拟合），需要换方法 —— 见 §8。

**风险**：低（只影响启发式，不影响元数据驱动部分）。

### P1-a：委托缓存惯用法 + noreturn 剪枝

**预期收益**：中高。`__c.__9__N_M` 委托缓存是 C# 编译器高频产物，
Limbus 有 4,012 个 `<>c__DisplayClass`。

**做法**：
1. 识别 `if (cache == null) { cache = new Delegate(target); }` 的
   结构特征，输出 `CACHE ?? (CACHE = new Delegate(target))`
   —— il2csharp **已有** `_delegate_cache_fold`（CLAUDE.md 提到），
   所以这是"修好它"而不是"新做"
2. `throw;` 的 noreturn 证明：`rethrow_va` 已识别真正的 C# rethrow，
   要把"IL2CPP 委托创建失败路径"也识别为 noreturn，让 `_prune_nonreturning`
   能剪掉后面的死代码

**风险**：中。`_delegate_cache_fold` 是既有 pass，改它要重跑金色快照。

### P1-b：`else { if }` → `else if` 折叠

**预期收益**：中。纯可读性，零风险（不改变语义）。
il2csharp 有 `_drop_dead_locals` 等 25 个 pass，`else if` 折叠应该已有
但没覆盖这个形态。**这是最便宜的一项，可作为第一个交付。**

### P2：重复 getter 去重

**预期收益**：低-中。发射层去重，不影响 lift。
**风险**：低。但要先确认 RVA 相同的两个属性是否真是同一成员
（可能是 partial class 跨文件，或有意的重载）。

### P2：`[Address]` / `[AnalysisError]` 属性化

**预期收益**：中（可诊断性）。这是 UREngine guide 给的最大启发。
**风险**：中（格式变更，影响金色快照与 parse gate，需单独评估）。

---

## 8. 关于 KLASS_* 标定：我之前的失败与换思路

我在本次会话早些时候尝试标定 `KLASS_VTABLE`，结论是**静态位移扫描无法区分
候选** —— 每个 16 对齐的 K 都同样拟合位移直方图（`docs/probes/` 里没有
归档这个失败的探针，因为它是负结果）。

换思路（未实施，记录备用）：

1. **找一个有静态字段的类型，用 metadata 的 `fieldOffsets` 推它的静态字段
   总数，再找它的 klass 指针**。klass 指针可以从 `.data` 里指向
   `Il2CppClass` 的、且其 `image`/`name` 字段能对应上 metadata 的项反查。
2. **用一个已知的 vtable 调用点反推**：找一个 `callvirt` 编译后的
   `call [reg+disp]`，其目标地址能通过 metadata 的 vtable 表反查到
   `(typedef, slot)`，则 `disp = K + slot*16`。**关键是先定位 klass 指针**，
   而不是先看 disp。
3. **最可靠**：从 IL2CPP 运行期已知结构反推 ——
   `Il2CppClass` 的 `static_fields` 指针指向 `.bss` 里一块数据，
   而 `initialized` 标志在它附近。可用 `bss_usage_map`（2,798 项，
   已由 il2csharp 自己扫出）作为已知锚点。

---

## 9. 本次审计的边界（诚实声明）

- **抽样 40 文件 / 4,572 行**，非全量。结论的方向可信，
  具体比例需全量统计（构建仍在跑，完成后可做）。
- §2/§3/§4 的根因判断基于**读代码 + 读输出**推断，
  未通过单方法复现验证（`tools/inspect_methods.py --mi <N>` 可验）。
  **在按 P0 动手前，应先复现。**
- 我**没有**验证 `drop_empty_init_guards` / `_delegate_cache_fold` 的
  现有实现细节，只是从命名和 CLAUDE.md 描述推断它们的存在与用途。
  实施前必须读源码。
- 审计期间构建继续在跑（`limbus_out1` 未锁），本审计只读。

---

## 10. 建议的执行顺序

1. **先复现**：用 `--mi` 单方法回路复现 §2/§3/§4 三个缺陷，确认根因
2. **P1-b**（`else if` 折叠）：最便宜，验证"改源码→测试→文档"流程通畅
3. **P0-b**（KLASS 标定）：独立、低风险，且是 P0-a 的前置知识
4. **P0-a**（类初始化守卫）：收益最大，但在 3 之后
5. **P1-a**（委托缓存 + noreturn）：收益中高，风险中
6. **P2**：按需

---

# 附录 A：修复记录（2026-10-21 起，与上文审计结论对应）

## A.1 P1-b `else { if }` → `else if` 已修（commit `c99e579`）

即 §6 的缺陷。新增 `_elseif_flatten_multi` 于 `il2cpp/dec/flow.py`，
在 `structure.py` 的 `_elseif_flatten` 之后、`_switch_synth` 之前调用。

复现（`StageScript_9564Base.CheckTrigger`，mi 19943）从 4 层嵌套
变成扁平 `else if` 链：

```csharp
if (triggerCode == 956401)      { this._triggered = true; }
else if (triggerCode == 956402) { this._endStageProgress = true; return; }
else if (triggerCode != 956400) { }
else                            { this._endGimmickSkill = true; return; }
```

portable 套件 1325 passed / 0 failed（基线不变）。

## A.2 P0-a 类初始化守卫已修 —— 但根因与审计时的判断不同

**审计时（§2）的根因判断是错的。** 真实根因不是"`drop_empty_init_guards`
的正则形状不匹配"，而是：**`_guards` peephole 从未在这个二进制上生效过**。

`Decompiler.lift_method` 走 `self._decode(m)` → `self._guards(kept)`
（`il2cpp/dec/build.py:535`），**不经过** `Lifter.lift` 里那份同名的
peephole（`state.py:1509`，死代码）。而 `_guards` 的第一个扫描窗口
白名单是 `LEA/MOV/CALL/MOVZX/XOR/PUSH/SUB`，MSVC 在每次
`il2cpp_codegen_initialize_runtime_metadata` 调用后插入的
`lock or dword ptr [rsp],0` 释放屏障**不在其中**，于是扫描在屏障处
break，`found` 永远为 False：

```
0x182bab279  cmp byte ptr [189446C5Fh],0     ← 守卫标志
0x182bab289  jne short 182BAB2B4             ← 已初始化则跳过
0x182bab28b  lea rcx,[1890CA148h]
0x182bab292  call 1807980C0                  ← rt_init_meta
0x182bab297  lock or dword ptr [rsp],0       ← 屏障：peephole 在这里 bail
0x182bab2a8  lock or dword ptr [rsp],0
0x182bab2ad  mov byte ptr [189446C5Fh],1     ← 置位
0x182bab2b4  ← 真正的函数体
```

**全量普查**（299,281 个有原生代码的方法，重放 `_guards` 自身逻辑）：

| 项 | 计数 |
| --- | --- |
| 守卫站点总数 | 361,773 |
| 修复前被接受 | **1,726（0.48%）** |
| 因 `lock or` 屏障 bail | **360,019（99.5%）** |
| 因其他原因 bail | 15 |
| `lock or` 指令总数 | 835,802 |
| 其中位于守卫窗口内 | 748,254 |

也就是说这不是边缘情况：整个 peephole 在这个二进制上等于没写。

### 修复方案与可靠性论证

在 `_guards` 的第一个（有界 24 条）扫描窗口内接受屏障，条件是：

1. `mnemonic == OR`、`op0_kind == MEMORY`、`memory_base == RSP`、
   **`imm_of(ins, 1) == 0`**。`or` 立即数 0 是逐位恒等，
   `*rsp |= 0` 把刚读到的值原样写回，不改变任何状态；
   非 0 立即数是源码真实写入的 store，**不接受**。
2. 目标是本函数自己的栈（`sub rsp,50h` 之后），不是托管字段、
   数组元素或堆对象，本体内任何后续 load 都观察不到它。
   其他基址寄存器的屏障**不接受**。
3. 只在该窗口**已经见过 `call rt_init_meta`** 之后接受 ——
   证明我们读的是初始化序列，不是无关的 `lock or`。
   标志必须在同一个有界扫描内置位（第二个扫描跑在后面，
   在那里置位永远来不及）。
4. 只把该扫描已接受的 IP 加入 `skip`；第二个（无界）扫描不动，
   免得吞掉与守卫无关的屏障。
5. `lock xadd`/`xchg`/`cmpxchg` 是不同助记符（真实原子操作），
   完全不受影响。

### 修复效果

`CoinAbility_1041004_2.OnSucceedAttack`（mi 18594）修复后：

```csharp
unsafe
{
    if (!(action._model.HasAbility(298)))   ← 直接从真逻辑开始
    {
        ...
```

`obj1`、`obj1 | 0`、`obj1 |= 0` 与 `unsafe` 修饰符一并消失
（屏障消失后不再产生指针运算）。

**作用域实测**（4,000 方法）：`cmp byte [rip],0` 候选 10,915 个，
接受 10,264 个（94%）；`cmp dword [rip],0`（GC 屏障守卫，见 A.3）
1,699 个，**接受 0 个**。portable 套件 1325 passed / 0 failed。

顺带清掉 `build.py:579-581` 一段 2026-09-14 的遗留怪码
（`if False else` 短路包着一个不存在的 `IReg.RCP` 引用），
行为中性，就在本次修改的同一个 `if` 上。

## A.3 新发现：`data_X != 0` 是 GC 写屏障，不是类初始化守卫（未修）

修掉 A.2 后仍有 684/3,000 个 body 持有 `if (data_X != 0) { while (...) { } }`。
反汇编证明这是**另一回事**：

```
0x180908a0d  cmp dword ptr [1894383ECh],0    ← GC 屏障启用标志（dword，非 byte）
0x180908a1c  je short 180908A5B              ← 未启用则跳过
0x180908a1e  lea r8,[rbx+10h]                ← 被写入对象的地址
0x180908a2c  shr rdx,12h                     ← 卡片索引
0x180908a40  mov rax,[r9+rdx*8+462E0h]
0x180908a4b  bts rcx,r8                      ← 置卡片表位
0x180908a4f  lock cmpxchg [r9+rdx*8+462E0h],rcx
0x180908a59  jne short 180908A40h           ← 重试循环 → 输出里的空 while
```

这是 .NET/IL2CPP 的 **cardmarking GC 写屏障**。输出里的空
`while (...) { }` 是 `lock cmpxchg` 重试循环被错误建模的产物。

**不能简单删除**：它确实在写卡片表，是真实效果。但它对 C# 输出
毫无意义 —— C# 有 GC，不需要手写卡片表。这是"原生代码里的 GC
机制泄漏到托管输出"这一类问题，与 A.2 的类初始化守卫不同，
需要单独设计与实现（已记录，未动手）。

## A.4 待办（承接 §10）

| 项 | 状态 |
| --- | --- |
| P1-b `else if` 折叠 | **已完成** `c99e579` |
| P0-a 类初始化守卫 | **已完成**（本文 A.2） |
| P0-b KLASS 标定 | 未开始（§8 三条路线） |
| P1-a 委托缓存 + noreturn | 未开始 |
| URE P0 `sub_` 失败原因注释 | 未开始 |
| A.3 GC 写屏障 | 新发现，未开始 |
