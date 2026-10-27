# 计划：打包/编译门切片（三档风险分级，2026-10-27）

> **状态（2026-10-27 更新）**：**已并入
> [`2026-10-25-todo-roadmap.md`](2026-10-25-todo-roadmap.md) 作为其 §7
> "P5 — 打包/编译门轨道"，并**排在 P0–P4 全部完成之后执行**（用户
> 2026-10-27 裁定）。本文件保留为详规与原始依据；排期、顺序与验收
> 以路线图 §7 为准，两者冲突时以路线图为准。
>
> 原文保留：已批准，先于 ARM64/AssetRipper 大计划执行（大计划见
> [`2026-10-27-arm64-assetripper-unity-program.md`](2026-10-27-arm64-assetripper-unity-program.md)）。
> 与路线图的关系：P0–P4 codegen 主线不动，本计划是**独立的
> infra/打包轨道**；P0-1 基线只约束 codegen delta 计量，不约束本计划
> Tier-1/2 切片。落地永远一次一个 slice，直接在 `main`（横切纪律沿用
> 路线图 §8）。

## 0. 依据（一段话）

仓库现状的自查结论：**反编译正文管线已达标，组织层缺位**——根层无
`.sln`/类型索引/工作区文件，91 个镜像平铺无游戏/引擎分层，无 Unity
工程形态的导出，"可编译"叙事缺一个真实度量。外部商业工具的对标细节
存于本机笔记（未跟踪，本仓库不复述）；2026-10-27 的两组开源实验
（Cpp2IL 解密实测、fARM64 解码器评估）的证据附录见 ARM64 计划文档
§1。本计划只补组织层，正文管线零改动。

## 1. 三档风险分级

| 档 | 切片 | 差异性质 |
| --- | --- | --- |
| **Tier 1 零风险纯增益** | A1 class-index.json；A2 根 `.sln` + `.code-workspace`；B1 `--profile`；C 游戏/引擎编译门；E `--layout unity`（opt-in） | 不改任何已有文件的字节；goldens、MANIFEST、parse/brace 门全不动 |
| **Tier 2 条件安全** | A3 `--layout grouped`（opt-in）；B2 `--workers` 默认自动；B3 进度行 | 默认零差异或仅行为变化（资源占用/stdout）；树内字节不变 |
| **Tier 3 必然产生差异** | D 裸 `[SerializeField]` | 全 MonoBehaviour 文件字节变 → game goldens 成批移动 → 全量失败集重数 + 用户重钉审批；**挂起，等重钉预算** |

## 2. 切片 A：根层组织（Tier 1 + A3 Tier 2）

**A1 `class-index.json`（类型→文件索引）**

- emitter 写每个类型文件处（`emitter.py` `_emit_one_top`，`dirp =
  os.path.join(asm_dir, *rel)`）已计算 `(td, base, rel)`；worker 的
  delta 返回值增加一组 `(assembly, role, ns, file, typedef_index)` 行，
  parent 在镜像循环收尾聚合，按 metadata 顺序（镜像序 → TypeDefIndex）
  写 `<out>/class-index.json`。风格对齐既有 `script.json`/
  `stringliteral.json`（`cli.py:552`）。
- 触点唯一：worker delta 元组协议——并行一致性测试必须覆盖新根文件。

**A2 根 `.sln` + `.code-workspace`**

- 在 `cli.py` 收尾（`MANIFEST.json` 写入点附近）生成；GUID 用
  `uuid5(NAMESPACE_URL, asm_name)` 确定性派生（与 `PYTHONHASHSEED`
  无关），两次构建 byte-identical；游戏/引擎两个 solution folder。

**A3 role 分类 + 分层目录（opt-in）**

- 按镜像名前缀分类：`mscorlib/System.*/UnityEngine*/UnityEditor*/
  netstandard/Microsoft.*/Mono.*` → Engine，其余 → Script。
- 实现点：`_assembly_dir_name(img.name)`（`emitter.py:1604/1625` 都经
  它取目录名）加 `--layout grouped` 前缀。gates/compare_trees 走树遍
  历不假设路径（已核）。MANIFEST 路径随布局变——**先 opt-in，完整
  limbus 重建 + 双门全绿后再议翻默认**（用户 call）。

**验收**：portable 套件全绿；limbus 全量重建后类型文件零 diff、新根
文件在位、brace 0、parse 0/0/0/0；串行 vs `--workers 8` 含新根文件
byte-identical。

## 3. 切片 B：速度 UX（Tier 2）

