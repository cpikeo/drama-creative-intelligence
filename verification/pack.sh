#!/usr/bin/env bash
# 构建「运行包」：只含 Director Core 的创作知识（SKILL.md + references/）。
#
# 为什么可以不带 verification/：
#   · 度量证明其创作 Context 成本为 0（measure.py 的计量范围本来就不含 verification/，
#     带与不带，技能文件 token 完全相同——见 verification/README.md「运行包」节）。
#   · 技能文件从不命令创作时运行 lint / media_qa / run_all（grep 可为证）；
#     MEDIA QA 的验收要求写在协议 §6，不依赖脚本存在。
#   · 删掉它失去的是回归测试、变异样本、Token 度量、A/B 盲评台与媒体测量自检——
#     这些属于源码维护，不属于创作运行。
#
# 用法: bash verification/pack.sh [输出目录]     # 默认 dist/skill-runtime
set -uo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
OUT="${1:-dist/skill-runtime}"

rm -rf "$OUT"
mkdir -p "$OUT/references"
cp SKILL.md "$OUT/SKILL.md"
cp references/*.md "$OUT/references/"

echo "== 1. 文件集校验（应恰为 4 个技能文件，且不含 verification/）=="
EXPECTED="SKILL.md references/creative-direction.md references/director-memory-continuity.md references/presentation.md"
GOT="$(cd "$OUT" && find . -type f | sed 's|^\./||' | sort)"
echo "$GOT" | sed 's/^/  /'
BAD=0
for f in $EXPECTED; do
  [ -f "$OUT/$f" ] || { echo "  FAIL 缺文件: $f"; BAD=1; }
done
for f in $GOT; do
  case " $EXPECTED " in *" $f "*) ;; *) echo "  FAIL 运行包含多余文件: $f"; BAD=1 ;; esac
done
echo "$GOT" | grep -q '^verification/' && { echo "  FAIL 运行包含 verification/"; BAD=1; }
[ "$BAD" -eq 0 ] && echo "  PASS 文件集正确" || { echo "== 打包失败 =="; exit 1; }

echo ""
echo "== 2. 自洽校验（运行包内不得有指向包外的链接）=="
DANGLING=0
while IFS= read -r f; do
  dir="$(dirname "$OUT/$f")"
  for tgt in $(grep -o ']([^)#][^)]*)' "$OUT/$f" | sed 's/^](//;s/)$//'); do
    if [ ! -e "$dir/$tgt" ]; then
      echo "  FAIL $f -> $tgt（包外链接）"
      DANGLING=1
    fi
  done
done < <(cd "$OUT" && find . -type f | sed 's|^\./||')
[ "$DANGLING" -eq 0 ] && echo "  PASS 无包外链接（运行包可独立分发）" || { echo "== 打包失败 =="; exit 1; }

echo ""
echo "== 3. 体量与 Context 成本 =="
echo "  字节: $(find "$OUT" -type f -exec cat {} + | wc -c) B / $(find "$OUT" -type f | wc -l) 个文件"
python3 verification/measure.py "$OUT" --md 2>/dev/null |
  sed -n '/技能文件合计/p;/常驻/p;/典型任务/p' | sed 's/^/  /'

echo ""
echo "== 4. 对照：完整仓库同口径（应完全相同，证明 verification/ 的 token 成本为 0）=="
python3 verification/measure.py "$ROOT" --md 2>/dev/null |
  sed -n '/技能文件合计/p;/常驻/p;/典型任务/p' | sed 's/^/  /'

echo ""
echo "运行包已生成: $OUT（dist/ 不入库，见 .gitignore）"
echo "源码仓库请保留 verification/：lint 与变异测试是改动技能包后唯一的回归保障。"
