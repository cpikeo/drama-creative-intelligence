#!/usr/bin/env python3
"""drama-creative-intelligence 确定性校验器（Continuity Lint + 仓库完整性）。

只做确定性检查，不做任何模型调用、不评作品质量。作品质量评价见 rubric.md（人工盲评）。

用法:
  python3 lint.py --repo <仓库根目录>                 # 仓库完整性（R1-R5）
  python3 lint.py --project <项目目录>                # 协议安全网（P1-P16）

退出码: 0 全部通过；1 存在失败。输出每条失败的规则 ID、位置与证据。
"""
import re
import sys
from pathlib import Path

# ---------------- 公共工具 ----------------

STAGES = {"Seeded": 0, "Activated": 1, "Pressured": 2, "Narrowed": 3,
          "Redefined": 4, "Fulfilled": 5, "Abandoned": 5}
QA_CONCLUSIONS = {"APPROVE", "APPROVE_WITH_NOTES", "REVISE", "PROVISIONAL"}
KNOWN_PREFIX = {"CHAR", "LOC", "PROP", "EVENT", "REL", "PROM", "ASSET", "SC", "SH",
                "MEDIA", "EDGE", "LOCK", "GEN", "CUT", "P", "DEC", "CHG", "REF"}
EP_CHAPTERS = ["场次与出去压力", "对白", "镜头卡", "变化记录", "道具持有链", "承诺状态",
               "光态与时间", "图谱增量", "Snapshot Diff", "QA", "生产追踪"]

ID_RE = re.compile(r"\b([A-Z]{2,6}(?:-[A-Z]{2,6})?-\d+)\b")
PLAIN_ID_RE = re.compile(r"\b([A-Z]{2,6})-(\d+)\b")
SHOT_ID_RE = re.compile(r"\bSH-\d+\b")


class Report:
    def __init__(self):
        self.failures = []
        self.files_scanned = 0

    def fail(self, rule, loc, msg):
        self.failures.append((rule, loc, msg))

    def done(self, name):
        print(f"\n== {name} ==")
        if self.failures:
            for rule, loc, msg in self.failures:
                print(f"  FAIL [{rule}] {loc}: {msg}")
            print(f"结果: {len(self.failures)} 项失败（扫描 {self.files_scanned} 个文件）")
            return 1
        print(f"结果: 全部通过（扫描 {self.files_scanned} 个文件，0 项失败）")
        return 0


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def all_md(root: Path):
    # 跳过 .git、__pycache__ 与 A/B 生成快照（生成物，不入库）
    return sorted(p for p in root.rglob("*.md")
                  if not ({".git", "__pycache__", "snapshots"} & set(p.parts)))


# ---------------- 仓库完整性（R1-R5） ----------------

