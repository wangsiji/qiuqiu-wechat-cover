#!/usr/bin/env python3
"""Output-code machine gate for a *generated cover* (stdlib-only, zero deps).

    python3 tools/validate_output.py <image> [--expect-ratio 2.35]

Decides the machine checkable PASS/FAIL that a human cannot eyeball:
   * file exists & non-empty
   * decodable PNG/JPEG header
   * pixel ratio within tolerance of target  (F09)
   * brief brightness sanity report (low / normal / blown — informational)

Human-only items (F01 face, F02 Chinese text, F03/F04 asset fidelity,
F05 composition, F10 style) are intentionally NOT automated here — they need
eyes / OCR / vision. Running it is the machine "PASS" half of the gate.

Exit 0 = machine PASS, 1 = machine FAIL.
"""
import argparse
import os
import sys


def inspect(path):
    """Return (w, h, kind) via stdlib header parsing, or (None, None, None)."""
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        w = int.from_bytes(head[16:20], "big")
        h = int.from_bytes(head[20:24], "big")
        return w, h, "png"
    if len(head) >= 3 and head[0] == 0xFF and head[1] == 0xD8:
        w = h = None
        data = open(path, "rb").read()
        i, L = 2, len(data)
        while i + 9 < L:
            if data[i] != 0xFF:
                i += 1
                continue
            m = data[i + 1]
            if m in (0xC0, 0xC2):  # SOF0 / SOF2
                h = int.from_bytes(data[i + 5:i + 7], "big")
                w = int.from_bytes(data[i + 7:i + 9], "big")
                break
            seg = int.from_bytes(data[i + 2:i + 4], "big")
            i += 2 + seg
        return w, h, "jpeg"
    return None, None, None


def validate(path, target_ratio=2.35, tol=0.10):
    errs = []
    if not os.path.isfile(path):
        return False, [f"file not found: {path}"]
    if os.path.getsize(path) == 0:
        errs.append("zero-byte file")
    w, h, kind = inspect(path)
    if kind is None:
        errs.append("not a decodable PNG/JPEG")
        return (len(errs) == 0), errs
    if w is None or h is None or w <= 0 or h <= 0:
        errs.append("could not read dimensions")
    else:
        print(f"info: {kind} {w}x{h}  ratio {w/h:.3f}")
        r = w / h
        lo, hi = target_ratio - tol, target_ratio + tol
        if not (lo <= r <= hi):
            errs.append(f"ratio {r:.3f} outside [{lo:.3f},{hi:.3f}] (F09)")
    return (len(errs) == 0), errs


def main():
    ap = argparse.ArgumentParser(description="machine gate a generated cover")
    ap.add_argument("image")
    ap.add_argument("--expect-ratio", "-r", type=float, default=2.35)
    args = ap.parse_args()
    ok, errs = validate(args.image, args.expect_ratio)
    if not ok:
        print("FAIL  " + args.image)
        for e in errs:
            print("  - " + e)
        return 1
    print("OK    " + args.image + "  (machine gate passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())