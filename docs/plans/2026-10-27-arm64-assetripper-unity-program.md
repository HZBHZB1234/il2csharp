# 计划：ARM64 lifter + AssetRipper fork + Unity 工程闭环（2026-10-27）

> **状态（2026-10-27）**：用户已批准，**押后执行**——先走
> [`2026-10-27-packaging-compile-gate-slices.md`](2026-10-27-packaging-compile-gate-slices.md)
> 的打包/编译门切片。本计划**推翻 2026-09-28 "平台支持 not planned
> soon" 裁定**（`2026-10-25-todo-roadmap.md` P4 搁置区"平台支持"行
> 的重启条件就此触发，该行已同步更新）。
>
> **证据与出处边界**：本计划的实验证据（§1）全部来自本仓库夹具与
> 开源工具的可复现实验。外部商业产品的对标细节（架构逆向、能力边界、
> 合规研究）仅存于本机笔记（未跟踪目录），本仓库一律不复述；2026-10-21
> 对标调研文档的"架构层不抄"结论继续有效，本计划针对的是平台与工程链。

## 0. 决策记录（全部用户拍板 2026-10-27）

| # | 决策 | 内容 | 依据 |
| --- | --- | --- | --- |
| D1 | 许可证 | 整仓 MIT → **GPL-3.0**（`LICENSE`/`public_release.md`/THIRD-PARTY-NOTICES 一次 commit）。GPL-3.0 是 AssetRipper 的许可证；进程内 fork 要求整仓同许可 | 用户明示 |
| D2 | 解码器 | **fARM64 主解码器**（valeria-org/fARM64，MIT，iced-x86-shaped API，`implicit_registers()`），capstone 5.0.7 降为对拍基线 | §1.3 实测 |
| D3 | 正文 | 自研 ARM64 lifter；**不接 Cpp2IL 做正文**（开源组件链在本语料 22.6% 干净率，不可用） | §1.2 实验 |
| D4 | 资产/Unity 工程 | **fork AssetRipper 做源码级改造**：其 `Export.UnityProjects` 已具备 Unity 工程导出能力；ScriptExport 槽位改为产出 il2csharp 正文，GUID/序列化绑定在 Processing 阶段天然成立，优于"导出后覆盖 .cs"。fork 放独立 GPL 仓库，主仓库通过依赖边界引用 | AR 上游公开事实 |
| D5 | Shader | 恢复纳入范围：AR 提取 → SPIRV-Cross 反编译 → **glslang 16.5.0 编译验证** → ShaderLab 包装（全部开源组件，Khronos 工具链） | 开源组件组合 |

## 1. 证据与实验记录（全部可复现；输入为本仓库 fixture 家族与开源工具）

### 1.2 Cpp2IL 解密实验（2026-10-27，Limbus 1.117.0 / Unity
6000.3.12f1 / ARM64，输入 `E:\download\libil2cpp_decrypted.so`，
metadata magic `0xFAB11BAF` ver 39）

| 指标 | 加密 so | 解密 so |
| --- | --- | --- |
| Cpp2IL `dll_il_recovery`（155 程序集） | 8 类型失败、无产物 | 成功，81.2 MB，**7m55s** |
| ilspycmd（Assembly-CSharp.dll） | 25 s（占位体） | 4m32s，24,718 个 .cs |
| 含 `Not implemented instruction` 文件 | 23,400/24,717（94.7%） | 14,026（56.7%） |
| 含 `Method not found @` 文件 | — | 18,247（73.8%） |
| **合并后干净文件** | ~5.3% | **22.6%** |
| 失败指令 top | 全盘 INVALID | BLR 32,104、LDUR 15,053、LDRH 14,378、MOVI 11,747、CSET 9,771、FCMP 8,058、CSEL 7,040（66 种**日常指令**缺失）；另 519,553 次调用目标解析失败、栈建模类型错乱（`(I)(obj - 1568)` 形） |