def check_repo(root: Path) -> int:
    rep = Report()
    rep.files_scanned = len([f for f in all_md(root) if ".git" not in f.parts])

    # R1: frontmatter 与版本一致性
    skill = read(root / "SKILL.md")
    m = re.match(r"^---\n(.*?)\n---\n", skill, flags=re.S)
    if not m:
        rep.fail("R1", "SKILL.md", "缺少 frontmatter")
    else:
        fm = m.group(1)
        for field in ("name:", "description:", "license:"):
            if field not in fm:
                rep.fail("R1", "SKILL.md frontmatter", f"缺字段 {field}")
        vm = re.search(r"version:\s*([\d.]+)", fm)
        if not vm:
            rep.fail("R1", "SKILL.md frontmatter", "metadata 缺 version")
        else:
            ver = vm.group(1)
            readme = read(root / "README.md")
            if f"v{ver}" not in readme:
                rep.fail("R1", "README.md", f"标题版本与 frontmatter 不一致（应为 v{ver}）")
            chlog = read(root / "CHANGELOG.md")
            if not re.search(rf"^## v{re.escape(ver)}\b", chlog, flags=re.M):
                rep.fail("R1", "CHANGELOG.md", f"最新条目不是 v{ver}")

    # R2: Markdown 链接全部可解析
    for f in all_md(root):
        if ".git" in f.parts:
            continue
        text = read(f)
        for lm in re.finditer(r"\[[^\]]*\]\(([^)#][^)]*)\)", text):
            target = lm.group(1).strip()
            if not (f.parent / target).resolve().exists():
                rep.fail("R2", f.relative_to(root), f"失效链接: {target}")

    # R3: § 章节引用可解析
    alias = {
        "SKILL": "SKILL.md", "宪法": "SKILL.md",
        "手册": "references/creative-direction.md",
        "导演判断手册": "references/creative-direction.md",
        "creative-direction": "references/creative-direction.md",
        "协议": "references/director-memory-continuity.md",
        "记忆与生产协议": "references/director-memory-continuity.md",
        "presentation": "references/presentation.md",
        "Presentation": "references/presentation.md",
        "Presentation手册": "references/presentation.md",
    }
    skill_files = ["SKILL.md", "references/creative-direction.md",
                   "references/director-memory-continuity.md", "references/presentation.md"]

    def sections_of(rel):
        text = read(root / rel)
        return set(int(n) for n in re.findall(r"^#{2,3}\s+(\d+)[｜|]", text, flags=re.M))

    sec_cache = {rel: sections_of(rel) for rel in skill_files}
    pat = re.compile(r"(SKILL|宪法|手册|导演判断手册|creative-direction|协议|记忆与生产协议"
                     r"|Presentation手册|Presentation|presentation)?\s*§\s*(\d+)\s*(?:[–—-]\s*(\d+))?")
    for rel in skill_files:
        text = read(root / rel)
        for sm in pat.finditer(text):
            target_rel = alias.get(sm.group(1)) if sm.group(1) else rel
            if target_rel not in sec_cache:
                rep.fail("R3", rel, f"未知引用目标: {sm.group(0)!r}")
                continue
            secs = sec_cache[target_rel]
            lo = int(sm.group(2))
            hi = int(sm.group(3)) if sm.group(3) else lo
            for n in range(lo, hi + 1):
                if n not in secs:
                    rep.fail("R3", rel, f"引用 {sm.group(0)!r} → {target_rel} 无 §{n}")

    # R5: 运行包自洽——技能文件不得链接 verification/（验证工具只属维护者，不进创作 Context）
    for rel in skill_files:
        text = read(root / rel)
        for lm in re.finditer(r"\[[^\]]*\]\(([^)#][^)]*)\)", text):
            if lm.group(1).strip().startswith("verification/"):
                rep.fail("R5", rel,
                         f"技能文件链接了验证目录: {lm.group(1)}"
                         f"（verification/ 仅维护者使用，运行包不携带；请改为文字说明）")

    # R4: 关键概念保留（能力不因重构丢失）
    concepts_file = root / "verification" / "concepts.txt"
    if concepts_file.exists():
        skill_text = "\n".join(read(root / f) for f in skill_files)
        for line in read(concepts_file).splitlines():
            c = line.strip()
            if not c or c.startswith("#"):
                continue
            if c not in skill_text:
                rep.fail("R4", "verification/concepts.txt", f"关键概念在技能文件中缺失: {c}")

    return rep.done("仓库完整性（R1-R5）")


# ---------------- 协议安全网（P1-P16） ----------------

# 接缝中"物品状态变化"的封闭词表（与手册 §3 静动逻辑一致；写不进词表的变化用 EVENT-/CHG- 描述）
PROP_CHANGE_WORDS = ("拿起", "放下", "传递", "递交", "接过", "开门", "关门", "半开", "开启",
                     "关上", "推开", "拉开", "破损", "破碎", "熄灭", "点燃", "翻倒", "掉落",
                     "换到", "新增", "消失", "不见", "多出", "少了一个")
# "动作未完成"的封闭标记（写进出点即承诺下一镜承接同一阶段）
UNFINISHED_WORDS = ("未完成", "进行中", "中途")
CARRIED_WORDS = ("未完成", "进行中", "中途", "半开", "继续")

def collect_ids(files_text: dict):
    ids = set()
    for text in files_text.values():
        ids.update(ID_RE.findall(text))
    return ids


