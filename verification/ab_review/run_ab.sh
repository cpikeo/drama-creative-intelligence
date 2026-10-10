#!/usr/bin/env bash
# A/B 评审环境准备：校验技能版本标签，输出两个版本的指纹（sha256 + 度量），导出技能快照。
# 快照为生成物，不入库（.gitignore），lint 扫描会跳过 snapshots/ 目录。
# 用法:
#   bash run_ab.sh                          # 默认 T-AB1：skill-v7.1.0 vs skill-v7.2.0
#   bash run_ab.sh skill-v7.2.1 skill-v7.3.0   # T-AB2：连续性优化前后对照
set -uo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"
if [ "$#" -eq 0 ]; then
  TAGS=(skill-v7.1.0 skill-v7.2.0)      # 默认 T-AB1
else
  TAGS=("$@")                            # 例: skill-v7.2.1 skill-v7.3.0 → T-AB2
fi
if [ "${#TAGS[@]}" -ne 2 ]; then
  echo "用法: bash run_ab.sh [<旧版本标签> <新版本标签>]"
  exit 2
fi
FILES=(SKILL.md references/creative-direction.md references/director-memory-continuity.md references/presentation.md)

echo "== 0. 标签校验 =="
for tag in "${TAGS[@]}"; do
  if ! git -C "$ROOT" rev-parse "$tag" >/dev/null 2>&1; then
    echo "FAIL: 缺少标签 $tag"
    echo "      本仓库的 git 历史中没有该锚点（T-AB1 的 skill-v7.1.0 / skill-v7.2.0 即如此）；"
    echo "      连续性对照请用: bash run_ab.sh skill-v7.2.1 skill-v7.3.0"
    exit 1
  fi
  echo "  $tag -> $(git -C "$ROOT" rev-parse --short "$tag")"
done

echo ""
echo "== 1. 版本指纹（sha256 前 12 位 + 度量）=="
for tag in "${TAGS[@]}"; do
  echo "--- $tag"
  out="snapshots/$tag"
  rm -rf "$out"; mkdir -p "$out"
  for f in "${FILES[@]}"; do
    h=$(git -C "$ROOT" show "$tag:$f" | sha256sum | cut -c1-12)
    echo "  $f  sha256:$h"
    mkdir -p "$out/$(dirname "$f")"
    git -C "$ROOT" show "$tag:$f" > "$out/$f"
  done
  python3 ../measure.py "$out" --md 2>/dev/null | sed -n '/技能文件合计/p;/典型任务/p'
done

echo ""
echo "== 2. 产出 =="
echo "技能快照已导出到 verification/ab_review/snapshots/<tag>/（生成物，不入库）"
echo "版本对：${TAGS[0]} vs ${TAGS[1]}"
echo "下一步："
echo "  1) 主持人将两个快照以盲标 A / B 交给两名评审员，每人各持一份；"
echo "  2) 固定任务：T-AB1 用 task.md；连续性对照（v7.2.1 vs v7.3.0）用 task_continuity.md 的 T-C1–T-C7；"
echo "  3) 评审员各自独立填写 rater_sheet.md（九维度、盲于版本、附成本账）；"
echo "  4) 两版本产出都用 v7.3.0 的 lint.py --project 核对（P1–P14），失败规则记入记录单；"
echo "  5) 主持人回收评审单后解盲，分歧 >1 的维度组织讨论并记录；"
echo "  6) 产出与评审单归档，结论写入 CHANGELOG（不得由单一作者自评替代）。"
