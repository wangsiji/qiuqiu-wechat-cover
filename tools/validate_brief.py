#!/usr/bin/env python3
"""Validate a Cover Brief JSON (stdlib-only, zero deps).

Structural rules mirror references/cover-brief.schema.json. Business rules
remain here because JSON Schema alone does not express category/template
mapping, fidelity floors, Copy Lock confirmation, or cross-field uniqueness.
"""
import json, re, sys

VALID = {"L01","L02","L03","L04","L05"}
CAT2TPL = {
    "product":"L02","goods":"L02","comparison":"L04","ai":"L04",
    "travel":"L03","personal":"L01","tutorial":"L05","learning":"L05","desk":"L05",
}
MIN_FIDELITY = {
    "logo": 3, "brand_asset": 3,
    "real_product": 2, "real_subject": 2, "travel_photo": 2,
    "screenshot": 2, "decorative": 0,
}
INPUT_RE = re.compile(r"^image_(?:[3-9]|[1-9][0-9]+)$")
ERRORS = []


def _err(m): ERRORS.append(m)


def validate(brief):
    ERRORS.clear()
    if not isinstance(brief, dict):
        _err("top-level must be an object"); return False
    ok = True

    c = brief.get("cover")
    if not isinstance(c, dict) or not isinstance(c.get("size"), str) or not re.fullmatch(r"[0-9]+x[0-9]+", c.get("size", "")):
        _err("cover.size required as 'WxH', e.g. 1880x800"); ok = False
    if (c or {}).get("ratio") != "2.35:1":
        _err("cover.ratio must be exactly '2.35:1'"); ok = False

    ct = brief.get("content")
    if not isinstance(ct, dict):
        _err("content required"); ok = False
    else:
        for f in ("topic",):
            if not isinstance(ct.get(f), str) or not ct[f]:
                _err(f"content.{f} must be a non-empty string"); ok = False
        cat = ct.get("category")
        if cat not in CAT2TPL:
            _err(f"content.category '{cat}' unknown"); ok = False
        tpl = (brief.get("layout") or {}).get("template")
        if cat in CAT2TPL and tpl and tpl != CAT2TPL[cat]:
            _err(f"layout.template {tpl} != default {CAT2TPL[cat]} for category {cat}"); ok = False

    cp = brief.get("copy")
    if not isinstance(cp, dict):
        _err("copy required (Copy Lock)"); ok = False
    else:
        at = cp.get("allowed_text")
        if not isinstance(at, list) or not at or not all(isinstance(x, str) and x for x in at):
            _err("copy.allowed_text must be a non-empty array of non-empty strings"); ok = False
        if cp.get("status") != "confirmed":
            _err("copy.status must be 'confirmed' before generation"); ok = False
        if isinstance(at, list) and len(set(at)) != len(at):
            _err("copy.allowed_text must not contain duplicates"); ok = False

    i = brief.get("identity")
    if not isinstance(i, dict) or not isinstance(i.get("enabled"), bool) or not isinstance(i.get("mask"), bool):
        _err("identity.enabled and identity.mask must be boolean"); ok = False

    st = brief.get("style")
    if not isinstance(st, dict) or not isinstance(st.get("reference"), str):
        _err("style.reference must be a string"); ok = False
    pixel = (st or {}).get("pixel_ratio")
    if pixel is not None and not (isinstance(pixel, (int, float)) and not isinstance(pixel, bool) and 0 <= pixel <= 1):
        _err("style.pixel_ratio must be 0..1"); ok = False

    ly = brief.get("layout")
    if not isinstance(ly, dict) or ly.get("template") not in VALID:
        _err(f"layout.template must be one of {sorted(VALID)}"); ok = False

    seen_ids, seen_inputs = set(), set()
    for idx, a in enumerate(brief.get("assets") or []):
        if not isinstance(a, dict):
            _err(f"assets[{idx}] must be an object"); ok = False; continue
        aid = a.get("id")
        if not isinstance(aid, str) or not aid:
            _err(f"assets[{idx}].id must be a non-empty string"); ok = False
        elif aid in seen_ids:
            _err(f"assets[{idx}]({aid}).id duplicated"); ok = False
        else:
            seen_ids.add(aid)
        fid = a.get("fidelity")
        if not isinstance(fid, int) or isinstance(fid, bool) or fid not in (0, 1, 2, 3):
            _err(f"assets[{idx}]({aid}).fidelity must be integer 0..3"); ok = False
        inp = a.get("input")
        if not isinstance(inp, str) or not INPUT_RE.fullmatch(inp):
            _err(f"assets[{idx}]({aid}).input must match image_3, image_4, ..."); ok = False
        elif inp in seen_inputs:
            _err(f"assets[{idx}]({aid}).input '{inp}' is already bound to another asset"); ok = False
        else:
            seen_inputs.add(inp)
        kind = a.get("kind")
        if kind not in MIN_FIDELITY:
            _err(f"assets[{idx}]({aid}).kind unknown"); ok = False
        elif isinstance(fid, int) and not isinstance(fid, bool) and fid < MIN_FIDELITY[kind]:
            _err(f"assets[{idx}]({aid}).fidelity {fid} below {kind}'s floor {MIN_FIDELITY[kind]} (Asset Contract)"); ok = False

    edit = brief.get("edit")
    if isinstance(edit, dict) and edit.get("enabled"):
        if edit.get("scope") not in ("TEXT_ONLY","PRODUCT_ONLY","PERSON_ONLY","BACKGROUND_ONLY","FULL"):
            _err("edit.scope invalid when edit.enabled"); ok = False
        target = edit.get("target")
        if target and target.get("type") == "asset":
            if target.get("value") not in seen_ids:
                _err(f"edit.target asset '{target.get('value')}' not found in assets"); ok = False

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
