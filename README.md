# drama-creative-intelligence v7.4.4

导演级与作者级的剧集创作智能。用于从一句话、授权原著、剧本、分镜或成片出发，创作、续写、修改或生产 AI 漫剧、短剧、剧集、广告与电影；维护跨集记忆、世界状态、角色 DNA（含声音）、跨镜接缝与因果图谱，并对真实媒体做分层验收。

## 这是什么

一份可直接加载的创作技能包。入口是 `SKILL.md`；`references/` 下的三份手册按需加载，
不需要在每次对话中全部读入。

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 核心契约与工作流（常驻） |
| `references/creative-direction.md` | 故事、角色、电影语言、规格与剪辑（按需） |
| `references/director-memory-continuity.md` | 记忆协议、世界状态、跨集与跨镜连续性（按需） |
| `references/presentation.md` | 交付与汇报格式（按需） |

## 许可

Apache-2.0，见 [LICENSE](LICENSE)。

## 源码仓库

本包只含创作知识。回归测试、规则 lint、Token 度量、媒体测量自检与 A/B 盲评协议
属于源码维护，不在本包内，见上游源码仓库。
