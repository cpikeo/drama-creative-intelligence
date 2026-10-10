#!/usr/bin/env bash
# 一键验证入口：仓库完整性 + 样例项目安全网 + 变异测试 + 度量。
# 全部为确定性检查，不调用任何模型，不产生媒体费用。
# 运行记录自动写入 results/latest_run.md。
set -uo pipefail
cd "$(dirname "$0")"
ROOT="$(cd .. && pwd)"
mkdir -p results

{
echo "# 验证运行记录（verification/run_all.sh）"
echo ""
echo "- 日期: $(date '+%Y-%m-%d %H:%M %z')"
echo "- 环境: $(python3 --version 2>&1)；$(python3 -c 'import tiktoken; print("tiktoken", tiktoken.__version__, "(o200k_base)")' 2>/dev/null || echo 'tiktoken 缺失（token 为估算）')"
echo "- 性质: 全部确定性检查，零模型调用，零媒体费用"
echo ""

FAIL=0
echo "== 1/5 仓库完整性（R1-R5，应全部通过）=="
python3 lint.py --repo "$ROOT" || FAIL=1

echo ""
echo "== 2/5 样例项目安全网（P1-P16，应全部通过）=="
python3 lint.py --project fixtures/project || FAIL=1

echo ""
echo "== 3/5 变异测试（10 个已知缺陷，应全部检出）=="
for d in fixtures/mutations/M*/; do
  name="$(basename "$d")"
  expect="$(cat "$d/EXPECT")"
  out="$(python3 lint.py --project "$d" 2>&1)"
  if [ $? -ne 0 ] && echo "$out" | grep -q "\[$expect\]"; then
    echo "  PASS  $name  检出规则 $expect"
  else
    echo "  FAIL  $name  期望检出 $expect"
    echo "$out"
    FAIL=1
  fi
done

echo ""
echo "== 4/5 度量 =="
python3 measure.py "$ROOT" > "results/measure_$(date +%Y%m%d).json"
python3 measure.py "$ROOT" --md | sed -n '/## 度量摘要/,$p'

echo ""
echo "== 5/5 媒体测量层自检（需要 ffmpeg；缺失时标注未执行，不伪造结果）=="
python3 media_qa.py --selftest || FAIL=1

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "## 总结果: 全部验证通过"
else
  echo "## 总结果: 存在失败项，见上方输出"
fi
exit "$FAIL"
} 2>&1 | tee results/latest_run.md
EXIT=${PIPESTATUS[0]}
exit "$EXIT"
