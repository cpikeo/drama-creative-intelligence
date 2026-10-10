# verification｜随仓库交付的可复现验证

把"这个 Skill 如何被验证"变成仓库内可复现的材料，而不是口头声明。
v7.0.0 的测试制品保留在作者工作区、未随仓库发布（见 CHANGELOG v7.0.0 §4–§6）；
本目录用最小代价重建其中**确定性**的部分，并把**艺术质量**部分交给明确的盲评量表。

## 运行

```bash
bash verification/run_all.sh
```

四步确定性验证 + 一步条件化媒体自检，全部零模型调用、零媒体费用：

1. **仓库完整性（R1–R4）**：frontmatter 与版本一致、Markdown 链接可解析、
   § 章节引用可解析、关键概念保留（`concepts.txt`，防止重构丢能力）。
2. **样例项目安全网（P1–P16）**：`fixtures/project/` 是一个完整、内部一致的
   微型项目（总控 + EP001），逐章对照协议 §1 的固定章节与 §6 的安全网清单。
3. **变异测试**：`fixtures/mutations/` 下 10 个已知缺陷样本
   （承诺跳阶、变更段内箭头、缺固定章节、悬空依据 ID、未观看却通过、
   悬空接缝引用、出点与入点不回指、跨场接缝无依据、物品状态变化无来源、
   动作阶段跨镜重置），每个都必须被对应规则检出。
4. **度量**：`measure.py` 输出字节 / o200k_base token / 规则措辞 / 重复规则句 / 失效链接。
5. **媒体测量层自检**：`media_qa.py --selftest` 用 ffmpeg 生成真实测试媒体
   （参考件 + 响度违规 + 分辨率违规），验证积分响度（LUFS）/ 真峰值（dBTP）/ 规格
   的测量与判定；感官项恒为 NEEDS_HUMAN。无 ffmpeg 时标注未执行（可
   `pip install imageio-ffmpeg` 获得静态二进制）。

另有两套面向"人"的台子（本身不替代人工评审）：

- **`ab_review/`**：双人盲评协议——固定任务 T-AB1（v7.1.0 vs v7.2.0，其历史锚点不在本仓库
  git 历史中，见 [ab_review/README.md](ab_review/README.md)「版本锚点」）与
  T-AB2 / T-C1–T-C7（视觉连续性与角色一致性，v7.2.1 vs v7.3.0，锚点可复现）、评审记录单、
  版本指纹与快照导出（`run_ab.sh`）。详见 [ab_review/README.md](ab_review/README.md)。
- **`media_qa.py --media <文件> [规格参数]`**：对任意真实媒体做确定性测量
  （分辨率 / 时长 / 编码 / 声道 / 积分响度 / 真峰值），逐项给出
  `MEASURED_PASS / MEASURED_FAIL / NEEDS_HUMAN`；响度偏差超 ±0.5 LU 时
  按协议 §6 提示二遍归一化。测量不等于观看，感官项永远待人工。

## 运行包 vs 源码仓库：`verification/` 该不该删？

**结论：源码仓库保留，运行包排除。不要从仓库删除，也不要在创作时加载它。**

### 证据（本轮实测，非推断）

| 问题 | 实测答案 |
|---|---|
| 删掉它，创作 Context 省多少 token？ | **0**。`measure.py` 的计量范围是 SKILL.md + references/（另计 README/CHANGELOG），本来就不含 verification/。`bash verification/pack.sh` 对"仅技能文件"与"完整仓库"同口径测量，结果逐项相同（15,320 tok / 常驻 6,025 tok / 故事向 11,490 tok）。 |
| 创作路径依赖这些脚本吗？ | **不依赖**。`grep -n "lint\.py\|media_qa\.py\|run_all\.sh\|measure\.py" SKILL.md references/*.md` 无命中：技能文件从不命令创作时运行它们。MEDIA QA 的验收要求（响度以测量值验收、±0.5 LU、二遍归一化）写在协议 §6，不依赖脚本存在。 |
| 技能文件引用 verification/ 吗？ | **不允许**。原 SKILL.md §6 有一条指向 `verification/README.md` 的链接（发布包里会变成死链）；已改为文字说明，并由新增的 **R5** 机器看住：技能文件再链接 verification/ 即 FAIL。 |
| verification/ 依赖技能文件吗？ | 反向依赖存在（`lint.py --repo` 读 SKILL.md 做 R1–R5），但是**单向**的：技能文件不依赖它，因此它可以整体移除而不破坏创作包。 |
| 它占多少？ | git 跟踪 46 个文件 / 226,620 B（整个仓库 pack 149 KiB）；另有约 24.9 MB **未跟踪生成物**（`media_selftest/assets/` 的 3 个测试 mp4、`ab_review/snapshots/`），已在 `.gitignore`，clone 不携带。 |
| 删了会失去什么？ | 回归测试（lint + 10 个变异）、Token 与重复度量、A/B 盲评台、媒体测量自检。**这些是改动技能包后唯一的回归保障**——没有它们，"优化"只能靠自评。 |

