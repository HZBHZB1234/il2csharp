# 计划：TODO 推进路线图（2026-10-25）

> **进展注记（同日晚些）**：P0-1 的 b20-local 基线已测（pre-143：
> syntax 52,785 / binding 63,221，详见 `docs/todo.md` 顶部）并立刻
> 抓到两个真问题——(1) 本地 else-if peephole（c99e579）在 v39 上
> 产出 ~13.2k 语法坏行（**fix 143 已修**，765adb8）；(2) 逐 image
> 无引用编译的 CS0518×45k 方法论伪影（门禁 v2 需要分组/引用闭包，
> 下个 session）。fix 142a 已落地（0eb7ed1）。post-143 全量重建
> + 重测门禁是下一个 session 的第一件事。

> 依据 2026-10-25 的全量盘点写成：上游 `mynamescrax/il2csharp` 自分叉点
> `5291b7c` 后仅发布 `c3195dc`（fix 141，本地已手同步且 `analyze.py`
> 逐字节一致）；本地领先 36 个提交（perf 程序、peephole P0/P1、GC
> cardmark、v39 元数据修复、fixture 框架）。上游 fix 141 挂出的三项
> 后续中，game recount 与 golden 重钉已被本地 fixture 迁移实际完成/
> 消解，仅剩 `_` → `default` 一项两边都 open。本文件是活文档；
> 每完成一项就回写状态，不做完不删条目。

## 0. 状态快照（2026-10-25，`main` = `3f1a1f5`，工作树干净）

| 指标 | 值 | 说明 |
| --- | --- | --- |
| Roslyn gate（r_base → b19 本地） | 828,571 → 454,955（-45.1%） | b19 = fix 140，旧 fixture 上测得 |
| Roslyn gate（上游 b20） | 439,578（-46.95%） | 上游证据，旧 fixture，**不迁移** |
| 本地 fix 141 后基线 | **未测** | 只有配对重建 + census，见 P0-1 |
| 套件 | 便携 1,380 passed；game 1,400 / 2 env 失败 / 1 xfailed | 2 个失败缺 `Unity.Burst.Unsafe`，pre-existing |
| 门禁工具 | `tools/compile_gate.py`（per-image，syntax 门禁 / binding 报告） | 全树计数需小驱动汇总 |
| 完整树 | `out/limbus/v39-gates` 在位 | P0-1 可直接跑 |

## 1. 排期总览

| 层 | 内容 | 性质 | 需用户决策 |
| --- | --- | --- | --- |
| **P0** | 基线复测 + 5 处文档滞后清理 | 簿记，半天级 | 否 |
| **P1** | 4 个既定小 slice | 每个 = 标准流程一轮 | `_`→`default` 一项是 |
| **P2** | C 族主线（C1 → C2 → C3 → C5 → 小族） | backlog 既定顺序 | promotion / 重钉时 |
| **P3** | async 状态机探针 C → 分叉决策 | 计划文档已门控 | 阶段 2/3 需单独审批 |
| **P4** | 搁置区（sidecar、平台、Megabonk…） | 不排期，仅记录 | 已裁定 |

层间不严格串行：P2 的探针（只读）可以与 P1 的落地并行；
P3 的探针 C 同理。**落地永远一次一个 slice，直接在 `main`。**

---

## 2. P0 — 基线与簿记（先做，其余一切的前置）

### P0-1 本地 Roslyn 基线（b20-local）

上游 b20 = 439,578 是已删除旧 fixture 上的数字，不能作为本地度量基准；
本地 fix 141 落地后从未在完整树上复测过。没有这个数，后面每个 C 族
slice 的 delta 都无从计量。

- 对 `out/limbus/v39-gates` 逐 image 跑 `python tools/compile_gate.py
  --tree <imgdir>`，写一个小驱动汇总全部 image 的错误数（按 CS code
  分桶），产出 **b20-local** 与失败集快照，写入 `docs/todo.md` 顶部与
  `validation_reports/limbus/`。
- 若树已陈旧（fix 141 之后没重建过），先 `python il2csharp.py --fixture
  limbus --label v39-gates` 全量重建（`--workers` 已可用，perf 程序后
  全 AC 约 86 min 量级），再跑门禁。树与计数都要记录构建源 commit。
