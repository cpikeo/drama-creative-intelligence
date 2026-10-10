# 验证运行记录（verification/run_all.sh）

- 日期: 2026-10-10 01:00 +0000
- 环境: Python 3.13.16；tiktoken 0.14.0 (o200k_base)
- 性质: 全部确定性检查，零模型调用，零媒体费用

== 1/5 仓库完整性（R1-R5，应全部通过）==

== 仓库完整性（R1-R5） ==
结果: 全部通过（扫描 39 个文件，0 项失败）

== 2/5 样例项目安全网（P1-P16，应全部通过）==

== 协议安全网（P1-P16）: /home/user/drama-creative-intelligence/verification/fixtures/project ==
结果: 全部通过（扫描 2 个文件，0 项失败）

== 3/5 变异测试（10 个已知缺陷，应全部检出）==
  PASS  M10_action_stage_reset  检出规则 P16
  PASS  M1_promise_stage_skip  检出规则 P2
  PASS  M2_arrow_inside_segment  检出规则 P3
  PASS  M3_missing_fixed_chapter  检出规则 P1
  PASS  M4_dangling_basis_id  检出规则 P5
  PASS  M5_unwatched_media_approved  检出规则 P7
  PASS  M6_dangling_seam_ref  检出规则 P13
  PASS  M7_seam_not_reciprocated  检出规则 P13
  PASS  M8_cross_scene_seam_without_transition  检出规则 P14
  PASS  M9_prop_change_without_basis  检出规则 P15

== 4/5 度量 ==
## 度量摘要

| 文件 | 字节 | tokens | 规则词 |
|---|---|---|---|
| SKILL.md | 21435 | 6025 | 42 |
| references/creative-direction.md | 18829 | 5465 | 52 |
| references/director-memory-continuity.md | 11082 | 3183 | 15 |
| references/presentation.md | 2456 | 647 | 2 |
| README.md | 5750 | 1582 | 2 |
| CHANGELOG.md | 65518 | 21367 | 69 |

- 技能文件合计: 53802 B / 15320 tok
- 常驻 SKILL.md: 6025 tok；按需 references: 9295 tok
- 典型任务（故事向）: 11490 tok；生产向: 9208 tok
- 规则性措辞合计（技能文件）: 111
- 跨文件重复规则句: 0 条
- 跨文件共享 8 字短窗: 168 条（含规则词 0 条）
- 失效链接: 0

== 5/5 媒体测量层自检（需要 ffmpeg；缺失时标注未执行，不伪造结果）==
ffmpeg: /usr/local/lib/python3.13/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
== 生成参考件（目标 -16 LUFS / 1080x1920 / 10s / h264+aac）==
== 生成变异件 A（响度违规：+12 dB，无归一化）==
== 生成变异件 B（分辨率违规：1920x1080）==

-- 参考件: ref_1080p916_10s.mp4
   事实: {'file': '/home/user/drama-creative-intelligence/verification/media_selftest/assets/ref_1080p916_10s.mp4', 'duration_s': 10.0, 'vcodec': 'h264', 'width': 1080, 'height': 1920, 'fps': 30.0, 'acodec': 'aac', 'sample_rate': 48000, 'channel_layout': 'mono', 'integrated_lufs': -16.0, 'true_peak_dbtp': -8.7}
   [MEASURED_PASS] resolution: 期望 1080x1920，实测 1080x1920
   [MEASURED_PASS] duration: 期望 9–11s，实测 10.0s
   [MEASURED_PASS] vcodec: 期望 h264，实测 h264
   [MEASURED_PASS] acodec: 期望 aac，实测 aac
   [MEASURED_PASS] channels: 期望 1 声道，实测 mono
   [MEASURED_PASS] integrated_loudness: 实测 -16.0 LUFS，目标 -16.0 ±0.5，偏差 +0.0 LU
   [MEASURED_PASS] true_peak: 实测 -8.7 dBTP，上限 -1.0 dBTP
   NEEDS_HUMAN 感官项: 5 项（恒为待人工）
   断言: 无 MEASURED_FAIL 且感官项齐全 -> PASS

-- 变异件A(响度): mutation_loudness.mp4
   事实: {'file': '/home/user/drama-creative-intelligence/verification/media_selftest/assets/mutation_loudness.mp4', 'duration_s': 10.0, 'vcodec': 'h264', 'width': 1080, 'height': 1920, 'fps': 30.0, 'acodec': 'aac', 'sample_rate': 48000, 'channel_layout': 'mono', 'integrated_lufs': -9.8, 'true_peak_dbtp': -1.1}
   [MEASURED_PASS] resolution: 期望 1080x1920，实测 1080x1920
   [MEASURED_PASS] duration: 期望 9–11s，实测 10.0s
   [MEASURED_PASS] vcodec: 期望 h264，实测 h264
   [MEASURED_PASS] acodec: 期望 aac，实测 aac
   [MEASURED_PASS] channels: 期望 1 声道，实测 mono
   [MEASURED_FAIL] integrated_loudness: 实测 -9.8 LUFS，目标 -16.0 ±0.5，偏差 +6.2 LU；超差须二遍归一化（协议 §6）
   [MEASURED_PASS] true_peak: 实测 -1.1 dBTP，上限 -1.0 dBTP
   NEEDS_HUMAN 感官项: 5 项（恒为待人工）
   断言: 必须检出 ['integrated_loudness'] -> 实际检出 ['integrated_loudness'] -> PASS

-- 变异件B(分辨率): mutation_resolution.mp4
   事实: {'file': '/home/user/drama-creative-intelligence/verification/media_selftest/assets/mutation_resolution.mp4', 'duration_s': 10.0, 'vcodec': 'h264', 'width': 1920, 'height': 1080, 'fps': 30.0, 'acodec': 'aac', 'sample_rate': 48000, 'channel_layout': 'mono', 'integrated_lufs': -16.0, 'true_peak_dbtp': -8.7}
   [MEASURED_FAIL] resolution: 期望 1080x1920，实测 1920x1080
   [MEASURED_PASS] duration: 期望 9–11s，实测 10.0s
   [MEASURED_PASS] vcodec: 期望 h264，实测 h264
   [MEASURED_PASS] acodec: 期望 aac，实测 aac
   [MEASURED_PASS] channels: 期望 1 声道，实测 mono
   [MEASURED_PASS] integrated_loudness: 实测 -16.0 LUFS，目标 -16.0 ±0.5，偏差 +0.0 LU
   [MEASURED_PASS] true_peak: 实测 -8.7 dBTP，上限 -1.0 dBTP
   NEEDS_HUMAN 感官项: 5 项（恒为待人工）
   断言: 必须检出 ['resolution'] -> 实际检出 ['resolution'] -> PASS

== 自检结论 ==
媒体测量层: 参考件全项测量通过；两个变异件被对应规则检出；感官项恒为 NEEDS_HUMAN。

## 总结果: 全部验证通过
