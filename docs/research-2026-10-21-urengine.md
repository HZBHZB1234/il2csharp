# UREngine 对标调研：il2csharp 能借鉴什么（2026-10-21）

## 0. 结论先行

**不要参考 UREngine 改 il2csharp 的架构。** 两者的核心设计是同一件事
（带类型的符号执行 + 语义变量 + 上下文快照 + 栈帧还原），il2csharp 的
版本更成熟、约束更严格。

值得抄的有**两项**，按价值排序：

1. **失败的可诊断性**（§5，新增，2026-10-21 补充）——
   UREngine 把"我在解析哪个调用时失败、失败在哪"直接写进方法上的
   `[AnalysisError(...)]`，且每个方法都带 `[Address]`。il2csharp 输出
   `sub_<va>` 时只有地址、没有原因，读者得自己回二进制里查。
   **这项比状态机更基础，且实现成本低得多。**
2. **async / 协程状态机还原**（§4）—— 实测出的功能短板，
   Limbus 上有 1,950 个状态机类型 / 2,169 个 `MoveNext` 方法受影响。

本文记录调研过程、哪些材料可信、哪些不可信，以及为什么选这两项。

> **修订记录**：v1（同日早些时候）的结论是"只有状态机值得抄"。
> 补读 `https://www.ur-engine.com/guide/` 后发现可诊断性是更基础的
> 差距，已修正。v1 对《技术详解》的低可信度判断被 guide 证实，未改。

---

## 1. 材料来源与可信度分级

| 来源 | 可信度 | 说明 |
| --- | --- | --- |
| https://www.ur-engine.com/faq/ | **高** | 技术判断准确，边界诚实 |
| https://www.ur-engine.com/support/ | **高** | 支持范围与未实现项写得明确 |
| https://www.ur-engine.com/changelog/ | **高** | v1.0.6–1.0.8（2026-10）逐版本修真实 bug |
| https://www.ur-engine.com/guide/ | **高** | **最有价值的一份**：失败样例、诊断设计、使用约束，见 §5 |
| 《UREngine：我的反编译引擎构建之路》 | 中 | 架构演进叙述可信（三次重构的取舍） |
| 《UnityReverseEngine：突破性…技术详解》 | **低** | 示例几乎全是手写示意图，见 §3 |

### 1.1 FAQ 原文要点（可信）

- "**不是**利用 AI 还原的。完全自研的现代反编译器，基于二进制事实恢复代码"
- 反对 AI 的理由与 il2csharp 的铁律一致："AI 很可能生成'看起来正确、实际语义错误'的代码；对整个工程来说，这类错误会带来巨大的排查成本"
- "输出结果是原始 Unity 工程源码吗？**不是。** 是根据原生程序恢复的 C# 表达"
- "为什么部分方法可能无法完整恢复？复杂控制流、加密或修改过的输入，以及尚未建模的原生形态，都可能使部分方法保留较低层表达**或被明确标记为不支持**"
- 性能口径：超大型项目 5–10 分钟全工程还原；小型游戏 1 分钟内
- 平台：**当前仅 Android APK ARM64-v8a**（后续 iOS IPA）

### 1.2 Changelog 里的真实 bug（可信，且与 il2csharp 已修问题高度重合）

| UREngine 版本 | 修复内容 | il2csharp 对应状态 |
| --- | --- | --- |
| v1.0.6 | `bool` 存储范围、`char` 类型映射 | 已有：Boolean-byte stores（Review 78） |
| v1.0.6 | ARM64 `UBFX`、共享原生块 | 已有：共享体 all-candidates 论证（batch 21 起） |
| v1.0.6 | 原生栈布局、结构体复制 | 已有：RSP-copy frame homes / `slot_var` 归一化 |
| v1.0.7 | 托管 `ref` 返回、`in`/`ref` 参数识别 | 部分：preserve byref from return signature |
| v1.0.7 | 数组索引、结构体零初始化 | 部分：`_array_allocation` / typed identity |
| v1.0.7 | 枚举与整数比较 | 已有：`op_Implicit` conversion family gate |
| v1.0.7 | **异步与协程状态机的共享路径分析** | **无。本文 §4 的主题** |
| v1.0.7 | 局部函数、闭包、委托 | 已有：4,012 个 `<>c__DisplayClass*` 可处理 |
| v1.0.8 | `UIntPtr`、数组写入、SIMD 数据拼接 | 部分：SIMD 仅 sqrt 家族已证 |
| v1.0.8 | 内联构造逻辑的对象初始化还原 | 已有：`_alloc` / constructor completion（Review 84） |