- 顺带确认两个已知环境问题是否仍在：tree-sitter parse gate 对
  whole-image parse 段错误；`Unity.Burst.Unsafe` 缺失导致的 2 个套件
  失败。环境问题记录在案即可，不算代码债。

### P0-2 文档滞后清理（5 处，全部有据可查）

1. `docs/todo.md:635-637`：follow-up 行仍列 CS0019 `object op int` 为
   open —— fix 135/136（`22a5186`）已做掉，划掉并指向落地记录。
2. `docs/todo.md:199`（fix 140 区块）："re-pin of all 10 pending user
   approval" —— 已被 v39 fixture 迁移消解（v39 语料上零 pin 移动），
   标注消解方式。
3. `docs/todo.md:309`（fix 137 区块）："NOT landed, NOT pushed" ——
   `2e440fe`/`e1d9803` 已在 main 共享历史落地（fix 138 关闭了它的
   blocker），状态行更正；上游 todo 同样带着这行，下次同步时不接受
   上游侧的该旧文本。
4. `docs/plans/2026-10-21-async-state-machine.md:8`："待启动（探针未跑）"
   —— Stage 1 已于同日落地（`3c6ef10`，1,863 识别 / 0 误报），状态行
   改为"阶段 1 已交付（简化版：识别+注释）；阶段 2/3 待探针 C 分叉"。
5. `AGENTS.md` fix 124 条目 "complete on branch …, not merged" ——
   `d97dd15` 已是 `main` 祖先，改记为已合并。

**验收**：5 处都有 diff；不碰任何代码文件；套件不受影响（纯 docs）。

---

## 3. P1 — 既定小 slice 队列（每个独立落地，一次一个）

### P1-1 接口偏移表 1 字节 index-form raw read

- **来源**：fix 134 明确遗留的下一候选（todo.md:260-262）。
- **规模**：2,320 个 for-head CS0019（b13 数据），形状已探明：
  `((byte*)__addr(k) + (i + i)*8 + 0x0)[0] != typeof(I)` 的 index-form
  读被 fix 134 的 field-form-only 范围排除。
- **做法**：`_width_mark` 家族扩展到 index-form（接口表扫描的 stride
  已被 fix "array-addr stride cache" 建模），或按上游当年给出的方案
  (b) 走 `List<T>._size` 式泛型实例字段解析。先探针定形状分布再选。
- **验收**：for-head CS0019 2,320 → 接近 0；golden 预期有移动，逐个
  读 diff，重钉走用户审批。

#### P1-1 探针结论（2026-10-25，重塑为 fix 142：v39 helper 再证明）

**状态：fix 142a 已落地（见 `docs/todo.md` 顶部区块）——v39 模板
点亮命名/arity-trim/ifaceprune/管理式折叠；R8=方法槽号经
mi 290837（MoveNext@0 / Current@1，`FileHash` 类型闭合）经验证实，
142b 的歧义已消解；142b 仅剩退化接收者拼写 nit
（`IDisposable.Dispose(0)`）。** 探针正文保留作证据链：

探针在常驻 v39 树上实测并原生验证，结论推翻了"宽度标记"的原设计：

1. **人口**：`((byte*)E + (N + N)*8 + 0x0)[0] (!=|==) typeof(I)` 形状
   在常驻树（pre-141）= **2,917 行 / 1,014 文件，100% 在 for 头上**
   （非 for 行为 0）。每站点伴生三处宽度错误：接口数 `[k+0x12E]`
   （word 读成 1 字节）、表指针 `[k+0xB0]`（qword 读成 1 字节）、
   表项比较（qword cmp 渲染成 `[0]` byte）；hit 臂还有
   `((byte*)E + 0x0)[0]()(args)` 间接调用（CS0149 族）。
