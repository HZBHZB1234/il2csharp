# 计划：async / 协程状态机还原（2026-10-21）

**状态：待启动（探针未跑，不要先动手改源码）**
**上游依据：`docs/research-2026-10-21-urengine.md` §4**
**优先级：P1**（P0 是 `sub_` 失败原因，见 §9）

---

## 0. 这个计划在整体里的位置

2026-10-21 的 UREngine 对标得出三个可做项：

| 优先级 | 事项 | 计划文档 |
| --- | --- | --- |
| **P0** | `sub_` / `/* nothing */` 失败原因与上下文 | 本文档 §9（待展开） |
| **P1** | async / 协程状态机还原 | **本文档** |
| P2 | 程序集选择启发式 | 待写 |

P1 排在后，是因为它要新增 pass、动控制流、可能碰金色快照，
而 P0 几乎零风险。**但 P1 的用户价值更直观**（1,950 个类型从
不可读变为可读），所以两件事都值得做，只是顺序上 P0 先行。

---

## 1. 目标

把 IL2CPP 编译出的 async / 迭代器状态机，从

```csharp
private class <LoadSprite>d__1
{
    private int <>1__state;
    private void MoveNext()
    {
        switch (this.<>1__state) { case 0: ... }
    }
}
```

还原为可读的异步方法形态：

```csharp
private async Task LoadSprite(string path)
{
    ...
    yield return request;   // 或 await ...
}
```

**非目标**：不追求"还原成作者原始写法"。只还原状态机结构与控制流语义，
不推断设计意图（UREngine 那类示例不可达，也不该追）。

---

## 2. 第 0 步：探针（必须最先做）

**不要跳过。** 下面三个问题的答案决定投入规模，且都能在 10 分钟内测出。

探针目录：`docs/probes/`（已归档，见该目录 README；
原始位置 `C:\Users\tester\AppData\Local\Temp\opencode\`）

### 2.1 探针 A：状态机的真实规模与形态

已有数据（`probe_statemachine2.py`，2026-10-21）：

| 项 | 值 |
| --- | --- |
| `<MethodName>d__N` 类型 | **1,950** |
| `MoveNext` 方法 | **2,169** |
| `<>c__DisplayClass*` 闭包（已支持） | 4,012 |

待补测：

- [ ] 1,950 个里，多少带 `AsyncStateMachineAttribute`，多少带
      `IteratorStateMachineAttribute`，多少两者都无（拿不出证明的必须 decline）
- [ ] `MoveNext` 的 `<>1__state` 字段在产物树里的实际拼写
      （metadata 里搜不到 `__state`，说明 emitter 清洗过 —— 要确认清洗规则）
- [ ] state 字段的取值域：`0` 首入 / `-1` 完成 / `-2` 异常 是否成立

### 2.2 探针 B：现在的输出到底多难读

挑 3 个真实样本，量出**改造前的基线**：

- [ ] `<LoadSprite>d__1`（FMOD 加载）
- [ ] `<ExecuteAsync>d__*`（15 个，名字最像 async）
- [ ] `<GetEnumerator>d__*`（17 个，迭代器）

每个记录：行数、`switch` 个数、`goto` 个数、`sub_` 个数、`unknown` 个数。
**这组数字就是验收时的对照基线。**

### 2.3 探针 C：能恢复多少

对样本 B 的 3 个类型，尝试证明：

- [ ] `MoveNext` 的 `switch` 判别式是否就是 state 字段
- [ ] case 0 是否可证明是"首次进入"分支
- [ ] 是否存在 `builder.Start(ref stateMachine)` → 可证 async
- [ ] 是否存在 `yield return` 形态 → 可证迭代器
- [ ] 是否存在 `SetResult` / `SetException` → 可证 `Task` 完成路径

**若 C 的答案大面积为"否"，本计划降级为"只做识别 + 命名"**
（即把 `<LoadSprite>d__1` 标注为 `LoadSprite 的异步状态机`），
不做控制流重建。**不要为做而做。**

---

## 3. 实现阶段（仅在 §2 通过后）

### 阶段 1：识别（低风险，可独立交付）

新增 `il2cpp/dec/statemachine.py`（mixin，注册进 `Decompiler`）：

```
识别条件（全部满足才认）：
  1. 类型名匹配 ^<(?P<method>[^>]+)>d__(?P<num>\d+)$
  2. 该类型带 AsyncStateMachineAttribute 或 IteratorStateMachineAttribute
  3. 含一个 int 字段作为 state（名字形如 <>1__state / 清洗后的变体）
  4. 含 MoveNext 方法