**读法**：这张表说明两个独立团队在解同一组问题，且 il2csharp 对其中大部分
已有对应实现。唯一空缺是状态机。

---

## 2. 架构对比：UREngine 的"微型 Runtime"就是 il2csharp 的 Lifter

作者自述核心是"融合静态类型推导与动态执行模拟的微型 Runtime"，列举四项能力：

| UREngine 表述 | il2csharp 对应实现 |
| --- | --- |
| 精准模拟内存布局（class/struct 真实结构） | `type_sizes` + `fieldOffsets` 推导字段偏移；`KLASS_*` 标定 |
| 支持带类型的语义变量（不再是简单寄存器） | `Expr`（`expr.py`）：`text` + `ty` + `kind` + `recv` |
| 实现上下文快照（指令地址间保存/恢复状态） | Lifter 寄存器文件 + pass 2 的 phi merge |
| 还原真实函数栈帧 | `_setup_entry` / `_stack_offset` / RSP-copy frame homes / RBP quarantine |
| 函数级按需分析（不全量加载二进制） | 方法论有（`Lifter` 单方法），但每次构建仍全量解析元数据 |

### 2.1 作者自述的三次重构（可信，且印证了 il2csharp 的路线）

1. **IL 中间码转换** → 放弃，理由："调试过程几乎是一个黑盒……每一层都伴随着语义信息的衰减"
2. **直接生成 C#** → 采用，理由："语义更透明""调试更直观"，代价是闭包/匿名类等需手写完整链接解析
3. **静态分析 + 动态模拟混合** → 当前架构

il2csharp 走的正是第 2/3 条路线：直接从机器码符号执行到 C#，没有中间 IR。
**这条路线被独立验证过，不需要改。**

---

## 3. 为什么那篇《技术详解》不可信

它给出的"还原结果"具备以下不可能特征：

- `public float moveSpeed = 5f;` —— 声称"从二进制中推断出默认值"。
  IL2CPP 中字段初始值由 `.cctor` 在运行时赋值，且会被优化/重排，
  **静态反编译无法恢复字面量 `5f`**。
- `GetComponent<Rigidbody>()` / `DontDestroyOnLoad(gameObject)` /
  `PlayerPrefs.GetInt("HighScore", 0)` 完整还原 —— 这些需要识别
  "作者写的是单例模式"这类**设计意图**，属于语义之外的信息。
- `Instance == null` 的单例结构、行为树三分支切换 —— 同属设计意图。
- "生成代码直接可编译运行" —— 与 UREngine 自己 FAQ 的
  "部分方法可能无法完整恢复"矛盾。
- "代码 DNA 指纹 / 司法鉴定级相似度" —— 营销内容，无技术细节。

**判断依据**：这些示例是"原始 C# 源码"而非"反编译产物"——它们太干净了，
干净到没有任何反编译工具能达到。作者用它们说明"理想输出形态"。

**这不影响 UREngine 是个严肃项目**：FAQ 和 changelog 都很扎实。只是
那篇博客的示例不能作为能力基准，也不能作为 il2csharp 的改进目标。

---

## 4. 唯一值得抄的：async / 协程状态机还原

### 4.1 实测数据（Limbus Company，metadata v39）

探针：`docs/probes/urengine_statemachine_metadata.py`
（已归档；原始位置 `%TEMP%\opencode\probe_statemachine2.py`）