- 复现要点：批处理工程需注册 `AppDomain.AssemblyResolve` 从 `libs\`
  子目录解析运行时依赖（默认探测不含子目录）；该工程参数解析会把
  非 `--` token 全部当 outDir，**positional outDir 必须放参数最后**。
- 结论：正文不接 Cpp2IL（D3）；解密后的 so 是现成 ARM64 开发夹具；
  加密与解密两个形态各是一类输入，fixture 契约分开登记（§1.4）。

### 1.3 fARM64 解码器评估（2026-10-27，同输入）

- 全 RX 段（96MB 真实代码）：**25,167,396 条指令、0 invalid、12.0 秒**
  （~2.1M 条/秒，release）。
- .text 全段（1,547,693 条）与 capstone 逐条对拍：**100.00% 助记符
  一致**；仅 71 条别名分歧（`uxtl`↔`ushll #0`、`sxtl`↔`sshll #0`，
  fARM64 解析移位零别名，更可读）。
- 反向覆盖：capstone 5.0.7 在段内多个 2MB 窗口 **62% 的字解不了**
  （SVE2/SME 系：st1w/ld1w/sumopa/addva…）——分歧中 fARM64 是补齐方。
- 对拍 harness（解码 CLI + 对拍脚本，Rust）在本机未跟踪目录，待 A1
  采纳门通过后归档进 `docs/probes/`。
- 待办（A1 采纳门）：操作数级对拍（双基线 capstone + objdump）尚未
  做，采纳前必须完成。

### 1.4 样本事实与边界（重要：常态 vs dump）

- 样本：Unity 6000.3.12f1，metadata ver 39（与 PC 侧 fixture 同族）；
  ARM64 省略帧指针序言 `stp x30, xN, [sp,#-N]!`；段首 `bti c`（BTI
  存在，序言识别需处理）；本样本 pacibsp=0，但 PAC 形态已在 fARM64
  建模。
- **节头失真是 dump 重建样本的特性，不是常态**：`libil2cpp_decrypted.so`
  由解密工具从内存重组，`.text` 节头（5.9MB）与实际 RX 段（96MB 全
  代码）脱节、只读段散落 RET。**常态 APK 内 shipped 的 libil2cpp.so
  节头有效**。不写入常态契约。
- 通用稳健性原则（对一切输入形态成立）：**函数边界一律来自
  CodeRegistration/MetadataRegistration 方法指针 + EXIDX/runtime
  function 表，节头仅作提示**。这是工程稳健性，不是对节头的定罪。

## 2. 阶段 ARM-1…ARM-5：ARM64 lifter v1（6–10 个专注周）

- **ARM-1 解码桥（≤1 周）**：`farm64-ffi`（C ABI）+ ctypes 批量解码；
  `AInsn` 直通（`arm64.py` 脚手架已备，fARM64 API 即 iced 形状）；
  **采纳门 = 操作数级双基线对拍**（capstone + objdump，不过关切回
  capstone）；BTI/PAC 语义位。
- **ARM-2 指令语义（2.5–4 周）**：60–90 热点助记符带宽度/标志语义
  （MOV/MOVK/MOVZ、ADD/SUB/SUBS/CMP、LDR/LDUR/STR/STUR/LDP/STP/
  LDRH/LDRSW 族、B/BL/BR/BLR/CBZ/CBNZ/TBZ/TBNZ、CSET/CSEL/CSINC、
  标量 FP、位域 UBFM/SBFM/BFI）；NZCV + 条件选择建模；**未知指令失效
  传播从第一天接 `implicit_registers()`**（不重蹈 x64 静默 fall-through）；
  NEON v1 近似（LDP/STP Q 寄存器结构体拷贝），全向量延后。
- **ARM-3 调用约定与目标解析（2–3 周）**：AAPCS64（x0–x7 + v0–v7、
  x8 sret、RET x30）；calls.py 55 个识别器的 ARM64 重推导（iface 表
  扫描、虚调用目标、icall 选择、共享体 arity）；函数边界按 §1.4 原则。
- **ARM-4 EH（≤1 周，范围决策）**：v1 只用 EXIDX 做函数边界；catch
  区域恢复延后，seh.py 优雅降级并打标记。
- **ARM-5 验证与双夹具（1–2 周）**：
  - 常态夹具：从 1.117.0 apks 正常抽取（节头有效）或其他未加密
    Unity 6 游戏，按 `docs/fixtures.md` 注册；
  - 特殊夹具：`libil2cpp_decrypted.so` 登记 `dump-reconstructed` 标记
    （节头失真仅限此样本），开发期主测试床；
  - golden/gates 全套复用；portable 套件不回归。