```

产出：只做**标注**，不改控制流：

```csharp
// async state machine for LoadSprite (state field: <>1__state)
private class <LoadSprite>d__1 { ... }   // 拼写不变
```

**验收**：1,950 个类型的识别率；误识别数必须为 0（宁可漏认）。
**回归**：便携套件 1325 passed 不得下降；金色快照 64 个 body 的 hash
不得变化（本阶段不碰任何 body）。

### 阶段 2：MoveNext 结构化（中风险）

把 `switch (state)` 识别为状态分发，输出：

```csharp
private void MoveNext()
{
    switch (state)
    {
        case 0:  // initial entry
            ...
        case 1:
            ...
    }
}
```

即：给 case 加语义注释、把 `state = -1` 之后的代码识别为不可达。
**不重排控制流。**

**验收**：与 §2.2 基线对比 `goto` 数应下降；`/* nothing */` 不得增加。
**回归**：金色快照允许变化的 body 必须逐个读过再接受。

### 阶段 3：还原为 async / 迭代器（高风险，需单独审批）

仅当探针 C 能证明 `builder.Start` / `yield return` 时才做。
**任何一项证明缺失就保持阶段 2 的形态。**

---

## 4. 硬性约束（来自 CLAUDE.md，不可违反）

1. **`il2cpp/*.py` 必须 CRLF、无 BOM**。用二进制读写改，
   每次改完断言 `d.count(b'\r\n') == d.count(b'\n')`。
   参考既有模式：`work/patches/patch_*.py`。
2. **绝不先打开目标文件写**。在内存里构造完整内容、断言全过、再一次性写盘
   （batch 72 的教训：`open(p,'wb').write(f())` 会因 `f()` 抛异常留下零字节文件）。
3. **`PYTHONHASHSEED=0`** 始终设置。
4. **pass 顺序不可随意调整**。新增 pass 插在 `_structure` 的哪个位置，
   必须先读现有调用序列；多个 pass 互相依赖（死 phi copy 移除必须早于
   `&&`/`||` 折叠等）。
5. **decline-by-default**：拿不出证明就保持今天的拼写。`object objN` 是
   诚实标记，不为"好看"改名。
6. **不改 SEH 的 `d__100.MoveNext finally mid-switch` 补丁**，
   除非能证明状态机识别后它自然消解 —— 那是独立的已知产物。

---

## 5. 验证流程（每阶段都要走）

```powershell
$env:PYTHONHASHSEED = '0'
Set-Location 'E:\desktop\work\LimbusDecompile\il2csharp'

# 1. 语法 + 导入
python -c "import compileall,sys; sys.exit(0 if compileall.compile_dir('il2cpp', quiet=1) else 1)"
python -c "import il2cpp"

# 2. 便携套件（当前基线：1325 passed / 0 failed）
python -m pytest -q --disable-warnings -m "not game"

# 3. 单方法快速回路（不落盘）
tools/inspect_methods.py --metadata ... --binary ... --mi <MoveNext 的 mi>

# 4. 全量内存 sweep（~116k body，几分钟，抓崩溃）
python work/lib/sweep_audit.py <tag>       # work/ 在本 checkout 不存在，需内联

# 5. 括号审计（字面量感知）
#    work/lib/tree_brace_audit.py 同样不存在，用内联版
```

> **注意**：本 checkout 没有 `work/` 目录，`tree_brace_audit.py` /
> `sweep_audit.py` / `ts_gate.py` 都不可用。需要用内联等价物
> （本次会话已写过可用的字面量感知括号审计，可复用）。
> `tree_sitter` / `tree_sitter_c_sharp` 本次已装进 venv。

### 5.1 金色快照纪律

`tests/goldens_review84.json` 是 hash-only，锁定 64 个 body。
**任何导致 hash 变化的改动都必须逐个读过 diff 再接受**，
不许为了让测试过而重新生成快照。CLAUDE.md 原文：
"the goldens pin whatever the current source produces, bugs included."

---

## 6. 与进行中工作的关系

当前 `limbus_out1` 构建仍在跑（pid 27620，`--only Assembly-CSharp --workers 4`），
目标 32,907 类型，已完成约 9,383。本计划的探针**只读产物树与 metadata**，
不干扰构建。

若构建尚未结束，**不要启动全量重建** —— 状态机改动的验证要等这棵树出来，
或者用一个 `--max-methods` 限定范围的小构建 + 内存 sweep 代替。

---

## 7. 出口条件

- [ ] §2 三个探针全部有数据，且结论明确（做 / 降级 / 不做）
- [ ] 若做：阶段 1 交付，识别率与误识别数记录在案
- [ ] 便携套件不低于 1325 passed / 0 failed
- [ ] 金色快照变化逐个审阅并记录
- [ ] 括号审计 0 unbalanced
- [ ] 文档更新：`docs/todo.md` Current work + 本文档状态改为已交付/已放弃

---

## 8. 明确的放弃条件

出现以下任一情况，**停止并在文档记录原因**，不要继续投入：

1. 探针 C 显示 `<MethodName>d__N` 与 attribute 的对应关系大面积缺失
   （即拿不出证明的类型占多数）
2. 阶段 1 的误识别数 > 0 且无法收敛
3. 阶段 2 导致 `goto` 数不降反升
4. 金色快照出现无法解释的变化且无法归因

**宁可留下一个诚实的 `switch (state)`，也不要输出一个自信错误的 `async`。**

---

## 9. P0：`sub_` / `/* nothing */` 失败原因（计划待展开）

这是 UREngine guide 带来的最高优先级项，单独列在这里占位，
详细计划待写。核心思路：

il2csharp 内部**已经知道**为什么某个调用无法解析
（多候选无法定主 / 无候选 / 泛型未闭合 / ABI 未知 / 共享体 arity 无法 trim），
这些判定在 `_call`、`_shared_*`、`_icall_annotation` 里都做过，
只是没有往外传到渲染层。

要做的就是在既有 `sub_<va>` 渲染处**补上已计算的结论**：

```csharp
// 现在
sub_18084e320(type1, obj19, obj20, obj21)

