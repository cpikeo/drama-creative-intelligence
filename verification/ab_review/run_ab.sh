#!/usr/bin/env bash
# A/B 评审环境准备：校验技能版本标签，输出两个版本的指纹（sha256 + 度量），导出技能快照。
# 快照为生成物，不入库（.gitignore），lint 扫描会跳过 snapshots/ 目录。
set -uo pipefail
cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"
TAGS=(skill-v7.1.0 skill-v7.2.0)
FILES=(SKILL.md references/creative-direction.md references/director-memory-continuity.md references/presentation.md)

echo "== 0. 标签校验 =="
for tag in "${TAGS[@]}"; do
  if ! git -C "$ROOT" rev-parse "$tag" >/dev/null 2>&1; then
    echo "FAIL: 缺少标签 $tag"
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
echo "下一步："
echo "  1) 主持人将两个快照以盲标 A / B 交给两名评审员，每人各持一份；"
echo "  2) 评审员按 task.md（T-AB1）在对应版本下完成同一任务，产出创作与规格层作品；"
echo "  3) 评审员各自独立填写 rater_sheet.md（八维度、盲于版本）；"
echo "  4) 主持人回收评审单后解盲，分歧 >1 的维度组织讨论并记录；"
echo "  5) 产出与评审单归档，结论写入 CHANGELOG（不得由单一作者自评替代）。"