2. **根因**：fix 139 的 `ifaceprune` 第一道门要求 miss-call 的 helper
   已被命名（`names.get(target) == 'il2cpp_interface_get_method'`）；
   命名由 `_is_iface_resolve_helper`（`lifter/state.py:315`）给出——
   一个**钉死旧 fixture helper 字节的模板**（精确 24 字节序言 +
   恰 4 次 `call rel32` + 0x89 长度 + 尾 int3）。v39 运行时
   （Unity 6000.3.12f1）的 helper 在 `0x180789290`，代码生成完全
   不同 → 模板失灵 → 命名 0 处（树内 `il2cpp_interface_get_method`
   出现 0 次）→ **ifaceprune 在 v39 上整体失明**。对照：
   class-init（1,057 处命名）与 array-addr（26 处）检测器在 v39
   存活。
3. **v39 helper 定性**（0x180789290，原生反汇编验证）：extent
   0x1A9（旧 0x89 的两倍），13 次内部 call，**R9 零触碰**（第 4 参
   spray 性质成立），尾部
   `movzx r8d,r14w; mov rdx,rbp; mov rcx,r13; call rel32; int3`，
   保留语义不变量 `test byte [klass+0x136],0x10` 与
   `cmp [obj+0x10],rax`。新 lift（当前源码）确认扫描仍在输出里
   （mi 290837 `BuildHashes.PrintToConsole`）。
4. **扫描解剖**（mi 290837 @0x1808b0520）：`r13d` 开头 `xor` 清零 →
   扫描从 pair 0 起、16 字节步进（`rax = i*2; [r8+rax*8]`）比较
   pair[i].interface == iface klass；miss 臂
   `il2cpp_interface_get_method(obj, iface, 0, typeof(I))`——R8=0
   与扫描起点一致。
5. **R8 语义（142b 的判别）**：树内 3,032 个 miss 调用（2,989 个
   4-参 `(recv, typeof(I), S, typeof(I))` 形状）的第三参**逐站点
   变化**：0×1523、1×424、2×224、3×58、5×46、7×45、173×25、71×22、
   10×20……与真实运行时 `GetInterfaceInvokeData(obj, itf, slot)` 的
   **方法槽号**语义吻合，排除"恒为扫描起点"。但 mi 290837 上 R8 又
   等于开头 `xor` 清零的扫描起点寄存器 `r13d`（`xor r8d,r8d` 即
   `mov r8d,r13d` 的编译器化简）——slot=0 站点上两种解释不可区分。
   helper 自身对第三参做了 `cmp r14w, [iface+0x12A]` 的越界检查
   （对 iface 的某个 count），偏向方法槽号读法。
6. **分阶段落地**：
   - **fix 142a（含经验验证）**：`_is_iface_resolve_helper` 增加按序
     尝试的 v39 模板（前 30 字节序言 + 两个 klass 不变量 + 尾形
     `movzx r8d,r14w; mov rdx,rbp; mov rcx,r13; call; int3` +
     长度界 0x40<len≤0x400），点亮命名 + arity-3（R9 spray 剪除）
     → ifaceprune 复明 → 2,917 for 头整族从输出消失；`_ifm`
     折叠（calls.py:3094，键于命名）随之激活——**必须经验验证**：
     提 slot=1/2 的站点（第三参 1/2 共 648 个），核对渲染的管理式
     方法名与接口声明序一致（错名会立刻显形为 arity/用法错位）；
     若发现错名，给 `_iface_resolve_target` 加 v39 形状 decline。
   - **fix 142b（如 142a 验证发现错名）**：解决 R8 语义歧义后再
     放开 `_ifm`。
7. **验证计划**：142a 用 ACTk.Runtime（扫描重灾区：BuildHashes /
   StandaloneWindowsWorker）做配对重建 + `--mi` 重提（290837 必查）；
   brace 0；便携套件不降；full-tree delta 待 b20-local 基线出来后
   补量。

### P1-2 `_` → `default` 可编译拼写（上游遗留的唯一条目）

- **来源**：上游 fix 141 原文 "a compilable `default` spelling is a
  separate user-call slice"；CS0103 `_` 洞 728 → 827。
- **语义决策（需用户拍板，这正是上游把它标为 user-call 的原因）**：
  `_` 是诚实洞（未命名 stale 值），`default` 是宣称值（可编译但可能
  不是原生语义）。按 P4 "compiles never outranks correct"，倾向
  **保持 `_` 默认、加 opt-in 开关**（与 `--raw-addr`/`--publicize`
  同类的降级产物开关，文件头声明）。若用户裁定直接改默认，则：
