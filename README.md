# Director-Level Drama Creative Intelligence · 总导演宪法版 · v6.1

一个**总导演、一套创作大脑、一套持续记忆、一个世界状态、一张因果图谱、一条完整生产链**。
它不是多 Agent 岗位拼装、剧本模板、提示词库、网站模板、UI Design System 或组件库。唯一创作中枢是 **Creative Director / Director Core**，统一 Story、World、Character、Visual、Storyboard、Image、Video、Sound、Edit、Continuity、Production、QA 与按需的 Presentation / Editorial Art Direction。

## 完整能力链

```text
Understand → Remember → Reason → Decide → Direct → Generate → Verify → Update Memory
理解 → 回忆 → 推理 → 决策 → 执导 → 生产 → 验收 → 记忆更新
```

- **Director Intelligence**：关键问题以 `Evidence → Context → Alternatives → Trade-off → Decision → Consequence → Verification` 主动取舍；`DEC-L` 承担可逆局部取舍，`DEC-H` 承担会影响跨集真相的持久决定。
- **六种真相**：`CANON / STATE / HISTORY / PROMISE / INTENT / HYPOTHESIS` 一处定死（SKILL §02），变更条件显式；Promise 使用 `Seeded → Activated → Pressured → Narrowed → Redefined → Fulfilled / Abandoned` 生命周期。
- **Evidence Boundary**：每项证据带 `ID / Type / Source / Confidence / Usable for`；生成媒体只能先作为证据，媒体事实必须经 `真实媒体检查 → MEDIA QA → DEC-H` 才能晋升 Canon/State，永不自动污染。
- **Causal Memory**：所有有后果的行动遵循 `Choice → Event → State Delta → Consequence → New Constraint → Future Pressure`，让今天的选择持续限制明天的人物、关系、资源与 Promise。
- **Character DNA 六层**：`Identity + Psychology + Visual DNA + Voice DNA + Relationship + Arc State`；关键行动先过行动门 `Want → Know → Leverage → Pressure → Choice → Cost → visible Action`；配音参数是连续性锁（LOCK）；任何变化记录 `变化前 → 触发事件/选择 → 代价或结果 → 变化后 → 生效范围 → 下游影响`，无事件、因果与生效范围的变化不成立。
- **跨集控制**：World State、State Snapshot、最小 Snapshot Diff、Character DNA 与 Continuity Graph 共同约束下一集；图谱以十类稳定 ID 节点与十一词受控边词汇推演后果。
- **最小 Context / 最小调用**：只加载当前任务所需的 Canon/Intent、Snapshot、角色/资产、Graph 邻接、Promise 与媒体，足以判断即停；一次判断能解决的不拆层；能从既有记忆判断的不重读；规格批量、确认批量；未变化产物不重验；变化后只在 stale 范围重查。
- **变化与复用**：`Change → Dependency Graph → Stale Scope → Recheck`；`stale` 只要求重新判断，优先 `Re-read → Re-plan → Reuse → Edit → Regenerate`；仅当核心身份、事实、动作、信息、情绪或交付受损才重投。
- **导演级生产与验收**：外部生产走 精确预览 → 本次明确确认 → 执行 → 真实媒体检查 → 记忆更新；`SPEC QA / MEDIA QA / CUT QA` 按序审文本、真实媒体与成片，未观看必为 `PROVISIONAL`；实际体验以 `Intent → Attention → Information → Emotion → Expectation` 与高画质基线验收；商业级完成度 = 交付物按媒介交付规格直接可用。
- **按需 Presentation Intelligence**：故事圣经、Lookbook、提案、角色册、分镜展示、发行物与 deck 使用同一记忆派生，不另立真相。

## 运行架构

```text
drama-creative-intelligence/
├── SKILL.md                              # 总导演宪法：Director Core、六种真相、DNA 六层与因果图谱、能力链、Loop、生产与 QA、交付
├── README.md                             # 本说明与 v6 减法审计
├── LICENSE                               # Apache-2.0
└── references/                           # 按需加载的专业知识层（SKILL 头部有任务→章节加载矩阵）
    ├── creative-direction.md             # 导演判断手册：故事、Character DNA 六层判断、对白与 VO、电影语言（含表演/真实光影/高画质基线/美学锚点）、一致性三件套、声画规格编译（含声音圣经/分媒介镜头语法）、剪辑
    ├── director-memory-continuity.md     # 记忆操作层：三层项目真相、角色分层与系列承诺账、Evidence Boundary（含视点时间）、Snapshot 与每集状态表、图谱操作（随剧本写入/写场前反查）、生产与 QA 执行（批次/升级/追踪/锚点/分模态清单）
    └── presentation.md                   # Presentation 手册（仅按需）：判断链、工艺、P- 页面记录与 stale
```