```
metadata 类型名以 '<' 开头：8,882 个
  <>c__DisplayClassN_N            4,012   ← 闭包，il2csharp 已处理
  <>c                            2,444
  <Module>                         161
  <PrivateImplementationDetails>   103
  <MethodName>d__N               1,950   ← 状态机，il2csharp 未处理
方法名含 d__N 的类型：1,950
名为 MoveNext 的方法：2,169
名字含 __state / SetStateMachine：0（字段名被清洗，见下）
```

> 注：直接在产物树上搜 `d__NNN` 会得到 0 —— 因为 emitter 把标识符里的
> `<>` 清洗掉了（C# 输出名不允许）。必须查 metadata 才是真值。
> 两个探针都归档在 `docs/probes/`，其中
> `urengine_statemachine_tree.py` 就是这个"读到 0"的反面对照。

### 4.2 il2csharp 现状：零处理

`grep -E 'MoveNext|stateMachine|coroutine|await|yield|d__\d+' il2cpp/dec/*.py`
的 11 处命中**全部是关键字保护**（防止 `await`/`yield` 被当作变量名使用），
没有任何 pass 识别状态机结构：

- `dec/highlevel.py:1726` `_NOBJ_KW` 集合含 `'yield'`, `'await'`
- `dec/highlevel.py:1928` 关键字列表
- `dec/flow.py:968` 提到 `IEnumerator<PlayerRef>` 的 GetEnumerator/MoveNext/Current
  是**接口分发识别**，不是状态机还原
- `dec/flow.py:1528` "XmlDownloadManager's async MoveNext, VA" —— 当普通方法处理
- `dec/seh.py:407` "d__100.MoveNext: finally mid-switch" —— **SEH 正在为不认识
  状态机而付出的持续代价打补丁**

### 4.3 影响

这 1,950 个类型目前输出为：

```csharp
// 现在：读者完全看不出这是个 async 方法
private class <LoadSprite>d__1
{
    private int <>1__state;      // 状态字段
    private void MoveNext()
    {
        switch (this.<>1__state)   // 巨型 switch，case 0/1/2...
        {
            case 0: ... goto state_2;
            ...
        }
    }
}
```

期望：

```csharp
// 目标：还原为可读的异步方法
private async Task LoadSprite(string path)
{
    ...
    yield return request;
    ...
}
```

---

## 5. 最该抄的：失败的可诊断性（guide 的新发现）

`https://www.ur-engine.com/guide/` §3「判断反编译代码的恢复情况」
是全部材料里最有价值的一份。它公开了自己的失败长相：

```csharp
[AnalysisError("ConvertCallInstruction error, can not find method at 0x11D761C
  from SanAndreasUnity.Behaviours.NPCPedSpawner+<SpawnPedCoroutine>d__30::MoveNext
  at 0x11C0A48")]
[Address("0x11BEC84")]
private IEnumerator SpawnPedCoroutine(WorldSystem<PedAI>.Area worldSystemArea)
{
    return null;
}
```

以及优化期失败：

```csharp
[AnalysisErrorAttribute("decompiler optimize error")]
[global::UREngine.AddressAttribute("0x118B4DC")]
private void GetStats(global::UGameCore.Utilities.Stats.GetStatsContext context)
{
    // Compiler optimize diagnostics:
    // CS0019: 运算符“>=”无法应用于“int”和“方法组”类型的操作数
}
```

### 5.1 它做对的四件事，il2csharp 都缺

