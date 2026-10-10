# drama-creative-intelligence v7.5.1

导演级与作者级的剧集创作智能。用于从一句话、授权原著、剧本、分镜或成片出发，创作、续写、修改或生产 AI 漫剧、短剧、剧集、广告与电影；按项目规模分级维护跨集记忆、世界状态、角色 DNA（含声音绑定）、跨镜接缝与因果图谱，并对真实媒体做分层验收。

## 这是什么

一份自洽的创作技能包：入口是 `SKILL.md`（常驻），`references/` 下三份手册按任务按需加载，不需要在每次对话中全部读入。

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 判断的宪法 + 记忆档位（常驻） |
| `references/creative-direction.md` | 故事、角色、电影语言（含接缝维度清单）、规格与剪辑（按需） |
| `references/director-memory-continuity.md` | 档位表、文件结构、Snapshot、图谱、变化传播、批次与验收（按需） |
| `references/presentation.md` | 派生展示：提案、Lookbook、deck（按需） |

本包只含创作知识：没有脚本、没有测试目录、没有变更日志，四个文件之外不加载任何东西。

## 记录面分级

创作契约里定一次档：`T0 单条 · T1 单集 · T2 连续`（判据见 `SKILL.md` §2，免记清单见 `references/director-memory-continuity.md` §1）。
单条与单集项目不建图谱、承诺账、Snapshot 链与全字段镜头卡；连续剧仍是全量记录。任何档位都不省略：
身份锚点（脸 · 配音锁 · 关键道具外观）· 当前 STATE · 已声明的状态变化 · 未检查媒体的 `PROVISIONAL` 标记。

同一叙事的实测对照：15 秒单条猫咪短剧按 T0 口径比 T2 口径省 23.8% 记录面（3,394 → 2,585 tokens，同一正文、两版接缝与 QA 标准相同）。

## 许可

Apache-2.0，见 [LICENSE](LICENSE)。
