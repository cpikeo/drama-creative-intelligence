#!/usr/bin/env python3
"""度量脚本：技能文件的字节 / Token / 规则措辞 / 重复 / 引用完整性。

Token 口径: 优先用 tiktoken o200k_base 真实编码；无 tiktoken 时退化为
"中日韩字数 + 0.3 × 英文词数" 的估算，并在输出中标注 estimated=true。

用法:
  python3 measure.py <仓库根目录> [--md]
输出 JSON 到 stdout；--md 追加一份人读 markdown 摘要。
"""
import json
import re
import sys
from pathlib import Path

SKILL_FILES = ["SKILL.md", "references/creative-direction.md",
               "references/director-memory-continuity.md", "references/presentation.md"]
ALL_FILES = SKILL_FILES + ["README.md", "CHANGELOG.md"]
RULE_WORDS = ["必须", "禁止", "不得", "不可", "须", "必"]

try:
    import tiktoken
    ENC = tiktoken.get_encoding("o200k_base")
    ESTIMATED = False

    def tokens(text: str) -> int:
        return len(ENC.encode(text))
except Exception:
    ESTIMATED = True

    def tokens(text: str) -> int:
        cjk = len(re.findall(r"[一-鿿]", text))
        words = len(re.findall(r"[A-Za-z0-9]+", text))
        return cjk + int(words * 0.3)


def count_rule_words(text: str) -> dict:
    counts = {}
    for w in ["必须", "禁止", "不得", "不可"]:
        counts[w] = len(re.findall(w, text))
    tmp = text
    for w in ["必须", "禁止", "不得", "不可"]:
        tmp = tmp.replace(w, "")
    counts["须"] = len(re.findall("须", tmp))
    counts["必"] = len(re.findall("必", tmp))
    counts["合计"] = sum(counts.values())
    return counts


def strip_md(text: str) -> str:
    t = re.sub(r"```.*?```", " ", text, flags=re.S)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"\|", " ", t)
    t = re.sub(r"^#+\s*", "", t, flags=re.M)
    t = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"[*_>•·]", " ", t)
    return re.sub(r"\s+", "", t)


def split_sentences(text: str):
    parts = re.split(r"(?<=[。！？；!?;\n])", text)
    return [p.strip() for p in parts if len(p.strip()) >= 6]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    as_md = "--md" in sys.argv
    out = {"root": str(root), "token_estimation": "estimated" if ESTIMATED else "o200k_base",
           "files": {}}

    texts = {}
    for rel in ALL_FILES:
        p = root / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        texts[rel] = t
        out["files"][rel] = {
            "bytes": p.stat().st_size,
            "lines": t.count("\n") + 1,
            "chars": len(t),
            "tokens": tokens(t),
            "rule_words": count_rule_words(t),
        }

    skill_tok = sum(out["files"][f]["tokens"] for f in SKILL_FILES if f in out["files"])
    resident = out["files"]["SKILL.md"]["tokens"]
    out["totals"] = {
        "skill_files_bytes": sum(out["files"][f]["bytes"] for f in SKILL_FILES if f in out["files"]),
        "skill_files_tokens": skill_tok,
        "resident_SKILL_tokens": resident,
        "on_demand_references_tokens": skill_tok - resident,
        "rule_words_SKILL": out["files"]["SKILL.md"]["rule_words"]["合计"],
        "rule_words_all_skill": sum(out["files"][f]["rule_words"]["合计"]
                                    for f in SKILL_FILES if f in out["files"]),
        "typical_story_task_tokens": resident + out["files"]["references/creative-direction.md"]["tokens"],
        "typical_production_task_tokens": resident + out["files"]["references/director-memory-continuity.md"]["tokens"],
    }

    # 跨文件重复规则句（含规则词、出现在 ≥2 个技能文件中的句子）
    owners = {}
    for f in SKILL_FILES:
        if f not in texts:
            continue
        for s in split_sentences(texts[f]):
            if re.search(r"(须|必须|不得|禁止|不可)", s) and len(s) >= 8:
                owners.setdefault(s, set()).add(f)
    out["duplication"] = {
        "cross_file_rule_sentences": {s: sorted(o) for s, o in owners.items() if len(o) >= 2},
    }

    # 被 ≥2 份技能文件共享的 8 字短窗（脱敏后），含规则词者优先报告
    def grams(t, n=8):
        c = strip_md(t)
        return set(c[i:i + n] for i in range(len(c) - n + 1))

    owners = {}
    for f in SKILL_FILES:
        if f not in texts:
            continue
        for g in grams(texts[f]):
            owners.setdefault(g, set()).add(f)
    shared = {g: sorted(fs) for g, fs in owners.items() if len(fs) >= 2}
    rule_like = [(g, fs) for g, fs in sorted(shared.items()) if re.search(r"(须|必须|不得|禁止|不可|不|无)", g)]
    out["duplication"]["shared_8gram_total"] = len(shared)
    out["duplication"]["shared_8gram_rule_like"] = [{"gram": g, "files": fs} for g, fs in rule_like]

    # 链接完整性
    broken = []
    for rel, t in texts.items():
        for lm in re.finditer(r"\[[^\]]*\]\(([^)#][^)]*)\)", t):
            if not (root / lm.group(1).strip()).exists():
                broken.append(f"{rel}: {lm.group(1)}")
    out["broken_links"] = broken

    print(json.dumps(out, ensure_ascii=False, indent=2))

    if as_md:
        print("\n## 度量摘要\n")
        print("| 文件 | 字节 | tokens | 规则词 |")
        print("|---|---|---|---|")
        for rel in ALL_FILES:
            if rel in out["files"]:
                d = out["files"][rel]
                print(f"| {rel} | {d['bytes']} | {d['tokens']} | {d['rule_words']['合计']} |")
        t = out["totals"]
        print(f"\n- 技能文件合计: {t['skill_files_bytes']} B / {t['skill_files_tokens']} tok")
        print(f"- 常驻 SKILL.md: {t['resident_SKILL_tokens']} tok；按需 references: {t['on_demand_references_tokens']} tok")
        print(f"- 典型任务（故事向）: {t['typical_story_task_tokens']} tok；生产向: {t['typical_production_task_tokens']} tok")
        print(f"- 规则性措辞合计（技能文件）: {t['rule_words_all_skill']}")
        dup = out["duplication"]["cross_file_rule_sentences"]
        print(f"- 跨文件重复规则句: {len(dup)} 条")
        for s, o in dup.items():
            print(f"  - [{ '、'.join(o) }] {s[:70]}")
        print(f"- 跨文件共享 8 字短窗: {out['duplication']['shared_8gram_total']} 条"
              f"（含规则词 {len(out['duplication']['shared_8gram_rule_like'])} 条）")
        for item in out["duplication"]["shared_8gram_rule_like"][:25]:
            print(f"  - [{'、'.join(item['files'])}] {item['gram']}")
        print(f"- 失效链接: {len(out['broken_links'])}")
        if ESTIMATED:
            print("\n注意: 未安装 tiktoken，token 数为估算值。")


if __name__ == "__main__":
    main()