| # | UREngine 做法 | il2csharp 现状 | 差距 |
| --- | --- | --- | --- |
| 1 | 错误串含**完整定位链**：失败的调用地址 `0x11D761C` + **所在方法** `...d__30::MoveNext at 0x11C0A48` + 失败阶段 `ConvertCallInstruction` | `sub_18084e320` 只有地址；读者不知道这是调用失败还是本就没解析出来，更不知道它出现在哪个上下文 | **高** |
| 2 | 每个方法都带 `[Address("0x11BEC84")]` | 只有 `// RVA: 0x8765B0 VA: 0x1808765B0` 注释 | 低（形式差异） |
| 3 | **显式警告占位体**："方法体中的 `return null` 可能只是失败后的占位实现，不能据此推断原函数本来就返回空值" | `/* nothing */` 有这个语义，但无显式警告；`return null` 在某些路径上确实是 lift 产物 | **高** |
| 4 | 字段可见性受限时**逐点降级**为 `ReflectionFieldAccessor.GetFieldValue<int>(obj, "m_net_ammoInClip")`，并说明"这不代表反编译失败" | **已有对应机制，但是全局开关而非逐点降级**：`--publicize`（fix 127）把所有声明刷成 `public`，`--raw-addr`（fix 128）把 `(byte*)E` 收进 `__addr(E)` helper。见 §5.2a | 低（设计选择不同，非缺失） |

### 5.2a 反射访问那条：il2csharp 已有等价物，不是缺失

guide §3.4 的 `ReflectionFieldAccessor.GetFieldValue<int>(obj, "m_net_ammoInClip")`
看上去是 il2csharp 没有的能力，实际是**同一个问题的两种解法**。

根因（`il2cpp/emitter.py:250` 的注释说得很准确）：

> Native code reads private backing fields and internal members across
> images because IL2CPP inlines accessors and ignores accessibility, so a
> faithful body cannot compile against the faithful declarations (CS0122).

即 IL2CPP 把 C# 编成 C++ 时丢弃了访问修饰符，原生代码读私有字段和读
公共字段在机器码层面完全一样。于是"忠实的声明"和"忠实的函数体"
单独看都对，合起来编译不过。

| | UREngine | il2csharp |
| --- | --- | --- |
| 手段 | 逐点降级到 reflection helper | 全局开关：`--publicize` / `--raw-addr` |
| 声明层 | 保持 metadata 的私有性 | 全部刷成 `public`（背离 metadata） |
| 读者可见性 | 单个访问点被标记 | 整棵树的修饰符被改写，无任何提示 |

**不照抄逐点降级的理由**：il2csharp 那两个 flag 的定位是让 Roslyn 门
"只测 lift 错误、不测可访问性/裸指针噪音"（CLAUDE.md 原文：they exist
so the Roslyn gate measures lifting errors instead of
accessibility/raw-pointer noise）。在这个目的下，全局开关是在**隔离变量**，
比逐点降级更合适 —— 逐点降级反而会让门测到一堆降级路径自身的错误。

**真正该做的是补说明**：`--publicize` / `--raw-addr` 开启后，
产出里没有任何地方告诉读者"这些 `public` 和 `__addr` 是编造的"。
UREngine 那句"出现反射访问不代表反编译失败，也不表示原始源码用了反射"
防的正是这类误读。il2csharp 至少要有个文件头声明。

（§5.1 表中第 4 行据此从"缺失"改为"设计选择不同"。）

### 5.2b 为什么这项比状态机更该先做

- **成本**：状态机要新增 pass、要动控制流、要碰金色快照；
  可诊断性主要是**在既有 `sub_` 渲染处补上下文信息**，不改变任何 body 的语义。
- **收益面**：状态机只影响 1,950 个类型；
  而 `sub_` / `/* nothing */` / `unknown` 是**全树分布**的
  （CoinModel.cs 一个文件里就有 38 个 `sub_`、5 个 `unknown`）。
  每一个都是读者要回头查二进制的点。
- **风险**：几乎为零。不改 lift 结果，只改标记的信息量。
  符合 il2csharp 的 decline-by-default —— 甚至是在**加强**诚实性。

### 5.3 具体可做的三件事（按优先级）

1. **给 `sub_<va>` 补失败原因与上下文**。il2csharp 内部其实知道为什么
   （多个候选？无候选？泛型未闭合？ABI 未知？）—— 这些判定在
   `_call` / `_shared_*` 里都做过，只是没往外传。
   把" declined 的原因"渲染成注释：
   ```csharp
   // sub_18084e320: 3 metadata candidates, receiver chain cannot pick one
   ```
