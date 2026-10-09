# 验证运行记录（verification/run_all.sh）

- 日期: 2026-10-09 08:34 +0000
- 环境: Python 3.13.16；tiktoken 0.14.0 (o200k_base)
- 性质: 全部确定性检查，零模型调用，零媒体费用

== 1/4 仓库完整性（R1-R4，应全部通过）==

== 仓库完整性（R1-R4） ==
结果: 全部通过（扫描 21 个文件，0 项失败）

== 2/4 样例项目安全网（P1-P12，应全部通过）==

== 协议安全网（P1-P12）: /home/user/drama-creative-intelligence/verification/fixtures/project ==
结果: 全部通过（扫描 2 个文件，0 项失败）

== 3/4 变异测试（5 个已知缺陷，应全部检出）==
  PASS  M1_promise_stage_skip  检出规则 P2
  PASS  M2_arrow_inside_segment  检出规则 P3
  PASS  M3_missing_fixed_chapter  检出规则 P1
  PASS  M4_dangling_basis_id  检出规则 P5
  PASS  M5_unwatched_media_approved  检出规则 P7

== 4/4 度量 ==
## 度量摘要

| 文件 | 字节 | tokens | 规则词 |
|---|---|---|---|
| SKILL.md | 20200 | 5650 | 41 |
| references/creative-direction.md | 13393 | 3874 | 27 |
| references/director-memory-continuity.md | 10493 | 3021 | 14 |
| references/presentation.md | 2456 | 647 | 2 |
| README.md | 4146 | 1113 | 1 |
| CHANGELOG.md | 20211 | 6535 | 25 |

- 技能文件合计: 46542 B / 13192 tok
- 常驻 SKILL.md: 5650 tok；按需 references: 7542 tok
- 典型任务（故事向）: 9524 tok；生产向: 8671 tok
- 规则性措辞合计（技能文件）: 84
- 跨文件重复规则句: 0 条
- 跨文件共享 8 字短窗: 128 条（含规则词 0 条）
- 失效链接: 0

## 总结果: 全部验证通过