// 目标（不改变表达式本身，只补注释）
sub_18084e320(type1, obj19, obj20, obj21)  // unresolved: 3 candidates, receiver chain cannot pick one
```

以及给 `/* nothing */` / 空体补显式警告，避免读者把"未能恢复"
误读为"原函数为空"。

**约束（比 P1 更严格）**：

- 只渲染**已经算出的**原因，绝不为了信息量而编造或猜测原因
- 不改变任何 body 的语义，因此金色快照 hash 不应变化
  （若变化，说明顺带改坏了别的东西，必须回退重做）
- 注释形式优先于 attribute 形式：`[Address]` 那类格式变更会同时影响
  金色快照与 parse gate，需单独评估

**探针**（同样是第 0 步）：

- [ ] 统计全树 `sub_` 的**成因分布**：多候选 / 无候选 / 泛型 / ABI 各占多少
- [ ] 确认这些成因在 `_call` 里是否真的都已判定（而不是需要新算）
- [ ] 若某类成因需要新算，评估其证明成本，拿不出证明的类别**不加注释**
- [ ] `--publicize` / `--raw-addr` 开启时加文件头声明（`emitter.py` 写
      `__SharedBodyStubs.cs` / `.csproj` 的同一条路径上挂一行），
      明确这些修饰符与 `__addr(E)` 是降级产物而非原始源码
      （依据：调研文档 §5.2a；这是三项里成本最低的，可先行交付）