2. **给 `/* nothing */` / 空体补警告**，明确"这是未能恢复，不是原函数为空"。
3. **`--publicize` / `--raw-addr` 开启时加文件头声明**（§5.2a）：
   明确告知这些 `public` 和 `__addr(E)` 是反编译器的降级产物、
   不是原始源码的修饰符。成本近零，防的是一整类误读。

### 5.3a 暂不做：逐点 reflection 降级

理由见 §5.2a —— il2csharp 的两个 compile-gate flag 定位是隔离噪音，
全局开关在该目的下更优；逐点降级会让门测到降级路径自身的错误，
且要改表达式生成、影响金色快照，边际收益不抵风险。

### 5.4 它同样失败，这反过来印证了 il2csharp 的门是合理的

guide 里 UREngine 的失败形态与 il2csharp 高度同构：

- `can not find method at 0x...` ≈ il2csharp 的 `sub_<va>`
- `decompiler optimize error` + `CS0019` ≈ il2csharp 的 Roslyn 门 454,955 错误
- `return null` 占位 ≈ il2csharp 的 `/* nothing */` / 空返回

**这直接证伪了《技术详解》宣称的"生成代码直接可编译运行"**，
也说明 il2csharp "门 = parseable + brace-balanced，不追求可编译"
的定位不是退缩，而是诚实。

---

## 6. 次优先：程序集选择流程

guide §1 花了大篇幅讲"只勾选业务逻辑 DLL"：

- 排除 `System.*`、`mscorlib`、`UnityEngine.*`、非业务第三方库
- 用本机 Unity Editor 自动识别引擎/框架/业务边界
- "自动分析和内置排除列表可以辅助筛选，但提交前仍需逐项确认"

对 il2csharp 的对应改进很轻：`--only` 现在是子串匹配，
`Assembly-CSharp` 会连带 `Assembly-CSharp-firstpass`。
可以加一个 `--exclude` 或内置逻辑程序集启发式（`System.*` /
`UnityEngine.*` / `mscorlib` / `Mono.*` 默认排除，`--all` 覆盖）。

收益：减少无关输出、缩短构建时间。优先级低于 §5，高于状态机之下。

---

## 7. 不建议抄的部分

| UREngine 特性 | 为什么不抄 |
| --- | --- |
| ARM64 优先 | Limbus 是 x64 PE；`arm64.py` 只是 scaffold，投入产出比低 |
| Studio GUI 客户端 | 与"加快执行速度/提高产出质量"的目标无关 |
| Unity 工程重建（Prefab/Scene） | 那是资源层，不是代码层；il2csharp 定位是反编译 |
| 代码相似度 / 司法鉴定 | 营销功能，非反编译核心 |
| 插件化架构 | il2csharp 的 mixin 组合已够用，引入插件体系是净负担 |
| "生成代码直接可编译运行" | 目标不可达且非当前目标；il2csharp 的门是 parseable + brace-balanced |

### 7.1 顺带一个可抄的小点：元数据启动开销

UREngine 的"函数级按需分析"效率来源是**不一次性加载整个二进制**。
il2csharp 方法论上是单方法的，但每次构建都全量解析
51,021 typedef / 319,009 method / 373,677 param / 204,180 field。

这与之前提的 **C# 复刻**是同一个优化的两面，不单独作为状态机任务的前置。

---

## 8. 下一步

| 优先级 | 事项 | 文档 |
| --- | --- | --- |
| **P0** | `sub_` / `/* nothing */` 失败原因与上下文（§5.3） | 计划待写 |
| P1 | async / 协程状态机还原（§4） | `docs/plans/2026-10-21-async-state-machine.md` |
| P2 | 程序集选择启发式（§6） | 计划待写 |

核心约束：严格遵循 il2csharp 的 decline-by-default 铁律 —— 拿不出
证明就保持今天的诚实拼写。**P0 尤其如此：它是在加强诚实性，
不是让输出变好看，所以绝不能为了"信息量"而编造失败原因。**