- **B2 `--workers` 默认自动**：默认从 1 翻为 0（`_auto_workers()`，
  `cli.py:216`，半核 cap 8；内存注记：12 workers 峰值 ~8GB，默认 8
  安全）。输出 byte-identical 是已证明契约（全 8-worker 构建 == 串行）。
- **B1 `--profile`**：新 flag，写 `<out>/profile.json`（**不动
  MANIFEST**），分相计时 metadata 加载 / registration / 每镜像
  lift+emit / tail 写入。顺带回答"小语料固定开销"（ARM64 计划的
  前置事实之一）。
- **B3 进度行**：pool 路径已保证与串行同日志（`cli.py:151` 注释），
  加每镜像完成行 `N/M images: <asm> (K files)`；落地前 grep 确认无
  测试断言精确 stdout，否则做成 opt-in `--progress`。

**验收**：portable 套件绿；MANIFEST 字节不变。

## 4. 切片 C：游戏/引擎编译门（Tier 1，北极星指标）

**目标**：把"可编译"叙事的度量从全树 45.5 万错误改为**游戏程序集对
真实 UnityEngine 的错误数**。该模式（游戏代码引用真实引擎程序集，
而非反编译引擎自重写 BCL）绕开全树编译债的主体——45.5 万错误的大头
本就在 mscorlib/UnityEngine 自身镜像。

- 复用切片 A3 的 role 分类：门只跑游戏程序集 csproj。
- 实现点：`tools/compile_gate.py`（P0-1 已在用的 per-image 门）加
  模式——gate 侧 shadow 目录放 `Directory.Build.props` 注入
  `<Reference>` 指向真实 Unity 安装的 `Editor/Data/Managed/
  UnityEngine/*.dll` + netstandard facade；emitter 输出零变化。
- 产出 `validation_reports/compile_game_<fixture>.json`：每程序集错误
  数 + 按 CS code 分桶。
- **前置输入（需用户提供）**：Unity Editor 安装路径（Managed 目录），
  或允许从 `Program Files/Unity/Hub/Editor` 自动探测。
- 该数字同时是 ARM64 计划 U 阶段（Unity 工程闭环）的验收目标基线。

## 5. 切片 E：`--layout unity` 导出骨架（Tier 1，opt-in）

- `<out>/unity/` 下生成：游戏程序集按 `Assets/Scripts/<asm>/<ns>/
  Type.cs` 映射（或从已有树复制）、最小 `Packages/manifest.json`
  （空 dependencies + 注释）、`ProjectSettings/ProjectVersion.txt`
  （**需 `--unity-version` 参数**：global-metadata.dat 不携带 Unity
  版本，诚实做法是让用户给）、标准 `.gitignore`。
- csproj 加 UnityEngine 引用（复用切片 C 的注入）。
- **明确不做**：场景/prefab/GUID 绑定、纹理网格转换——decline by
  default，由 ARM64 计划 U 阶段的 AssetRipper fork 接管；manifest 里
  写清"本产物只含脚本"。
- 风险：opt-in，默认输出零变化。

## 6. 切片 D：`[SerializeField]` 裸拼写（Tier 3，挂起）

- 现状全限定 `[UnityEngine.SerializeField]`（`emitter.py:906-911`）。
- 改裸拼写 + 文件头显式补 `using UnityEngine.Serialization;`（仿
  `using static __SharedBodyStubs;` 头机制；`UsingTracker`
  （`csharp.py:81`）对裸名不会自动补 using，必须显式加）。
- 代价：所有 MonoBehaviour/ScriptableObject 后代文件字节变 → goldens
  成批移动 → 全量失败集重数 + 用户重钉。**单独切片、最后做、等预算**；
  也可以 decline（纯拼写问题，raw is honest）。

## 7. 执行顺序

```
A1+A2（纯增益） → A3（opt-in） → B2/B1/B3 → C（等 Unity 路径） → E
D 挂起（重钉预算到位再动）
```

每片标准流程：temp 探针 → 补丁 → compileall → portable 套件 → 定向
`--mi` 重提 → 配对重建 → 全量失败集重数 → docs/commit。LF 无 BOM
断言（`data.count(b'\r') == 0`）适用于每个新文件。

## 8. 与 ARM64 大计划的接口

- 切片 C 的编译率数字 = 大计划 U 阶段验收目标的基线。
- 切片 E 的 `Assets/Scripts` 布局 = 大计划 U1（AR fork ScriptExport）
  的落点预演。
- `--profile` 的小语料固定开销数据 = 大计划 ARM64 阶段的启动事实。
