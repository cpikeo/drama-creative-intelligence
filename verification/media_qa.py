#!/usr/bin/env python3
"""媒体测量层：对真实媒体文件做确定性测量，逐项给出结论。

测量不等于观看：
- 可测指标（分辨率 / 时长 / 编码 / 积分响度 LUFS / 真峰值 dBTP）→ MEASURED_PASS / MEASURED_FAIL
- 感官项（身份一致、表演情绪、听感、画面观感、口型字幕）→ 恒为 NEEDS_HUMAN（对应 QA 的 PROVISIONAL）

ffmpeg 查找顺序：PATH → imageio-ffmpeg 静态二进制。缺失时 --selftest 标注跳过，不伪造结果。

用法:
  python3 media_qa.py --media <文件> [--width 1080] [--height 1920] [--dur-min 9] [--dur-max 11]
                      [--vcodec h264] [--acodec aac] [--lufs-target -16] [--lufs-tol 0.5]
                      [--tp-max -1.0] [--channels 2]
  python3 media_qa.py --selftest [--assets <目录>]

退出码: 0 无 MEASURED_FAIL（selftest: 全部断言成立或已跳过）；1 存在测量失败/断言失败；2 工具缺失或文件不可读。
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SENSORY_ITEMS = [
    "身份一致（对照 REF 与美学锚点）",
    "表演与情绪",
    "听感（韵律 / 呼吸 / 房间声）",
    "画面观感（构图 / 光影 / 材质）",
    "口型与字幕（如有）",
]


def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def probe(ff, path):
    """用 ffmpeg -i 解析容器与流信息（无 ffprobe 依赖）。"""
    r = subprocess.run([ff, "-hide_banner", "-i", str(path)],
                       capture_output=True, text=True, timeout=120)
    info = r.stderr
    facts = {"file": str(path)}
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    facts["duration_s"] = round(int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)), 3) if m else None
    m = re.search(r"Video: (\S+).*?(\d{2,5})x(\d{2,5}).*?([\d.]+) fps", info)
    if m:
        facts["vcodec"], facts["width"], facts["height"], facts["fps"] = \
            m.group(1), int(m.group(2)), int(m.group(3)), float(m.group(4))
    m = re.search(r"Audio: (\S+).*?(\d{3,6}) Hz(?:, (\w+))?", info)
    if m:
        facts["acodec"], facts["sample_rate"] = m.group(1), int(m.group(2))
        facts["channel_layout"] = m.group(3) or ""
    return facts


def measure_loudness(ff, path):
    """BS.1770 积分响度与真峰值（ebur128, peak=true）。"""
    r = subprocess.run([ff, "-hide_banner", "-nostats", "-i", str(path),
                        "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=300)
    out = r.stderr
    i_vals = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    p_vals = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", out)
    return {
        "integrated_lufs": float(i_vals[-1]) if i_vals else None,
        "true_peak_dbtp": float(p_vals[-1]) if p_vals else None,
    }


def qa_media(ff, path, spec):
    facts = probe(ff, path)
    facts.update(measure_loudness(ff, path))
    verdicts = {}

    def setv(name, ok, detail):
        verdicts[name] = {"verdict": "MEASURED_PASS" if ok else "MEASURED_FAIL", "detail": detail}

    if spec.get("width") and spec.get("height"):
        got = (facts.get("width"), facts.get("height"))
        setv("resolution", got == (spec["width"], spec["height"]),
             f"期望 {spec['width']}x{spec['height']}，实测 {got[0]}x{got[1]}")
    if spec.get("dur_min") is not None and spec.get("dur_max") is not None:
        d = facts.get("duration_s")
        setv("duration", d is not None and spec["dur_min"] <= d <= spec["dur_max"],
             f"期望 {spec['dur_min']}–{spec['dur_max']}s，实测 {d}s")
    if spec.get("vcodec"):
        setv("vcodec", facts.get("vcodec") == spec["vcodec"],
             f"期望 {spec['vcodec']}，实测 {facts.get('vcodec')}")
    if spec.get("acodec"):
        setv("acodec", facts.get("acodec") == spec["acodec"],
             f"期望 {spec['acodec']}，实测 {facts.get('acodec')}")
    if spec.get("channels"):
        ch = {"mono": 1, "stereo": 2}.get(facts.get("channel_layout", ""), 0)
        setv("channels", ch == spec["channels"],
             f"期望 {spec['channels']} 声道，实测 {facts.get('channel_layout')}")
    if spec.get("lufs_target") is not None and facts.get("integrated_lufs") is not None:
        tol = spec.get("lufs_tol", 0.5)
        dev = facts["integrated_lufs"] - spec["lufs_target"]
        setv("integrated_loudness", abs(dev) <= tol,
             f"实测 {facts['integrated_lufs']} LUFS，目标 {spec['lufs_target']} ±{tol}，偏差 {dev:+.1f} LU"
             + ("；超差须二遍归一化（协议 §6）" if abs(dev) > tol else ""))
    if spec.get("tp_max") is not None and facts.get("true_peak_dbtp") is not None:
        setv("true_peak", facts["true_peak_dbtp"] <= spec["tp_max"],
             f"实测 {facts['true_peak_dbtp']} dBTP，上限 {spec['tp_max']} dBTP")

    for item in SENSORY_ITEMS:
        verdicts[f"感官项: {item}"] = {"verdict": "NEEDS_HUMAN",
                                      "detail": "需真实观看或聆听；未验证不得称为通过（PROVISIONAL）"}
    return {"facts": facts, "verdicts": verdicts}


def gen(ff, args, out):
    r = subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", *args, str(out)],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0 or not Path(out).exists():
        print(f"生成失败: {out}\n{r.stderr[-500:]}")
        sys.exit(2)


def selftest(assets_dir):
    ff = find_ffmpeg()
    if not ff:
        print("SKIP: 未找到 ffmpeg（可 pip install imageio-ffmpeg 获得静态二进制），媒体测量层未执行")
        return 0
    assets = Path(assets_dir)
    assets.mkdir(parents=True, exist_ok=True)
    spec = {"width": 1080, "height": 1920, "dur_min": 9, "dur_max": 11,
            "vcodec": "h264", "acodec": "aac", "lufs_target": -16.0,
            "lufs_tol": 0.5, "tp_max": -1.0, "channels": 1}
    base_v = ["-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30:duration=10"]
    base_a = ["-f", "lavfi", "-i", "sine=frequency=440:duration=10"]

    print(f"ffmpeg: {ff}")
    print("== 生成参考件（目标 -16 LUFS / 1080x1920 / 10s / h264+aac）==")
    ref = assets / "ref_1080p916_10s.mp4"
    gen(ff, [*base_v, *base_a, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
             "-ar", "48000", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-shortest"], ref)
    print("== 生成变异件 A（响度违规：+12 dB，无归一化）==")
    loud = assets / "mutation_loudness.mp4"
    gen(ff, [*base_v, *base_a, "-af", "volume=12dB",
             "-ar", "48000", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-shortest"], loud)
    print("== 生成变异件 B（分辨率违规：1920x1080）==")
    wide = assets / "mutation_resolution.mp4"
    gen(ff, ["-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30:duration=10",
             *base_a, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
             "-ar", "48000", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-shortest"], wide)

    results = {}
    ok = True
    for name, path, expect_fail in [("参考件", ref, []),
                                     ("变异件A(响度)", loud, ["integrated_loudness"]),
                                     ("变异件B(分辨率)", wide, ["resolution"])]:
        r = qa_media(ff, path, spec)
        results[name] = r
        fails = [k for k, v in r["verdicts"].items() if v["verdict"] == "MEASURED_FAIL"]
        sensory = [k for k, v in r["verdicts"].items() if v["verdict"] == "NEEDS_HUMAN"]
        print(f"\n-- {name}: {path.name}")
        print(f"   事实: {r['facts']}")
        for k, v in r["verdicts"].items():
            if v["verdict"] != "NEEDS_HUMAN":
                print(f"   [{v['verdict']}] {k}: {v['detail']}")
        print(f"   NEEDS_HUMAN 感官项: {len(sensory)} 项（恒为待人工）")
        if name == "参考件":
            good = not fails and len(sensory) == len(SENSORY_ITEMS)
            print(f"   断言: 无 MEASURED_FAIL 且感官项齐全 -> {'PASS' if good else 'FAIL'}")
            ok &= good
        else:
            good = all(e in fails for e in expect_fail)
            print(f"   断言: 必须检出 {expect_fail} -> 实际检出 {fails} -> {'PASS' if good else 'FAIL'}")
            ok &= good

    print("\n== 自检结论 ==")
    print("媒体测量层: 参考件全项测量通过；两个变异件被对应规则检出；感官项恒为 NEEDS_HUMAN。"
          if ok else "媒体测量层: 存在未达预期，见上方断言行")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--media")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--assets", default=str(Path(__file__).parent / "media_selftest" / "assets"))
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--dur-min", type=float)
    ap.add_argument("--dur-max", type=float)
    ap.add_argument("--vcodec")
    ap.add_argument("--acodec")
    ap.add_argument("--lufs-target", type=float)
    ap.add_argument("--lufs-tol", type=float, default=0.5)
    ap.add_argument("--tp-max", type=float, default=-1.0)
    ap.add_argument("--channels", type=int)
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest(args.assets))

    if not args.media:
        ap.error("需要 --media <文件> 或 --selftest")
    ff = find_ffmpeg()
    if not ff:
        print("错误: 未找到 ffmpeg（可 pip install imageio-ffmpeg 获得静态二进制）")
        sys.exit(2)
    if not Path(args.media).exists():
        print(f"错误: 文件不存在 {args.media}")
        sys.exit(2)
    spec = {"width": args.width, "height": args.height, "dur_min": args.dur_min,
            "dur_max": args.dur_max, "vcodec": args.vcodec, "acodec": args.acodec,
            "lufs_target": args.lufs_target, "lufs_tol": args.lufs_tol,
            "tp_max": args.tp_max, "channels": args.channels}
    result = qa_media(ff, args.media, spec)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if any(v["verdict"] == "MEASURED_FAIL" for v in result["verdicts"].values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