**单源真相**：六种真相定义、Character DNA 六层与变化规则、角色分层判据、因果链、图谱节点与边词汇、QA 三层结论、生产门与批次/升级规则均只固定于 SKILL；references 只深化判断（creative-direction）、固定操作（director-memory-continuity）或承载纯按需内容（presentation），不重新定义。

## v6 减法审计（删除 > 合并 > 简化 > 复用 > 新增）

**删除（重复定义与二次复述，19 处 → 0 处）**：

| # | 被删的重复 | v5 位置 |
|---|---|---|
| 1 | 六种真相定义表（整表） | memory §2（SKILL §02 升为唯一权威表） |
| 2 | Director Intelligence 决策链 | memory §2 |
| 3 | Causal Memory 因果链 | memory §2 |
| 4 | Character DNA 公式（两处） | creative-direction §2 开头、memory §4 |
| 5 | 行动门（一遍） | creative-direction §2 |
| 6 | QA 三层定义（两遍：层名/顺序/结论/PROVISIONAL） | creative-direction §5 尾段、SKILL §07 长段（宪法压缩入 §05-7） |
| 7 | stale 链与重生成阈值（一遍） | memory §5 尾部复述 |
| 8 | 生产门（两遍：完整流程表述） | SKILL §07、memory §7（宪法压缩入 §05-6） |
| 9 | 媒体晋升门（一遍完整表述） | SKILL §07 |
| 10 | Presentation 判断链与声明（一遍） | creative-direction §6 开头声明段 |
| 11 | 图谱边词汇（一遍） | memory §4 |
| 12 | Snapshot 五字段（一遍） | SKILL §03 行内 |
| 13 | Context 切片链（一遍） | SKILL §05-2 行内枚举 |
| 14 | World State 节点列表（一遍） | memory §3 |
| 15 | “Character 优先于 Appearance”口号（一遍） | creative-direction §2 标题 |
| 16 | 8 步循环的错位中文副行（12 词对 8 步） | SKILL 与 README 头部 |
| 17 | README 对不存在 `NOTICE` 文件的引用 | README |
| 18 | 图谱节点类型与 ID 前缀两套不一致（MEDIA/ASSET 无 ID；SC/GEN/CUT 有 ID 非节点） | memory §4/§5 |
| 19 | 变更记录字数不统一（CD 与 memory 各 5 词且措辞不同、均缺“下游传播”） | CD §2、memory §4 |

**合并**：memory §6“Presentation 派生视图”并入 §5 修改传播（`P-` ID 与 stale 规则）；视觉/声音资产、配音参数锁并入 Visual Bible/Assets 记忆域与变化源表；高画质基线一份标准两用——既是 §4 规格编译的生成目标下限，又是 `MEDIA QA` 的验收线；同一变化规则同时覆盖人物/道具/地点/天气/光态/画内文字/声音七类实体。

**简化**：SKILL.md 每条规则给唯一家、references 不再互相印证；按需加载从“两份文件全读”收紧为“按阶段读一份、按任务读章节”；循环八步每步压到可执行粒度并指向唯一操作层。

**数字**（UTF-8 字节）：

| 口径 | v5 | v6 | 变化 |
|---|---|---|---|
| SKILL.md（常驻加载） | 18,259 | 18,472 | +1.2%（若扣除本审计“新增”列内容：15,972，**−12.5%**） |
| creative-direction.md | 9,439 | 13,688 | +45.0%（全部为下节用户指定的新增智能层） |
| director-memory-continuity.md | 12,648 | 11,099 | **−12.2%** |
| 三文件正文合计 | 40,346 | 43,259 | +7.2%（纯减法口径：**−10.4%**） |
| 重复规则站点 | 19 | 0 | **−100%** |
| 单任务 Context（生产阶段，SKILL+所需 references） | 40,346 | 32,160 | **−20.3%** |

**调用（结构级削减）**：最小调用原则（一次判断一次调用、规格/确认批量、未变化产物不重验、变化后只 stale 范围重查、不自动重投有成本任务）+ Snapshot 继承（每集不重新理解整个世界）+ 确认失效规则（仅 State/prompt/参考/参数/输出变化才重走确认）。这些规则把重复读取、重复验证与盲目重投压到最小，是调用量下降的结构性来源。

**新增（仅带来新智能价值，全部对应需求项）**：