- v1 验收：双夹具上多数正文可读、门禁绿、诚实降级标记；与 PC 侧
  （114,458 正文 / 0 失败）出对照报告。对齐 x64 全质量是数月切片长尾
  （55 识别器重推导），按 per-slice 节奏走。

## 3. 阶段 U0–U3：AssetRipper fork + Unity 工程闭环（2–3 周）

- **U0（半天）**：AssetRipper 2.0.0 官方构建（本机已自取，未跟踪）
  对 PC fixture 跑一次完整 Unity 导出，建立资产/场景/绑定基线。
- **U1**：fork AR（独立 GPL 仓库），ScriptExport 槽位接 il2csharp
  类型树；输入契约覆盖 APK 与 PC 数据目录两路（AR 对 PC/Steam 支持
  成熟）。
- **U2**：Unity 工程重建编排：ProjectSettings、Packages manifest、
  Unity Editor 版本校验（校验值取自包内 `globalgamemanagers`，不收
  手填）。
- **U3 验收**：目标游戏在真实 Unity 打开；脚本编译错误数 ≤ 打包计划
  切片 C 测得基线；场景 Play 可交互——"打开、编译、可运行"三件事
  是本阶段的产品级验收线。
- 前置：打包计划切片 C 的数字（编译率入场券）。

## 4. 阶段 S1–S2：Shader 恢复（1–2 周起步，依赖 U2）

- **S1 SPIR-V 变体先行**：AR 提取平台变体 → SPIRV-Cross 反编译
  GLSL → glslang 16.5.0 编译验证 → ShaderLab 包装。
- **S2**：DXBC/DXIL 第二批，Metallib 最后。
- 验收：目标游戏材质不粉。

## 5. 阶段 W1–W3：收尾（可选，后置）

- **W1**：apks 前端并入主 CLI（批处理工程代码迁移）。
- **W2**：加密检测门（metadata 加密 magic 拒收 + 代码段熵检查；
  dump 样本走豁免标记）+ 错误码族。
- **W3**：实时进度 UI；（可选）资产预览（非必需）。

## 6. 依赖图

```
打包切片 C（编译率基线）─┐
ARM-1→ARM-2→ARM-3→ARM-4→ARM-5 ─┼→ U1 → U2 → U3（Unity 闭环验收）
U0（AR 基线）──────────────┘
        U2 → S1 → S2（shader）
W1–W3 与主线并行后置
```

ARM 线与 U 线部分并行：U0/U1 的资产侧不依赖 ARM-2/3。

## 7. 风险清单

| # | 风险 | 缓释 |
| --- | --- | --- |
| 1 | fARM64 操作数级正确性未验证 | ARM-1 采纳门双基线对拍；AInsn 抽象可切回 capstone |
| 2 | fARM64 四个月龄、单一维护方 | fork 锁定 commit + 上游跟踪 |
| 3 | ARM64 codegen 形状重推导长尾 | 方法学/harness/探针全套现成，按 per-slice 节奏 |
| 4 | 未知指令失效传播 | `implicit_registers()` 第一天接入 + fARM64 全覆盖（0 invalid 实测） |
| 5 | 加密输入（常态 APK） | W2 加密检测门拒收 + 错误码 |
| 6 | GPL 组件分发合规 | 已 GPL-3.0；fork 源码可得 + THIRD-PARTY-NOTICES；分发含 GPL 二进制时附许可证全文与书面 offer |
| 7 | 编译率未知 | 打包切片 C 一周内出数，决定 U3 验收目标 |

## 8. 横切纪律

沿用 `2026-10-25-todo-roadmap.md` §7 全部条目（上游同步、一次一个
slice、decline-by-default、user-call 清单、度量口径、LF/PYTHONHASHSEED
契约），外加两条本计划特有：

1. **fixture 双形态契约**：常态 APK 抽取与 dump 重建样本分开登记，
   dump 标记只描述该样本，不得升格为一般性假设。
2. **GPL 纪律**：AR fork 独立仓库；主仓库不改 AR 源码则不承担其
   delta 披露；分发含 AR 二进制时附许可证全文与源码 offer。
3. **外部产品信息边界**：商业产品的对标细节只存于本机笔记；本仓库
   文档引用实验结论时以本仓库夹具与开源工具为主体表述。
