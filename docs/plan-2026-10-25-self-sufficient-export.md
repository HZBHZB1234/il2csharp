# 计划：让导出树自足（不再需要回 dump.cs 找东西）

> 触发事件（2026-10-25 真实案例）：做下载加速分析时，我在 v39b21 导出里 grep
> `WebRequestQueue`，一度得出"Addressables 运行时不在导出内、得去 dump.cs 查"的
> 错误结论，实际该类型在 `Unity.ResourceManager/UnityEngine/ResourceManagement/WebRequestQueue.cs`，
> 且相关方法体（`InitializationOperation.Execute` 直接写 `s_MaxRequest` 字段）
> 只有导出里有、dump.cs 根本没有。翻案靠的是：显式 path 复跑 grep + 核对 mtime。
> 本计划把"为什么会出现这种局面"和"工具层怎么杜绝"落成条目。

## 一、踩坑链复盘（需求来源）

1. **跨程序集归属易错**：`UnityEngine.ResourceManagement.WebRequestQueue` 在
   `Unity.ResourceManager.dll` 不在 `Unity.Addressables.dll`（Addressables 2.x 把
   命名空间拆到两个程序集）。按命名空间猜程序集 → grep 错目录 → 误判"缺失"。
   → 需要**树内权威索引**回答"类型 X 在哪个文件"，不靠猜。
2. **"树里没有 X"不可判定**：v39b21 根部没有 MANIFEST.json（旧版工具产物），
   无法知道这棵树用没用 `--only`、跑没跑全；且树可被多次运行拼接
   （本案例：Assembly-CSharp 10:38 产物 + Unity.Addressables/Unity.ResourceManager
   13:45 补跑产物，mtime 实证）。→ 需要**每次运行都留清单**、**覆盖度可对账**。
3. **grep 假阴性代价高**：无显式 path、`head` 截断、ugrep 并行输出，都可能造成
   "看起来没有"。工具无法根治用户姿势，但可以把"grep 碰运气"变成"查索引"。

## 二、已核实的现状（2026-10-25，HEAD=6a9d196）

已有、无需重做：
- `MANIFEST.json` 默认写树根（`il2cpp/cli.py:_write_manifest`，含 `flags.only`、
  metadata/binary sha256、源码指纹）——v39b21 缺它只因树是旧版跑的，重跑即得。
- `script.json` / `stringliteral.json` 默认写树根（`cli.py:552-553`）。
- 每类型文件带 `// RVA:` 注释；`--types`/`--only` 过滤；`--workers` 字节不变树。

缺失：
- 树内没有"类型→文件"索引；回答"X 在哪"只能全树 grep。
- summary 只有全局计数（files/lifted/failed/fallbacks/emit_failed/ms/bodies），
  **没有 per-assembly 统计，更没有 vs metadata 的覆盖度对账**——"是不是全导出了"
  无法从树本身回答。
- 二次运行没有 top-up 语义：`--only` 补跑后 MANIFEST 被整树覆盖，只记录最后一次
  运行的 flags，先前运行的信息丢失（provenance 断裂）。

## 三、改造项

### P0-A 树内类型索引：`INDEX.md` + `types.tsv`

- 位置：树根（与 MANIFEST 同级）。emitter 已遍历全部 typedef，顺手输出。
- `types.tsv` 列（TSV 优先于 JSON：grep/awk 一行命令可用）：
  ```
  full_name  assembly  file  typedef_index  kind  nested_in
  ```
  - `full_name`：命名空间+类型全名（嵌套用 `Owner/Nested`）。
  - `file`：相对树根路径。**嵌套类型行指向 owner 文件**（与 `--types` 语义一致），
    另加 `nested_in` 列填 owner 全名（顶层留空）。
  - `kind`：class/struct/interface/enum；`typedef_index` 保留 Il2CppDumper 兼容定位。
- `INDEX.md`：人读摘要——每程序集：类型数（顶层/嵌套）、文件数、未还原体计数、
  指向 types.tsv。开头放使用示例（`grep -P '^UnityEngine\.ResourceManagement\.WebRequestQueue\t' types.tsv`）。