- **实现点**：`lifter/calls.py:706-708` 的 `'_'` 占位 → 目标类型
  `default`；emitter 已有 `= default` 路径（`emitter.py:468`）可复用。
- **验收**：开关关 = 输出逐字节不变；开 = `_` 洞清零、delta 分类
  无其他变化。

### P1-3 fix 135/136 remainder

- `__addr((objN + 0x80))` 帧/结构体基形状（探针 6,443 个）；
  call-defined temps（847 个）；CS0103 remainder。沿用
  `_numeric_obj_retype` 的证明式收紧（def 全整数 / 无引用式使用），
  拿不出证明的形状照旧 decline。

### P1-4 fix 140 nit

- 绑定的 narrowed result 误声明 `object`（`object obj35 =
  ((ASN1)...).GetBytes()`，mi 277）：bind 携带 byte[]，声明层跟类型。
  小改动，与 P1-1 同批落地亦可。

---

## 4. P2 — C 族主线（backlog 既定顺序，按预期收益）

> 流程不变：probe → patch → 便携测试 → 定向 `--mi` 重提 → 配对重建
> → gate delta（以 b20-local 为基数）→ 套件（failure set 逐字节比对）
> → docs → commit。每族落地后回写本文件与 `docs/todo.md`。

### P2-1 C1：共享/ICF 调用命名（最大单项）

- CS0103 最大驱动：~10.2k trailing-spray + ~4.0k `.ctor`-as-value。
  隐藏 `MethodInfo*` 参数（RDX/末参）命名真实 callee，随后按解析出的
  arity 截断 spray；base-ctor 尾跳 → `: base(...)`。
- **与 fix 141 的边界**：141 处理 guard-join phi 喷射（join 后的
  all-unknown phi），C1 处理共享体 methodinfo 形状（body 级 spray），
  互补不重叠；落地前先跑一次联合 census 确认残余 population 分层。
- 上游当年指出 fixture 内单实例渲染诚实的路径疑似绕过 candidates
  检查（dec direct-tail `_emit_tail`，cf. slice 2b）——探针先验证。

### P2-2 C2：原始偏移的字段解析

- CS0030/CS0208 最大份额。递归内部偏移（`0x18` inside Vector3 field
  at `0x10` → `.field.z`）。**必须在 Expr/lifter 层做**（类型信息在
  textpass 已丢失）——与 backlog 的长期方向（正则 pass 迁 IR）同向，
  这一项就是第一个践行者。

### P2-3 C3：lane 合并（= SIMD follow-up 的另一半）

- `movsd [rcx],xmm0` 拆分 store → 单个 struct 赋值；绝不往 struct
  字段写单 lane。repro mi 24267。
- **既定约束**：SHUFPS 的 destination 失效建模（F1 剩余一半，
  ~1,646 live read）必须与 MOVSS merge 一并落地——两条线在此汇合，
  排期时当一个 slice。

### P2-4 C5：runtime-bookkeeping 移除

- `il2cpp_codegen_initialize_runtime_metadata`、~17k klass-field
  检查、`__static_fields` blob → `Class.Field`。多为删减类改动，
  风险低收益稳，可在 C1/C2 的等待期穿插。

### P2-5 小族穿插

- C4 raw fallback helper（`Il2CppRaw.Ref<T>`；helper 计数记债务）、
  C6 未声明 stack-arg temps、C8 泛型拼写、C10 publicize（opt-in）。
  每族独立验收；C4 与 P1-2 的 `_`→`default` 共享"降级产物须声明"
  的设计原则，先定文件头注记格式再动。

---

## 5. P3 — async 状态机（独立计划已门控，按门走）

计划文档：`docs/plans/2026-10-21-async-state-machine.md`。
Stage 1 已交付（`3c6ef10`：`Emitter._state_machine_note`，两道门，
1,863 识别 / 0 误报，只加注释）。

