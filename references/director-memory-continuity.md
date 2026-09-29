# 导演记忆、World State、Continuity Graph、生产与创意 QA

这一份协议就是 Director Core 的持续记忆模型。它取代分散的角色表、资产表、连续性表、阶段摘要、任务缓存和 Agent 交接。事实只写一次；Context 只加载解决当前决定所需的节点与历史。

## 1. 三层项目真相

```text
<项目>/
├── 创作总控.md               # Director Memory：Bibles、Canon、Graph、全剧 Intent、分集 Snapshot
├── 剧集/EP001.md              # 本集事实：剧本、状态变化、分镜、声画规格、剪辑、QA
└── 制作/EP001/                # 真实参考、任务预览、生成媒体、导出和运行观察；不冒充 Canon
```

小项目可只保留总控加一集文件；不预建空集，不按岗位拆文件。`创作总控.md` 是 Memory，不是把全剧内容复制进去的百科；只保存下游会依赖的可追溯事实与未决线索。

| 记忆域 | 权威内容 | 不能放进这里 |
|---|---|---|
| **World Bible** | 时代、地点、势力、规则、资源、环境、空间可见事实 | 当前单镜姿态或无依据推测 |
| **Character Bible** | Character DNA、稳定身份、关系基线、弧线历史 | 每集重复情绪描写 |
| **Visual Bible** | 媒介、时代锚点、视觉方向、资产身份、连续性锁、声音身份 | 单镜瞬态或生成文件路径 |
| **Narrative Canon** | 已确认事实、时间线、来源定位、信息权限、改编边界 | 临时想法与未验证假设 |
| **Events / History** | 已发生事件、因果、不可逆后果 | 尚未发生的剧情 |
| **Relationships** | 双方立场、知识、债务、承诺、权力与变化历史 | 没有证据的“人物设定” |
| **Foreshadowing / Promise** | 建立位置、观众权限、预期回收条件、当前状态 | 已忘记的装饰细节 |
| **Assets** | 人/地/物身份、变体、状态、参考范围、权利信息 | 逐镜动作脚本 |
| **Directorial Intent** | 观看承诺、情绪、节奏、信息释放、视听策略、禁区/例外 | 冒充已发生的故事事实 |

## 2. Canon、State、History、Promise、Intent、Hypothesis

| 类型 | 定义与变更条件 |
|---|---|
| `CANON` | 已确认、可引用的既定事实。仅由来源证据、创作者确认或显式 retcon 变更；由媒体观察导出的事实还必须走完 `MEDIA QA → DEC-H`。 |
| `STATE` | 当前时点真实有效的可变事实。每次改变必须有触发事件、前后状态与生效范围。 |
| `HISTORY` | 已发生事件及后果；除明确 retcon/主观叙事例外外不可悄悄消失。 |
| `PROMISE` | 已建立且未回收的伏笔、悬问、关系债、威胁、视觉/声音承诺。状态为 `Seeded / Activated / Pressured / Narrowed / Redefined / Fulfilled / Abandoned`；回收、转义或放弃均需明确。 |
| `INTENT` | 导演如何让观众观看/感受/暂未知晓；可变但不能伪装为世界事实。 |
| `HYPOTHESIS` | 支撑当前设计的临时推断，附依据、置信与验证点；未验证前不进入 Canon。 |

任何记录应能回答：谁/什么、在哪/何时、为什么成立、从何而来、与谁有关、何时生效、何时终止、影响什么。冲突出现时，先检查类型和来源，再决定是状态变化、信息误导、主观画面、创作者 retcon 还是错误；不以新 prompt 覆盖旧记录。

### Director Decision、Evidence 与 Causal Memory

决定分两档：`DEC-L` 是可逆、仅影响当前场/镜/规格的局部取舍，可附在剧集或镜头；`DEC-H` 会改变 Canon、State、Character DNA、Promise、成本或跨集范围，必须留在权威记忆。普通措辞和微调不记录。每条 `DEC-H` 使用：

`Evidence → Context → Alternatives → Trade-off → Decision → Consequence → Verification`

`Evidence` 记录 `ID / Type / Source / Confidence / Usable for`：类型仅为 `USER / CANON / HISTORY / MEDIA / QA / HYPOTHESIS`，来源定位到创作者指令、文件、镜头或时间码，置信为 `Confirmed / Observed / Inferred / Unverified`，并说明它能支持什么、不能支持什么。`Alternatives` 只列真实可行且后果不同的方向；`Verification` 指向具体场、镜、媒体或后续 Snapshot。