- 验收：任何"X 在不在/在哪个文件"用一条 `grep types.tsv` 回答，不需要 dump.cs。

### P0-B 覆盖度对账：per-assembly 缺失清单进产物

- 新增 `coverage.json`（树根）：per assembly：
  ```
  { "metadata_typedefs": N, "emitted_top_level": M, "emitted_nested": K,
    "missing": ["FullName", ...], "compiler_generated": [...] }
  ```
  MANIFEST/summary 只放计数（`coverage: {asm: {meta: N, emitted: M, missing: n}}`），
  明细进 coverage.json，防 MANIFEST 膨胀。
- 计数口径（易错点，必须写死）：
  - metadata 侧用 TypeDef 表**全量**（含嵌套 typedef，Il2CppDumper TypeDefIndex 同口径）；
  - emitted 侧：顶层 = 文件数，嵌套 = typedef 中 `DeclaringType != 0` 者，归 owner；
  - 排除/单列编译注入项（`<Module>`、`PrivateImplementationDetails`、
    `EmbeddedAttribute` 等），别把它们算成缺口；
  - `--types`/`--only` 过滤运行时，coverage 只对**被选中的范围**对账，并在
    coverage.json 顶部记录范围，避免"部分导出被误读为缺失"。
- 验收：`grep -c` 一下 coverage.json 里 missing 非空的程序集，就能回答
  "这棵树全不全"；本案例那种误判可用一条命令证伪/证实。

### P1-C top-up 成为一等公民：`--add` + runs 历史

- `--add`：读目标树根 `MANIFEST.json` + `types.tsv` → 求出 metadata 中"不在树内"
  的程序集 → 只 emit 缺的部分（`--only` 的自动版），既有文件不重写（字节不变
  特性已保证安全）。
- MANIFEST 改为 `runs: [...]` 追加式（`_write_manifest` 读旧 MANIFEST，append 本次
  run，保留历次 `flags.only`/时间戳）；单 run 字段平铺保持向后兼容（取最后一次）。
- 验收：对 v39b21 这类"多次拼成的树"，MANIFEST 能完整回答"这棵树经历了哪几次
  运行、每次范围是什么"。

### P2-D dump-lite.cs（可选）

- 树根合并输出一份声明-only 的 dump.cs 兼容文件（`// Image N:` 分界 +
  `// TypeDefIndex:` 行格式），让工作区既有按 dump.cs 格式写的脚本
  （parse_catalog、md_endpoint_extractor 等）直接吃导出树。
- 成本低（headers.py 已有声明文本），但格式兼容要逐字段核对，故放 P2。

### P2-E 重跑 v39b21 存档

- 以上落地后，用当前 HEAD 对同一 metadata/binary 重跑 `--label v39b21-full`，
  产出第一棵带 MANIFEST + coverage + 索引的完整树，作为回归样例归档；
  旧 v39b21 保留与否由用户定（建议保留至新树验证过）。

## 四、非目标

- 不追求替代 IDA/Il2CppDumper 的全部用途（native 侧分析、script.json 之外的
  Il2CppDumper 专有格式）；目标是把"类型归属/成员清单/方法体/字符串字面量"这
  四类高频查询封闭在导出树内。
- 不改方法体还原质量（那是 fix 系列的主线，与本计划正交）。

## 五、落地顺序与工作量估计

| 顺序 | 项 | 估计 |
|------|----|------|
| 1 | P0-A types.tsv + INDEX.md | 半天（emitter 已有全量 typedef 遍历） |
| 2 | P0-B coverage.json + summary 计数 | 半天~1 天（口径坑在嵌套/编译注入） |
| 3 | P1-C --add + runs 历史 | 半天（_write_manifest 改造 + 过滤求补集） |
| 4 | P2-D / P2-E | 各半天，按需 |

每项独立可交付，合并顺序即上表；gate.py 加对应轻量校验（types.tsv 行数 ==
typedef 数、coverage 总数对账）防回归。
