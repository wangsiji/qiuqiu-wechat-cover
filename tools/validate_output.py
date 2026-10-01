#!/usr/bin/env python3
"""Machine gate for a generated cover (stdlib-only).

Checks file existence, PNG/JPEG headers, dimensions and target aspect ratio.
Visual items such as face identity, Chinese text accuracy, asset fidelity,
composition and style remain human/vision checks.
"""
import argparse, os

def inspect(path):
    with open(path, "rb") as fh: head = fh.read(24)
    if head[:8] == b"\x89PNG\r\n\x1a\n": return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big"), "png"
    if len(head) >= 3 and head[:2] == b"\xff\xd8":
        data = open(path, "rb").read(); i, L = 2, len(data)
        while i + 9 < L:
            if data[i] != 0xFF: i += 1; continue
            m = data[i + 1]
            if m in (0xC0, 0xC2): return int.from_bytes(data[i+7:i+9], "big"), int.from_bytes(data[i+5:i+7], "big"), "jpeg"
            seg = int.from_bytes(data[i+2:i+4], "big"); i += 2 + seg
    return None, None, None

def validate(path, target_ratio=2.35, tol=0.10):
    if not os.path.isfile(path): return False, [f"file not found: {path}"]
    if os.path.getsize(path) == 0: return False, ["zero-byte file"]
    w, h, kind = inspect(path)
    if kind is None: return False, ["not a decodable PNG/JPEG"]
    if not w or not h: return False, ["could not read dimensions"]
    print(f"info: {kind} {w}x{h}  ratio {w/h:.3f}")
    r = w / h; lo, hi = target_ratio - tol, target_ratio + tol
    return (lo <= r <= hi, [] if lo <= r <= hi else [f"ratio {r:.3f} outside [{lo:.3f},{hi:.3f}] (F09)"])

def main():
    ap = argparse.ArgumentParser(description="machine gate a generated cover")
    ap.add_argument("image"); ap.add_argument("--expect-ratio", "-r", type=float, default=2.35)
    args = ap.parse_args(); ok, errs = validate(args.image, args.expect_ratio)
    if not ok:
        print("FAIL  " + args.image)
        for e in errs: print("  - " + e)
        return 1
    print("OK    " + args.image + "  (machine gate passed)"); return 0

if __name__ == "__main__": raise SystemExit(main())