- **Voice DNA**（新 DNA 层）：音色、语速与节奏、口吻、呼吸、情绪化声表现、固定配音参数（TTS 音色 ID 为 `LOCK`）、口头禅与称呼；
- **Behavioral Strategy**：“行为先看常设策略再看当下情境”+ 策略升级必须完成 Arc State 过渡；
- **Arc State** 六阶段判断：处于哪一阶段、依据什么因果、下一个事件推向什么；
- **表演**子章节：微表情链、心理外化、走位、节奏、反应镜头价值；
- **真实光影**强化：光必须有动机、同场同段一致、光态是 STATE 进 Snapshot；
- **统一影像语言**：一部 Visual Bible = 一套影像语言，单集 look 变化必须事件/意图 + `DEC-H`；
- **高画质基线**：光学行为/皮肤质感/解剖稳定/几何一致/文字可读/无 AI 漂移/光影连续，7 条下限；
- **反伪电影感黑名单**：宽黑边、颗粒、霓虹暗黑、伪光学特效、无意义运动/升格/变速、罐头配乐；
- **最小调用原则**（§01）；
- **商业级完成度基线**（§07）；
- **媒介形态 × 交付形态一等决定**：静态漫剧/动态漫/图生视频/文生视频/拟真实拍风 × 短剧/剧集/广告/电影，契约期定档。

**停止减法的边界**：六种真相表、行动门、边词汇、Snapshot 卡、stale 表与 QA 三层不再进一步削减——每一项承担唯一职责（定义、人物逻辑、因果、跨集入口、变化边界、验收），再减会直接损害连续性、可追溯性与创作智能。总量 +7.2% 的 100% 来自上列新增；若不计新增，纯减法后总量 −10.4%、重复规则 −100%、单任务 Context −20.3%，质量不降。

## v6.1 操作化补全（P0–P2）

v6 解决"定义层单源"，v6.1 解决"承诺 → 执行"断层：把已有承诺接到生产流水线上。**不新增任何定义层概念**，全部落在按需层（宪法仅 +5 条条款级规则与加载矩阵）。

**P0（生产会翻车的缺口）**

| # | 补什么 | 落点 |
|---|---|---|
| 1 | 角色分层 A/B/C（判据 + 记录格式）：A=六层 DNA+全 LOCK+参考图；B=四字段；C=不进记忆，跨集升 B | 判据 SKILL §03；记录格式 MC §1 |
| 2 | 视觉一致性三件套：定妆参考图（REF 锁）、DNA→prompt 块（IDENTITY/STATE/SHOT 三块拼装，禁自由描述）、负面锁（do-not 清单为 LOCK） | CD §4 |
| 3 | 图谱两个程序：剧本定稿必须同步写图谱增量（边记录格式）；写场前反查 knows/holds/owes/promises + State，写入镜头规格"连续性依据"栏 | 条款 SKILL §03；格式与清单 MC §4 |
| 4 | 生产经济学：批次 3–5 镜/批 + 批内系统缺陷先修共同原因；同镜连续失败 2–3 次停止重投、升级 DEC-H | 条款 SKILL §05-6；细则 MC §6 |
| 5 | 美学锚点：3–6 张认可 REF 剧照声明锚定维度，MEDIA QA 第一项 = 与锚点比对；无锚点不得按通过处理 | 建立 CD §3；验收 MC §6；SKILL §05-7 一句 |

**P1（执行完备性）**

| # | 补什么 | 落点 |
|---|---|---|
| 6 | 生产追踪表（任务×模态×批次×状态×QA 结论），跨会话断点与恢复点 | MC §6 |
| 7 | 每集时间/地点/光态表（关键帧/视频/声音规格按行引用的单一源） | MC §3 |
| 8 | 分模态 QA 清单（图像/视频/TTS/音乐逐项勾选） | MC §6 |
| 9 | 对白与 VO：一句线一件事（默认砍 30%）、潜台词、对白经济、VO 只带视点人物所知 | CD §2 |
| 10 | 系列承诺账 + 两条定律（出去压力→进入压力；回收漂移必记 DEC-H） | MC §1 |
| 11 | 视点时间字段：闪回/梦境/想象是视点，不写 State，揭示信息进 knows 边 | MC §2 |
| 12 | 分媒介形态镜头语法/运动预算表（静态漫/动态漫/图生/文生/拟真） | CD §4 |
| 13 | 声音圣经（环境声锁/动机锁/响度目标/SFX 身份）+ TTS→视频生产顺序为 DEC-H | CD §4 |