### 怎么做

```bash
# 生成运行包（只含 SKILL.md + references/，自洽、无包外链接、可独立分发）
bash verification/pack.sh                 # 输出 dist/skill-runtime（不入库）

# 源码仓库继续随 verification/ 一起维护；改动技能包后回归：
bash verification/run_all.sh
```

`pack.sh` 校验四件事：文件集恰为 4 个技能文件、不含 verification/、无指向包外的链接，
并打印与完整仓库同口径的 token 对照。

### 分界

| 位置 | 内容 | 何时需要 |
|---|---|---|
| 运行包 | `SKILL.md` + `references/`（4 个文件） | 每次创作 |
| 源码仓库 | 上述 + `verification/` + `README.md` + `CHANGELOG.md` + `LICENSE` | 维护、改规则、发版本 |
| 按需取用 | `verification/rubric.md`（质量盲评）、`verification/media_qa.py`（有媒体且要测响度/规格时） | 评测与媒体验收场景 |

`rubric.md` 与 `media_qa.py` 是唯一两个"创作周边"工具：前者用于质量评测而非逐集创作，
后者用于有真实媒体时的技术测量。两者都不进创作 Context；需要时从源码仓库取。

## P 规则与协议安全网的对应

| 规则 | 协议依据（director-memory-continuity.md §6「安全网」） |
|---|---|
| P1 | 集文件固定章节，缺章节即未完成 |
| P2 | 承诺逐级推进、不跳阶；承诺账与集内推进一致 |
| P3 | 变更记录六段链，段内不用箭头 |
| P4 | 前因逐条引用上集出去压力的 ID；Snapshot Diff 引用可追溯 |
| P5 | 对白依据为 ID，且被所属镜头的连续性依据覆盖 |
| P6 | ID 前缀合法、节点不重复定义 |
| P7 | 未实际观看 / 聆听的媒体不得通过；QA 结论取值合法 |
| P8 | 进入生成的镜头须有三块规格（IDENTITY / STATE / SHOT） |
| P9 | 镜头被光态与时间状态表覆盖 |
| P10 | 道具有位置与持有链 |
| P11 | 每镜有职责（主功能） |
| P12 | 每镜有连续性依据 |
| P13 | 跨镜接缝：入点/出点齐备、引用存在、出点与入点双向回指 |
| P14 | 跨场接缝须声明转场性质或事件依据（跨镜变化须有出处） |
| P15 | 接缝中的物品状态变化须挂 `EVENT-`/`CHG-`/`DEC-` 来源 ID（无来源的物品变化不成立） |
| P16 | 入点/出点须写明动作阶段；出点未完成的动作，下一镜入点须承接同一阶段 |

lint **不覆盖**的条款（需人工或媒体工具）：接缝的视觉对齐（位置、视线、方向、景别与透视、
光态的实际画面）、物品是否真的还在原处、动作是否真的有过程、时长闭合、表演可读性、
VO 信息权限、响度测量、听感、盲评艺术质量——分别见 `rubric.md`、
[ab_review/task_continuity.md](ab_review/task_continuity.md) 与各 QA 清单。
P13–P16 只能证明连续性**被写下、有来源、可追溯**，不能证明画面真的接上了；
后者必须真实观看连续画面或成片。多段生成的接续帧一致性同样只能在媒体层复验。

## 质量评价

原创性、戏剧张力、人物可信度、视听意图、情绪穿透力等无法机器化的维度，
一律使用 `rubric.md` 做双人盲评，不得以关键词命中率代替。

## 结果记录

- `results/` 保存每次 `run_all.sh` 的度量 JSON；最新一次人读记录见
  [results/latest_run.md](results/latest_run.md)。
- 历史上 v7.0.0 声称的 T1–T4 测试（含真实媒体与粗剪）制品未随仓库交付，
  其媒体与听感结论在本仓库内**不可复现**，不作为已验证能力；
  本目录只交付并记录本仓库内实际执行的确定性验证。