相应因果条目使用：

`Choice → Event → State Delta → Consequence → New Constraint → Future Pressure`

生成文件和模型输出可作为 `MEDIA` 或 `QA` Evidence，但永不自动晋升为 Canon/State。其可见细节只证明该文件中可见；要晋升为新世界事实，必须经过 `真实媒体检查 → MEDIA QA → DEC-H → Canon/State`。模型补全、单镜可见和技术成功都不能越过此门。

## 3. World State 与 State Snapshot

### World State

按需维护以下可演化节点：

`时间/时代 · 地点/空间 · 势力 · 规则 · 资源 · 事件 · 关系 · 角色 · 道具 · 环境`

每个节点只留会影响行动、风险、信息、画面、声音或后续因果的字段。空间区分“可见事实 / 有依据推测 / 未知区域”；未知背面、精确尺度、隐藏门或产品细节不得为镜头方便虚构。

### 每集 Snapshot

每集开头读入、结尾写出同一张状态卡：

```text
EP### State Snapshot
前因：上集及更早仍在生效的事件/承诺
当前状态：世界、角色、关系、资产、时间/环境、观众知识
本集变化：谁因何事从什么变到什么
后果：已落地、不可逆或将限制下一行动的结果
未决线索：PROMISE、风险、误解、资源/信息缺口及预期责任
```

此卡是下一集的直接入口，不是剧情摘要。新集先继承它，再推演本集；结尾同时保留最小 `Snapshot Diff`：只列新增/改变/移除的节点、边和 Promise 状态，避免复制整张状态卡。若新剧本违背 Snapshot，必须写出事件、回忆、蒙太奇、时间跳跃或 retcon 的桥，而不是默默覆盖。

## 4. Continuity Graph 与 Character DNA

Continuity Graph 不需可视化软件，但应以稳定 ID 表达节点和关系：

- 节点：`CHAR`、`LOC`、`PROP`、`EVENT`、`REL`、`PROMISE`、`ASSET`、`SHOT`、`MEDIA`；
- 边：`causes`（导致）、`changes`（改变）、`limits`（限制）、`enables`（允许）、`knows`（知道）、`believes`（相信）、`holds`（持有）、`owes`（亏欠）、`promises`（承诺）、`fulfills`（回收）、`contradicts`（冲突）；空间/可见性/依赖是其受控属性，不另造平行关系词；
- 每条边带来源、起止状态和生效范围，必要时带观众是否已知。面对一个决定，应能反查它会 `changes` 什么、`limits`/`enables` 谁、压迫或回收哪个 Promise。

Character DNA 统一为：`Identity + Psychology + Visual DNA + Relationship + Arc State`。角色状态涵盖外貌/服装/伤痕/能力/道具、情绪/立场/知识、位置/朝向/持物、声音身份与弧线阶段。改变必须写：

`角色/关系：变化前 → 触发事件/选择 → 代价或结果 → 变化后；生效镜/集；下游影响`

同一规则用于道具、地点、天气、光态、画内文字和声音。相邻镜检查，也检查远距离因果：早期交出的物件、获得的知识、留下的伤痕或未兑现的承诺不能在后集凭空恢复或消失。

## 5. Context 读取、ID 与修改传播

Context 按任务切片加载：

`当前任务 → 相关 Canon/Intent → 上集 Snapshot → 相关角色/资产 → Graph 邻接 → 未兑现 Promise → 当前媒体`

读取目标是解决当前 Director Decision，不是复述整季。先从直接节点开始；当已有足够 Canon、State、人物动机、因果与制作限制来做决定时停止扩展。只有证据不足、因果跨越、人物行动无因、Promise 无法承接、资产状态不明或状态冲突时才扩展到相邻依赖。不要将所有角色、所有资产、全文剧本或历史媒体塞入 Context。

ID 表示同一实体、事件或叙事职责而非行号：`CHAR-`、`LOC-`、`PROP-`、`EVENT-`、`REL-`、`PROM-`、`VAR-`、`LOCK-`、`SC-`、`SH-`、`GEN-`、`CUT-`。润色/小改 prompt 不换 ID；真正拆并实体、事件或镜头才记录替代关系。

变更记录：`变更 ID / 类型 / 旧→新 / 依据或事件 / Graph 影响 / 已刷新 / 待刷新`。只将受影响下游标为 `stale`：

