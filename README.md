# Director-Level → Author-Level Drama Creative Intelligence · v7.2.0

一个导演级与作者级的剧集创作智能。以唯一的创作总监为中枢，维护跨集记忆、世界状态、角色 DNA（含声音）与因果图谱，用同一套判断完成故事、人物、镜头、声音、生产与验收，让每一集都建立在前集的真实后果之上。

它不是多 Agent 岗位拼装、剧本模板、提示词库或网站模板。

## 能做什么

- **从任何入口开始**：一句话、授权原著、既有剧本、分镜、已生成媒体或粗剪，都能在最短有效动作后进入创作或修复。
- **先决定该有什么**：作者级生成（创意发动机、审美世界观、原创性、情绪架构）先于剧本；六类导演智能再裁决对错。
- **电影级视觉统筹**：一句话视觉主张、艺术方向（时代质感/材质/视觉层级）、电影摄影（画幅/曝光/透视/运动）、视觉特效与合成判断，拒绝无动机炫技。
- **跨集不失忆**：六种真相（CANON、STATE、HISTORY、PROMISE、INTENT、HYPOTHESIS）分开存放；Snapshot 让下一集从上集的真实后果开始。
- **角色与声音一致**：角色 DNA 六层（含 Voice DNA 与配音锁 LOCK）、行动门与变化规则，防止身份漂移。
- **变化只重查受影响的部分**：按依赖 ID 的闭包传播；`stale` 不等于重生成，能编辑的不重投。
- **生产可追溯**：能力声明（设计、执行、验证分开）、按批次授权、失败归因与最小修复。
- **真实媒体验收**：SPEC / MEDIA / CUT 三层 QA；没有观看或聆听的部分明确标 `PROVISIONAL`。

## 怎么用

把下面的请求直接交给支持本 Skill 的智能体：

```text
从一句话开发 8 集 9:16 动态漫剧：替人收拾残局的实习生，
在公司直播事故中发现所有人的“好意”都指向同一份伪造数据。
先建立创作契约、创意发动机、Bibles、Canon、A/B 级 Character DNA（含配音锁）、承诺账，
再完成 EP001 的剧本、镜头卡、对白表（含 voice_id 与依据 ID）、Snapshot 与图谱增量。
先让观众看见她的旧策略失效，不套身份反转模板。
```

```text
继续 EP002：读取 EP001 的 Snapshot、相关角色 DNA、承诺账与图谱邻接，推演 EP002。
输出剧本、镜头卡、对白表、变化记录、道具持有链、承诺状态，以及下一集 Snapshot Diff。
```

```text
我修改了 EP001 的一条事实：……
请计算受影响范围：只列引用该 ID 的候选，逐条判为 Re-read / Edit / Regenerate / 无需动作。
```

## 能力声明（每个项目填写一次）

模板与规则见 [SKILL.md §5](SKILL.md)：设计 / 执行 / 验证分开记录；执行为"无"的模态停在 GEN；
听不了的模态，其相关验收项保持 `PROVISIONAL`。

## 仓库结构

```text
SKILL.md                                    宪法：判断、记忆、角色、作者级生成、生产与验收
references/creative-direction.md            导演判断手册：故事与因果、角色 DNA、电影语言、规格编译、剪辑
references/director-memory-continuity.md    记忆与生产协议：文件结构、Snapshot、图谱、变化传播、批次与验收
references/presentation.md                  派生展示（按需）：提案、Lookbook、deck
verification/                               随仓交付的可复现验证：lint、变异样例、度量脚本、盲评量表
CHANGELOG.md                                变更、度量、测试记录、未执行项与剩余风险
LICENSE                                     Apache-2.0
```

## 版本与验证

版本与完整变更记录见 [CHANGELOG.md](CHANGELOG.md)。

随仓库交付的可复现验证见 [verification/](verification/README.md)：确定性 lint
（仓库完整性 + 协议安全网）、5 个变异样本、度量脚本与盲评量表，一键运行：

```bash
bash verification/run_all.sh
```

v7.0.0 声称的真实媒体测试（图像、配音、粗剪）制品未随仓库交付，其媒体与听感结论
在本仓库内不可复现，不作为已验证能力；v7.1.0 起，确定性验证随仓库交付，
艺术质量评价统一走盲评量表，未执行的项在 CHANGELOG 逐项标注。

## License

Apache-2.0。见 [LICENSE](LICENSE)。
