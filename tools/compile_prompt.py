#!/usr/bin/env python3
"""Cover Brief -> Prompt compiler (stdlib-only, zero deps).

    python3 tools/compile_prompt.py <brief.json> [--output out.txt] [--failure F0X]

Emits a ready-to-send Lovart prompt from a validated Cover Brief.
Each contract emits its OWN section; the prompt is the sections reassembled
in a fixed order.

--failure <code>: real section patch. Loads references/failure-codes.json,
replaces ONLY the section that owns that failure code, and reassembles. The
other sections stay byte-identical. code->section map lives in that JSON
(single source of truth), not here.
"""
import argparse
import json
import sys
import os

LAYOUT_NOTE = {
    "L01": "headline ~45%, person ~40%, decoration ~15%",
    "L02": "headline ~35%, product ~45%, person ~20%",
    "L03": "headline ~35%, route/map ~45%, person ~20%",
    "L04": "headline ~40%, three products ~45%, person ~15%",
    "L05": "headline ~40%, scene ~60%, no person",
}
STYLE_FIXED = ("warm wooden pixel-game study/desk, bright warm window light, "
               "cream/purple/pink accents, cozy lively, real person + real objects "
               "integrated with soft pixel atmosphere")

# section id used in the json failure map -> section key rendered here
SECTION_ALIAS = {"ratio": "opener"}

ORDER = ["opener", "article", "copy", "ref_roles", "asset_fidelity",
         "style", "layout", "typography", "negative", "edit"]


def render_sections(b: dict) -> dict:
    cv = b.get("cover", {})
    ratio = cv.get("ratio", "2.35:1")
    size = cv.get("size", "1880x800")
    content = b.get("content", {})
    copy = b.get("copy", {})
    identity = b.get("identity", {})
    style = b.get("style", {})
    layout = b.get("layout", {})
    edit = b.get("edit", {})
    tpl = layout.get("template", "L02")
    assets = b.get("assets") or []
    allowed = copy.get("allowed_text") or []

    s = {}
    s["opener"] = (f"Create a {ratio} horizontal Chinese WeChat official-account cover "
                   f"for QIUQIU, canvas {size}.")
    s["article"] = "ARTICLE (facts only, from the article): " + content.get("topic", "")
    # copy lock
    c = ["COPY (exact, no added words):"] + [f"- {x}" for x in allowed]
    c.append('ALLOWED TEXT ONLY (the image may contain ONLY these strings, nothing else):')
    c += [f"  \u300c{x}\u300d" for x in allowed]
    c.append("No other Chinese / English / decorative / fake-label / UI / sign / packaging text.")
    s["copy"] = "\n".join(c)
    # reference roles
    r = ["REFERENCE ROLES:"]
    if identity.get("enabled") is not False:
        mask = "keep the face mask" if identity.get("mask", True) else "no face mask"
        r.append("- Image 1 (Identity): QIUQIU face ONLY. Reproduce the EXACT same face "
                 "from the reference (features, black hair/haircut, skin, age); no restyle, "
                 f"beautify, slim, jaw-sharpen, age-shift; {mask}.")
    r.append("- Image 2 (Brand): style ONLY (pixel UI, wood, palette, lights). Do NOT copy its "
             "text/person/logo/specific product.")
    s["ref_roles"] = "\n".join(r)
    # asset fidelity
    if assets:
        s["asset_fidelity"] = "ASSET FIDELITY (per asset, machine-bound by input/image role):\n" + \
            "\n".join(_slug_asset(a, i) for i, a in enumerate(assets))
    # style / layout / typography / negative
    s["style"] = "STYLE: " + (style.get("note") or STYLE_FIXED)
    s["layout"] = f"LAYOUT: {tpl} template — {LAYOUT_NOTE.get(tpl, '')}"
    s["typography"] = ("TYPOGRAPHY: bold square pixel display type, main title largest, "
                       "clear outline/shadow, exact Chinese glyphs.")
    s["negative"] = ("NEGATIVE: no unauthorized Chinese/English text, no invented products/logos, "
                     "no cartoon/doll/celebrity face, no dark tech mood, keep the overall style "
                     "consistent.")
    # edit
    if edit.get("enabled"):
        scope = edit.get("scope", "TEXT_ONLY")
        tgt = edit.get("target", {})
        e = [f"EDIT MODE / EDIT_SCOPE = {scope}"]
        if tgt.get("type") == "asset" and tgt.get("value"):
            e.append(f"TARGET: asset {tgt['value']}")
            e.append("CHANGE: only modify that asset.")
        e.append("PRESERVE: all other assets, person/face, text, background, lighting, layout.")
        e.append("Preserve all untouched regions as closely as the edit model allows.")
        s["edit"] = "\n".join(e)
    return s


def _slug_asset(a, i):
    ref = a.get("input") or f"image_{i + 3}"   # image_3, image_4, ...
    lvl = int(a.get("fidelity", 0))
    if lvl >= 2:
        role = ("authoritative. Do NOT redraw, recolor, deform, simplify, replace or "
                "modify. Position/size only.")
    else:
        role = "decorative; may be approximated/stylized."
    return f"- {ref} ({a.get('id')}, level {lvl}, input-attached as prompt&goods): {role}"


def assemble(s: dict) -> str:
    parts = []
    for k in ORDER:
        if k in s and s[k]:
            parts.append(s[k])
    return "\n\n".join(parts)


def apply_failure(sec: dict, code, patches) -> dict:
    """Replace exactly the section owning <code> with its patch; others untouched."""
    entry = patches.get(code)
    if not entry:
        return sec
    section = SECTION_ALIAS.get(entry["section"], entry["section"])
    out = dict(sec)
    if section in out:
        out[section] = entry["patch"]  # replace whole section
    else:
        out[section] = entry["patch"]  # add (e.g. ratio when opener was defaulted)
    return out


def load_failures(repo_root):
    p = os.path.join(repo_root, "references", "failure-codes.json")
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser(description="compile a Cover Brief to a Lovart prompt")
    ap.add_argument("brief")
    ap.add_argument("--output", "-o", help="write prompt to file")
    ap.add_argument("--failure", "-f", help="failure code to patch, e.g. F03")
    args = ap.parse_args()

    try:
        with open(args.brief, encoding="utf-8") as fh:
            brief = json.load(fh)
    except Exception as e:
        print(f"cannot read brief: {e}"); return 1

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(root, "tools"))
    import validate_brief as vb
    if not vb.validate(brief):
        print("brief invalid:")
        for e in vb.ERRORS:
            print("  - " + e)
        return 1

    sec = render_sections(brief)
    if args.failure:
        fc = load_failures(root)
        sec = apply_failure(sec, args.failure, fc)

    text = assemble(sec)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