| 变化源 | 至少重查 |
|---|---|
| Canon、世界规则、人物动机/关系、信息权限 | Snapshot、相关剧本/状态、镜头信息释放、声音、媒体 |
| Character DNA、资产身份/锁、环境状态 | 相关变体、关键帧、提示词、参考、后续镜与媒体 |
| 场景行动/对白/画内文字/声音 | 分镜、关键帧、视频/TTS/字幕/音乐、剪辑 |
| 镜头边界/时长/构图/声音 | 关键帧、视频规格、参考、剪辑/续接 |
| prompt/模型/参考/参数 | 预览、未运行任务、相关媒体与后续续接 |
| 已生成媒体/剪辑观察 | 剪辑与 QA；必要时回到规格、分镜、剧本或 State |

变更按 `Change → Dependency Graph → Stale Scope → Recheck` 执行。`stale` 代表重新判断范围，**不代表必须重生成**：先 `Re-read → Re-plan → Reuse → Edit → Regenerate`。只有缺陷破坏 Identity、Canon、State、核心动作、必要信息、情绪意图或交付可用性时才重拍/重生；可由剪辑、裁切、叠字、色声修整或局部编辑解决的不得重投。用户要求同步时才递归刷新至规格/QA，且永不自动重投有成本任务。

## 6. Presentation 作为 Director Memory 的派生视图

项目提案、世界观手册、Lookbook、角色册、分镜展示、发行封面和 deck 只消费同一份 Canon、State、Character DNA、Visual Bible 与 Intent。它们不能维护第二份人物设定、资产清单、视觉方向或故事时间线。

页面可用 `P-` ID 记录，但它不是新 Context。每个页面绑定其主张、引用的 Canon/资产/媒体、唯一焦点、信息层级、媒体用途与交付状态；页面表达的变更不影响故事。Canon、Intent、Character DNA、资产或媒体一变，引用它们的页面自动标为 `stale` 并按需刷新。

Presentation 的真实图片/视频、图表、字体、来源、版权/肖像、导出文件和可读性观察仍放在 `制作/` 的对应交付范围；不能用 deck 文件名、缩略图或设计说明冒充已检查的媒体/授权事实。

## 7. 真实媒体、生产边界与创意 QA

| 标记 | 含义 |
|---|---|
| `FACT` | 已确认 Canon/State/Intent 事实，可作为下游约束。 |
| `REF` | 真实可读、内容/用途/授权已检查的输入。 |
| `PLAN` | 用户将在外部界面挂载或提供的计划，不能冒充项目文件。 |
| `GEN` | 已写出的图像/视频/TTS/音乐规格，尚未生产。 |
| `MEDIA` | 已生成/导入的真实文件，可检查/剪辑，尚不等于质量通过。 |

每个 `REF/MEDIA` 写相对路径、来源/授权、用途（身份/造型/地理/构图/起始/结束/风格/声音）、控制/不得控制范围与实际检查内容。

每次外部生产：**精确任务（模态、数量、规格、参考、参数、输出、成本/授权）→ 展示预览 → 创作者本次明确确认 → 执行 → 检查真实媒体 → 更新 Memory**。任一当前 State、prompt、参考、参数或输出变化均令旧确认失效；中断任务先收集/检查已提交结果，不盲目重投。

QA 分三层并按顺序进行：`SPEC QA` 审故事/人物、Canon/State/Graph 和分镜/生成规格；`MEDIA QA` 审实际图像、视频、声音、授权与技术可用性；`CUT QA` 审连续观看的剪辑、节奏、色声接缝与交付体验。实际观看时再以 `Intent → Attention → Information → Emotion → Expectation` 复核：导演意图是否被观众注意到，必要信息是否被接收，情绪是否由行动/视听产生，下一步期待是否兑现或有意延迟。每层结论为 `APPROVE`、`APPROVE_WITH_NOTES`、`REVISE` 或 `PROVISIONAL`；未观看/聆听实际媒体时，`MEDIA QA` 与 `CUT QA` 必须为 `PROVISIONAL`。每个问题提供位置、事实/可见证据、观众或制作影响、最小修复、责任层和保留项。

在导演判断前做最小 Continuity Lint：ID 是否唯一可追溯；是否继承上集 Snapshot；道具是否有位置/持有者转移链；时间/光态是否连续或有例外；角色是否按当前知识行动；每镜是否有职责；时长是否闭合；未检查媒体是否标 `PROVISIONAL`。Lint 是安全网，不替代导演判断。