**探针 A 已完成（2026-10-25，见计划文档 §2.1）**：1,949 个状态机
声明在产物树里 100% 可分类——1,096 async（struct `IAsyncStateMachine`
+ `__t__builder`）+ 853 iterator（class `IEnumerator`）+ 0 decline；
分类判据来自声明本身，attribute 解码不再需要。剩余按原计划门控：

1. **Stage 1.5（新分叉点，低风险可独立交付）**：`_state_machine_note`
   写出诚实的种类（iterator/async），判据 = 声明段的接口/字段形状。
   post-b21 落地（会动 1,949 个注释，golden 需配对重建评估）。
2. **探针 C（可证明性）**：对真实样本证明 async 侧 `builder.Start` /
   `AwaitUnsafeOnCompleted`、iterator 侧 yield 状态形态。大面积可证明
   → 阶段 2（MoveNext 结构化）；否则按计划降级关闭，C9 定格为
   "识别+标注"。
3. **阶段 3（re-sugar）**：仅当阶段 2 交付且探针 C 全绿，需单独审批。

---

## 6. P4 — 搁置区（不排期，防止重复盘点）

| 项 | 搁置原因 | 重启条件 |
| --- | --- | --- |
| sidecar 程序（method+generic 5.6k、mega-shared 3.9k、struct-field folding、per-arm Color…） | 大工程，by design deferred；多数子项需要 use->def 前置 | C2 落地后重估（类型层基建可复用） |
| isinst klass 表达式 ~4,666、bounds slice B、多参分发、untyped-R9、single-field-struct returns | 同上，需 element-class provenance / use->def | sidecar 或 C2 前置就绪 |
| Cpp2IL side B | 需外部二进制 | 用户提供 Cpp2IL 产物 |
| Megabonk 46 | 等 method list / binaries | 材料到位 |
| 平台支持（Linux/macOS/Android 深化） | 用户已裁定 not planned soon（2026-09-28） | 用户翻案；已知低成本切入点：`cli.py` 发现扫描只认 `gameassembly.dll`/`libil2cpp.so` |
| Dec F5 余项 | latent，0 corpus hits | 出现 corpus 命中再做 |

---

## 7. 横切纪律（每个 slice 都适用）

1. **上游同步节奏**：每次本地落地后 `git ls-remote
   https://github.com/mynamescrax/il2csharp` 一眼；上游仍停在
   `c3195dc`。上游新 fix 大概率继续需要手同步（fixture 框架、
   emitter/dec 均已分叉），沿用 fix 141 模式：代码逐字节搬、测试在
   本地 `game("limbus")` 框架上重写、上游 gate 数字一律视为不迁移。
2. **一次一个 slice**，直接在 `main`，不开分支/worktree（用户
   2026-10-06 裁定）。
3. **decline-by-default**：拿不出 native proof 的形状保持今天的
   拼写；`object objN` 是诚实标记，不为编译通过猜 cast（P4）。
4. **user-call 清单**（不擅自执行）：golden/pin 重钉、全量
   promotion、快照重生成、`_`→`default` 的默认语义、阶段 3 re-sugar。
5. **度量口径**：一切 delta 以 P0-1 的 b20-local 为基数；套件
   failure SET 逐字节比对；golden hash 变化逐行读过才接受。
6. **契约**：`PYTHONHASHSEED=0`；`il2cpp/**/*.py` LF no-BOM，改后
   断言 `data.count(b'\r') == 0`；探针脚本放临时目录或
   `docs/probes/`，不进 `tools/`、不落 repo 根。

## 8. 里程碑（建议的检查点，非承诺日期）

- **M1**：P0 完成 —— b20-local 数字在案，5 处文档修正落地。
- **M2**：P1-1 / P1-3 / P1-4 落地 —— for-head CS0019 清零，
  CS0019 族再下一档；`_`→`default` 随用户决策或缓行。
- **M3**：C1 落地 —— CS0103 最大驱动清零（预期 b20-local 基础上
  -1 万量级）；此时再校准一次各族剩余占比，决定 C2/C5 顺序。
- **M4**：探针 C 有结论 —— async 线分叉（做阶段 2 / 降级关闭）。
- **M5**：C2 落地 —— CS0030/CS0208 大头消失，sidecar 重估。