**P2（工程化）**

| # | 补什么 | 落点 |
|---|---|---|
| 14 | 自检三场景（见下节） | README |
| 15 | 任务→章节加载矩阵（Remember 步机械可执行，替代粗触发） | SKILL 头部 |
| 16 | Presentation 拆为独立按需 reference（常规漫剧生产不再携带 ~2.9KB） | references/presentation.md |
| 17 | IP 提示词卫生（prompt 不出现受保护作品名/角色名）+ 契约补目标平台/时长/画幅/内容红线 | CD §4；SKILL §04 |
| 18 | QA 记录位置显式化（剧集文件 QA 节）+ PROVISIONAL→APPROVE 升级路径 | MC §6 |

**v6.1 数字**（UTF-8 字节）：SKILL 18,439→19,693（+6.8%，= 任务加载矩阵 + 5 条条款级规则）；CD 13,688→15,264（+11.5%，全为 P0-2/P1 机制）；MC 11,052→15,027（+36.0%，全为操作协议）；presentation 新增 2,889（从 CD/MC 移出 3,200，净变化 ≈ −300，且常规任务不再加载）。**单任务 Context 反而下降**：加载矩阵把"整份 reference"收紧为"任务→章节"，生产任务最坏情况 35.0KB（v6 为 43.2KB，−19%），严格按章节读则 23–28KB（−35~−47%）。

## 自检（三个验收场景）

技能跑起来后，用以下场景验证"承诺是否落地"。任一检查项不过 = 技能执行缺陷，不是故事缺陷。

**场景 A：第一集包完备性**（输入：一句话创意）
- [ ] 创作契约含媒介形态、交付形态、平台/时长/画幅/内容红线
- [ ] A 级角色六层 DNA 完整（含 Voice DNA 的 TTS 音色 ID/参数锚点）；B 级角色仅四字段
- [ ] 每个 A 级角色有定妆参考图计划（REF）与 IDENTITY/负面锁记录
- [ ] Snapshot 卡五字段齐全；每集状态表已建；图谱边数 ≥ 场景数且每条边带来源
- [ ] 每镜规格由三块拼装（无自由描述）；视觉圣经含美学锚点（或显式声明"无锚点"）

**场景 B：跨集继承**（输入：已验收 EP001，写 EP002）
- [ ] EP002 从 EP001 Snapshot 继承（非重猜世界）；EP001 出去压力出现在 EP002 前因
- [ ] EP001 埋设的伤痕/物件/知识在 EP002 相关镜头规格中按行引用
- [ ] 系列承诺账中相关 PROMISE 状态推进（Seeded→Activated 等）
- [ ] 写场前反查记录可见（连续性依据栏非空）

**场景 C：变更传播**（输入：已验收 EP001，修改其中一条 Canon）
- [ ] 变更记 `DEC-H`，含依据/牺牲/下游影响/验证方式
- [ ] stale 范围正确（按 MC §5 变化源表）；未点名下游被标 stale 而非静默
- [ ] 剧本定稿后图谱增量同步更新；受影响媒体标 stale 且未自动重投

## 使用方式

```text
从一句话开发 8 集 9:16 动态漫剧：替人收拾残局的实习生，
在公司直播事故中发现所有人的“好意”都指向同一份伪造数据。
以 Director-Level Drama Creative Intelligence 建立 World/Character/Visual Bible、Narrative Canon、
Character DNA（含 Voice DNA 配音参数锚点）、伏笔、EP001 Snapshot 和 Continuity Graph，
再完成可生产的第一集。不要套身份反转模板；先让观众看见她的旧策略失效。
```

```text
继续 EP004：读取上一集 Snapshot、与女主有关的 Character DNA、PROMISE 和 Graph 邻接节点，
推演父亲雨夜出现后她的关系和资产状态。她不原谅父亲，但替他撑一次伞。
更新剧本、状态、分镜、声画规格、剪辑和下一集 Snapshot；列出需要补拍的媒体，不要自动投产。
```

```text
基于已接受的 Canon 和 Visual Bible，为制片方制作一份项目 Lookbook 与 10 页合作提案。
先确定 Audience、Objective、Message 和 Insight；每页只保留一个视觉重心，
只使用能证明故事、世界、角色或制作价值的剧照/图表/资产。页面表达不能改写世界事实。
```

## License

Copyright 2026 **drama-creative-intelligence Contributors**.

Released under the [Apache License, Version 2.0](LICENSE). 若日后加入受自身 notice 约束的第三方材料，其要求的署名必须在再分发前补入。
