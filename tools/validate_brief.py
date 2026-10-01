#!/usr/bin/env python3
"""Validate a Cover Brief JSON (stdlib-only, zero deps).

    python3 tools/validate_brief.py path/to/brief.json   -> exit 0 OK / 1 FAIL

Enforces the shape from references/cover-brief.md + schema, plus the business
rules that keep a brief honest: Copy Lock confirmed & non-empty allowed_text,
layout template matches category default, fidelity in 0..3, ratio/size sane.
"""
import json, sys

VALID = {"L01","L02","L03","L04","L05"}
CAT2TPL = {
    "product":"L02","goods":"L02","comparison":"L04","ai":"L04",
    "travel":"L03","personal":"L01",
    "tutorial":"L05","learning":"L05","desk":"L05",
}
# Asset Contract default-protection floor: a kind that is authoritative in the
# docs has a minimum fidelity. Manual override is allowed only via explicit
# ERROR text (raise the value), i.e. raising default is silent, lowering warns.
MIN_FIDELITY = {
    "logo": 3, "brand_asset": 3,
    "real_product": 2, "real_subject": 2, "travel_photo": 2,
    "screenshot": 2, "decorative": 0,
}
ERRORS = []


def _err(m): ERRORS.append(m)


def validate(brief):
    ERRORS.clear()
    if not isinstance(brief, dict):
        _err("top-level must be an object"); return False
    ok = True

    # cover
    c = brief.get("cover")
    if not isinstance(c, dict) or not isinstance(c.get("size"), str) or "x" not in str(c.get("size")):
        _err("cover.size required as 'WxH', e.g. 1880x800"); ok = False
    ratio = (c or {}).get("ratio")
    if ratio != "2.35:1":
        _err("cover.ratio must be exactly '2.35:1' (not e.g. 2.34:1)"); ok = False

    # content
    ct = brief.get("content")
    if not isinstance(ct, dict):
        _err("content required"); ok = False
    else:
        for f in ("topic","hook","title"):
            if not isinstance(ct.get(f), str) or not ct[f]:
                _err(f"content.{f} must be a non-empty string"); ok = False
        cat = ct.get("category")
        if cat not in CAT2TPL:  # keep mapping local
            _err(f"content.category '{cat}' unknown"); ok = False
        tpl = (brief.get("layout") or {}).get("template")
        if cat in CAT2TPL and tpl and tpl != CAT2TPL[cat]:
            _err(f"layout.template {tpl} != default {CAT2TPL[cat]} for category {cat}")

    # copy lock (the whole point)
    cp = brief.get("copy")
    if not isinstance(cp, dict):
        _err("copy required (Copy Lock)"); ok = False
    else:
        at = cp.get("allowed_text")
        if not isinstance(at, list) or not at or not all(isinstance(x, str) and x for x in at):
            _err("copy.allowed_text must be a non-empty array of non-empty strings"); ok = False
        if cp.get("status") != "confirmed":
            _err("copy.status must be 'confirmed' before generation"); ok = False
        # allowed_text must cover hook+title+subtitle (when present)
        if isinstance(at, list) and isinstance(ct, dict):
            for key in ("hook", "title", "subtitle"):
                val = ct.get(key)
                if isinstance(val, str) and val and val not in at:
                    _err(f"copy.allowed_text missing content.{key}='{val}'"); ok = False

    # identity
    i = brief.get("identity")
    if not isinstance(i, dict) or not isinstance(i.get("enabled"), bool) or not isinstance(i.get("mask"), bool):
        _err("identity.enabled and identity.mask must be boolean"); ok = False

    # style
    pixel = (brief.get("style") or {}).get("pixel_ratio")
    if pixel is not None and not (isinstance(pixel, (int, float)) and 0 <= pixel <= 1):
        _err("style.pixel_ratio must be 0..1"); ok = False

    # layout
    if not isinstance(brief.get("layout"), dict) or brief.get("layout", {}).get("template") not in VALID:
        _err(f"layout.template must be one of {sorted(VALID)}"); ok = False

    # assets / fidelity (+ input binding)
    for idx, a in enumerate(brief.get("assets") or []):
        if not isinstance(a, dict):
            _err(f"assets[{idx}] must be an object"); ok = False; continue
        fid = a.get("fidelity")
        if fid not in (0, 1, 2, 3):
            _err(f"assets[{idx}]({a.get('id')}).fidelity must be integer 0..3"); ok = False
        if "input" not in a or not isinstance(a.get("input"), str) or not a["input"].startswith("image_"):
            _err(f"assets[{idx}]({a.get('id')}).input required, e.g. 'image_3' — machine link to attachment"); ok = False
        kind = a.get("kind")
        if kind in MIN_FIDELITY and isinstance(fid, int) and fid < MIN_FIDELITY[kind]:
            _err(f"assets[{idx}]({a.get('id')}).fidelity {fid} below {kind}'s floor {MIN_FIDELITY[kind]} (Asset Contract)"); ok = False

    # edit
    edit = brief.get("edit")
    if isinstance(edit, dict) and edit.get("enabled"):
        if edit.get("scope") not in ("TEXT_ONLY","PRODUCT_ONLY","PERSON_ONLY","BACKGROUND_ONLY","FULL"):
            _err("edit.scope invalid when edit.enabled"); ok = False

    return ok


def main():
    if len(sys.argv) < 2:
        print("usage: validate_brief.py <brief.json>"); return 2
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            brief = json.load(f)
    except Exception as e:
        print(f"FAIL  {path}: cannot read/parse: {e}"); return 1
    ok = validate(brief)
    if not ok:
        print(f"FAIL  {path}")
        for e in ERRORS:
            print("  - " + e)
        return 1
    print(f"OK    {path} (Cover Brief valid)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