def check_project(root: Path) -> int:
    rep = Report()
    files = {p: read(p) for p in all_md(root)}
    rep.files_scanned = len(files)
    rel_files = {str(p.relative_to(root)): t for p, t in files.items()}
    all_ids = collect_ids(rel_files)
    ep_files = {k: t for k, t in rel_files.items() if re.search(r"剧集/EP\d+\.md$", k)}

    # P6: ID 前缀合法（先跑，后续检查依赖完整 ID 集合的语义）
    for rel, text in rel_files.items():
        for tok in ID_RE.findall(text):
            prefix = tok.rsplit("-", 1)[0].split("-")[-1]
            if prefix not in KNOWN_PREFIX:
                rep.fail("P6", rel, f"未知 ID 前缀: {tok}")

    # P1: 集文件固定章节
    for rel, text in ep_files.items():
        for ch in EP_CHAPTERS:
            if not re.search(rf"^## {re.escape(ch)}\b", text, flags=re.M):
                rep.fail("P1", rel, f"缺固定章节「{ch}」")

    # P2: 承诺逐级推进、不跳阶；承诺账与承诺状态一致
    promise_status = {}
    for rel, text in rel_files.items():
        for row in re.findall(r"^\|\s*(PROM-\d+)\s*\|[^|]*\|[^|]*\|\s*(\w+)\s*\|", text, flags=re.M):
            pid, status = row
            if status not in STAGES:
                rep.fail("P2", rel, f"{pid} 承诺账状态非法: {status}")
            promise_status[pid] = status
    for rel, text in ep_files.items():
        for pm in re.finditer(r"(PROM-\d+)：\s*(\w+)\s*→\s*(\w+)", text):
            pid, a, b = pm.groups()
            if a not in STAGES or b not in STAGES:
                rep.fail("P2", rel, f"{pid} 状态名非法: {a} → {b}")
            elif STAGES[b] - STAGES[a] != 1:
                rep.fail("P2", rel, f"{pid} 跳阶: {a} → {b}（须逐级推进，跨两阶拆两行）")
            else:
                promise_status[pid] = b
    for pid, status in promise_status.items():
        # 承诺账（总控）当前状态须与集内最后一次推进一致
        for rel, text in rel_files.items():
            for row in re.finditer(rf"^\|\s*{pid}\s*\|[^|]*\|[^|]*\|\s*(\w+)\s*\|", text, flags=re.M):
                if row.group(1) != status:
                    rep.fail("P2", rel, f"{pid} 承诺账状态 {row.group(1)} 与集内推进终点 {status} 不一致")

    # P3: 变更记录六段链（变更ID · 变化前 → 触发 → 代价或结果 → 变化后 → 生效范围 → 下游影响）
    for rel, text in rel_files.items():
        for line in text.splitlines():
            if re.match(r"^CHG-\d+\s*·", line):
                parts = line.split("·")
                if len(parts) != 2:
                    rep.fail("P3", rel, f"变更记录须为「ID · 六段链」两部分: {line[:40]}")
                    continue
                segs = parts[1].split("→")
                if len(segs) != 6 or any(not s.strip() for s in segs):
                    rep.fail("P3", rel, f"变更记录须恰好 6 段且均非空，当前 {len(segs)} 段: {line[:40]}")

    # P4: Snapshot Diff / 前因 引用的 ID 必须存在（总控与集文件都可能持有前因）
    for rel, text in rel_files.items():
        m = re.search(r"^## Snapshot Diff\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
        if m:
            for tok in ID_RE.findall(m.group(1)):
                if tok not in all_ids:
                    rep.fail("P4", rel, f"Snapshot Diff 引用了不存在的 ID: {tok}")
        for fm in re.finditer(r"前因[：:]([^\n]*(?:\n(?!## |### )[^\n]*)*)", text):
            if "首集" in fm.group(1):
                continue
            cited = ID_RE.findall(fm.group(1))
            if not cited:
                rep.fail("P4", rel, "非首集的前因须逐条引用上集出去压力的 ID")
            for tok in cited:
                if tok not in all_ids:
                    rep.fail("P4", rel, f"前因引用了不存在的 ID: {tok}")

    # 解析镜头卡
    shots = {}  # SH-ID -> basis/func/line/file + 接缝字段（sc/in/out/trans）
    for rel, text in ep_files.items():
        for line in text.splitlines():
            sm = re.match(r"^(SH-\d+)\s*·\s*(.*)$", line)
            if not sm:
                continue
            sid, rest = sm.groups()
            fields = [f.strip() for f in rest.split(" · ")]
            basis, func, trans, seam_in, seam_out = set(), "", "", "", ""
            for f in fields:
                for lab in ("连续性依据", "主功能", "转场", "入点", "出点"):
                    idx = f.find(lab + "：")
                    if idx == -1:
                        continue
                    val = f[idx + len(lab) + 1:]
                    if lab == "连续性依据":
                        basis = set(ID_RE.findall(val))
                    elif lab == "主功能":
                        func = val
                    elif lab == "转场":
                        trans = val
                    elif lab == "入点":
                        seam_in = val
                    else:
                        seam_out = val
            sc = re.search(r"\bSC-\d+", fields[0]) if fields else None
            shots[sid] = {"basis": basis, "func": func, "line": line, "file": rel,
                          "sc": sc.group(0) if sc else "",
                          "in": seam_in, "out": seam_out, "trans": trans}

    # P5: 对白依据存在且被所属镜头的连续性依据覆盖
    for rel, text in ep_files.items():
        for row in re.findall(r"^\|\s*(CHAR-\d+)\s*\|\s*(SH-\d+)\s*\|([^|]*)\|\s*([^|]*?)\s*\|",
                              text, flags=re.M):
            speaker, sid, _line, basis = row
            if speaker not in all_ids:
                rep.fail("P5", rel, f"对白说话人不存在: {speaker}")
            if sid not in shots:
                rep.fail("P5", rel, f"对白引用了不存在的镜头: {sid}")
                continue
            b_ids = set(ID_RE.findall(basis)) or ({basis.strip()} if basis.strip() else set())
            if not b_ids:
                rep.fail("P5", rel, f"对白缺依据 ID: {speaker}「{_line.strip()[:20]}」")
            for b in b_ids:
                if b not in all_ids:
                    rep.fail("P5", rel, f"对白依据不存在: {b}")
                elif b not in shots[sid]["basis"]:
                    rep.fail("P5", rel, f"对白依据 {b} 未被 {sid} 的连续性依据覆盖")

    # P11/P12/P13/P14: 每镜有职责、连续性依据非空、跨镜接缝可追溯
    for sid, info in shots.items():
        if not info["func"]:
            rep.fail("P11", info["file"], f"{sid} 缺主功能（每镜须有职责）")
        if not info["basis"]:
            rep.fail("P12", info["file"], f"{sid} 连续性依据为空")

    # P13: 接缝字段齐备、引用存在、出点与入点双向回指
    for sid, info in shots.items():
        if not info["in"]:
            rep.fail("P13", info["file"], f"{sid} 缺入点（跨镜接缝：承接哪一镜）")
        if not info["out"]:
            rep.fail("P13", info["file"], f"{sid} 缺出点（跨镜接缝：交给哪一镜）")
        for r in set(SHOT_ID_RE.findall(info["in"])) | set(SHOT_ID_RE.findall(info["out"])):
            if r not in shots:
                rep.fail("P13", info["file"], f"{sid} 接缝引用了不存在的镜头: {r}")
        for r in set(SHOT_ID_RE.findall(info["out"])):
            tgt = shots.get(r)
            if tgt is None or "有意断裂" in tgt["in"]:
                continue
            if sid not in set(SHOT_ID_RE.findall(tgt["in"])):
                rep.fail("P13", info["file"],
                         f"{sid} 出点指向 {r}，但 {r} 的入点未回指本镜"
                         f"（须在 {r} 入点声明有意断裂与回归锚点）")

    # P14: 跨场接缝须有依据（转场性质或事件/变更 ID），否则跨镜变化无出处
    TRANSITION_WORDS = ("硬切", "静帧", "留黑", "匹配", "声音桥", "省略", "重建空间",
                        "时空转换", "主观", "跳切", "非线性")
    for sid, info in shots.items():
        for r in set(SHOT_ID_RE.findall(info["in"])):
            tgt = shots.get(r)
            if tgt is None or not tgt["sc"] or not info["sc"] or tgt["sc"] == info["sc"]:
                continue
            declared = any(w in (info["in"] + info["trans"]) for w in TRANSITION_WORDS) \
                or bool(re.search(r"(EVENT|CHG|DEC)-\d+", info["in"] + info["trans"]))
            if not declared:
                rep.fail("P14", info["file"],
                         f"{sid} 承接 {tgt['sc']} 的 {r} 却未声明转场性质或事件依据"
                         f"（跨镜变化须有叙事或剪辑依据）")

    # P15: 接缝中的物品状态变化须挂来源 ID（无来源的物品变化不成立）
    for sid, info in shots.items():
        for label, txt in (("入点", info["in"]), ("出点", info["out"])):
            if not txt:
                continue
            if re.search(r"\bPROP-\d+\b", txt) and any(w in txt for w in PROP_CHANGE_WORDS) \
               and not re.search(r"(EVENT|CHG|DEC)-\d+", txt):
                rep.fail("P15", info["file"],
                         f"{sid} {label}出现物品状态变化却未挂来源 ID"
                         f"（PROP 变化须有事件、变更或决定依据）")

    # P16: 动作阶段须写明；出点未完成的动作，下一镜入点须承接同一阶段
    for sid, info in shots.items():
        for label, txt in (("入点", info["in"]), ("出点", info["out"])):
            if txt and "动作阶段" not in txt:
                rep.fail("P16", info["file"], f"{sid} {label}缺动作阶段（动作跨镜须可衔接）")
        for r in set(SHOT_ID_RE.findall(info["out"])):
            tgt = shots.get(r)
            if tgt is None or "有意断裂" in tgt["in"]:
                continue
            if any(w in info["out"] for w in UNFINISHED_WORDS) and \
               not any(w in tgt["in"] for w in CARRIED_WORDS):
                rep.fail("P16", info["file"],
                         f"{sid} 出点动作未完成，但 {r} 的入点未承接同一动作阶段"
                         f"（不得从已完成状态开始）")

    # P8: 进入生成的镜头须有三块规格
    for rel, text in ep_files.items():
        for row in re.findall(r"^\|\s*(GEN-\d+)\s*\|([^|]*)\|([^|]*SH-\d+[^|]*)\|[^|]*\|\s*(GEN|MEDIA)\s*\|",
                              text, flags=re.M):
            _tid, _modal, spec, status = row
            sid = re.search(r"SH-\d+", spec).group(0)
            if status == "GEN" and sid in shots:
                line = shots[sid]["line"]
                for block in ("IDENTITY", "STATE", "SHOT"):
                    if block not in line:
                        rep.fail("P8", rel, f"{sid} 进入生成但镜头卡缺 {block} 块规格")

    # P9: 镜头须被光态与时间状态表覆盖（含区间展开）
    for rel, text in ep_files.items():
        m = re.search(r"^## 光态与时间\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
        if not m:
            continue
        covered = set()
        for rng in re.finditer(r"(SH)-(\d+)\s*[–—-]\s*(?:SH-)?(\d+)", m.group(1)):
            for n in range(int(rng.group(2)), int(rng.group(3)) + 1):
                covered.add(f"SH-{n:03d}")
        for sid in re.findall(r"SH-\d+", m.group(1)):
            covered.add(sid)
        for sid, info in shots.items():
            if info["file"] == rel and sid not in covered:
                rep.fail("P9", rel, f"{sid} 未被光态与时间状态表覆盖")

    # P10: 道具持有链（道具存在、持有人存在、位置非空）
    for rel, text in ep_files.items():
        for line in text.splitlines():
            if re.match(r"^PROP-\d+\s*·", line):
                pid = re.match(r"^(PROP-\d+)", line).group(1)
                if pid not in all_ids:
                    rep.fail("P10", rel, f"道具不存在于图谱: {pid}")
                holder = re.search(r"持有人[：:]\s*(CHAR-\d+)", line)
                if not holder:
                    rep.fail("P10", rel, f"{pid} 缺持有人")
                elif holder.group(1) not in all_ids:
                    rep.fail("P10", rel, f"{pid} 持有人不存在: {holder.group(1)}")
                if not re.search(r"位置[：:][^·]+", line):
                    rep.fail("P10", rel, f"{pid} 缺位置")

    # P7: 未实际检查的媒体不得通过
    for rel, text in ep_files.items():
        for row in re.findall(r"^\|\s*(GEN-\d+)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(MEDIA)\s*\|([^|]*?)\|([^|]*?)\|",
                              text, flags=re.M):
            tid, _status, checked, concl = row
            if concl.strip() in {"APPROVE", "APPROVE_WITH_NOTES"} and \
               checked.strip() in {"", "—", "未执行", "未检查"}:
                rep.fail("P7", rel, f"{tid} 未实际检查媒体却给出 {concl.strip()}（应为 PROVISIONAL）")
        m = re.search(r"^## QA\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
        if m:
            for cm in re.finditer(r"(SPEC QA|MEDIA QA|CUT QA)[：:]\s*(\w+)", m.group(1)):
                if cm.group(2) not in QA_CONCLUSIONS:
                    rep.fail("P7", rel, f"非法 QA 结论: {cm.group(2)}")

    # 节点重复定义（同一节点在两个图谱块中定义）
    node_defs = {}
    for rel, text in rel_files.items():
        m = re.search(r"^#+ 节点\n(.*?)(?=^#+ |\Z)", text, flags=re.S | re.M)
        if m:
            for tok in ID_RE.findall(m.group(1)):
                node_defs.setdefault(tok, []).append(rel)
    for tok, where in node_defs.items():
        if len(where) > 1:
            rep.fail("P6", ",".join(where), f"节点重复定义: {tok}")

    return rep.done(f"协议安全网（P1-P16）: {root}")


def main():
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "--repo":
        sys.exit(check_repo(Path(args[1]).resolve()))
    if len(args) >= 2 and args[0] == "--project":
        sys.exit(check_project(Path(args[1]).resolve()))
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
