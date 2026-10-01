#!/usr/bin/env python3
"""Cover Brief -> Prompt compiler (stdlib-only, zero deps).

    python3 tools/compile_prompt.py <brief.json> [--output out.txt] [--failure F0X]

Reads a validated Cover Brief JSON and emits a ready-to-send Lovart prompt.
One section per contract: copy lock -> ALLOWED TEXT, identity -> FACE,
asset -> ASSET FIDELITY, layout -> LAYOUT, style -> STYLE.

--failure <code> re-locks ONLY the section that owns that failure (see
references/failure-codes.md) so a retry changes one layer, not the whole
prompt.
"""
import argparse
import json
import sys
import os

FAILURE_LAYER = {
    "F01": "identity", "F02": "copy", "F03": "asset", "F04": "asset",
    "F05": "layout", "F06": "content", "F07": "quality", "F08": "copy",
    "F09": "ratio", "F10": "style",
}
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


def render(b: dict) -> str:
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

    blocks = []
    blocks.append(
        f"Create a {ratio} horizontal Chinese WeChat official-account cover for QIUQIU, "
        f"canvas {size}."
    )
    blocks.append("")
    # ARTICLE
    blocks.append("ARTICLE (facts only, from the article): " + content.get("topic", ""))
    blocks.append("")
    # COPY + ALLOWED TEXT  (Copy Lock: single source = copy.allowed_text,
    # NOT recomputed from content.*)
    blocks.append("COPY (exact, no added words):")
    for s in allowed:
        blocks.append(f"- {s}")
    blocks.append("ALLOWED TEXT ONLY (the image may contain ONLY these strings, nothing else):")
    for s in allowed:
        blocks.append(f"  「{s}」")
    blocks.append("No other Chinese / English / decorative / fake-label / UI / sign / packaging text.")
    blocks.append("")
    # FACE (identity)
    if identity.get("enabled") is not False:
        blocks.append("REFERENCE ROLES:")
        mask = "keep the face mask" if identity.get("mask", True) else "no face mask"
        blocks.append(
            "- Image 1 (Identity Layer) = QIUQIU's face ONLY. Reproduce the EXACT same face from "
            "the reference: same features, black hair/haircut, skin, age. Do NOT restyle, "
            f"beautify, slim, sharpen jaw, age-shift; {mask}.")
    blocks.append(
        "- Image 2 (Brand Layer) = style ONLY (pixel UI, wood, palette, lights). Do NOT copy its "
        "text, person, logo, specific product.")
    blocks.append("")
    # ASSET FIDELITY (Asset Contract, by level)
    if assets:
        blocks.append("ASSET FIDELITY:")
        for a in assets:
            lvl = int(a.get("fidelity", 0))
            if lvl >= 2:
                blocks.append(
                    f"  - {a.get('id')} (level {lvl}): authoritative. Do NOT redraw, recolor, "
                    "simplify, replace or modify. Position/size may change only.")
            else:
                blocks.append(f"  - {a.get('id')} (level {lvl}): may be approximated/stylized.")
        blocks.append("")
    # STYLE
    blocks.append("STYLE: " + (style.get("note") or STYLE_FIXED))
    blocks.append("")
    # LAYOUT
    blocks.append(f"LAYOUT: {tpl} template — {LAYOUT_NOTE.get(tpl, '')}")
    blocks.append("")
    # TYPOGRAPHY
    blocks.append("TYPOGRAPHY: bold square pixel display type, main title largest, clear "
                  "outline/shadow, exact Chinese glyphs.")
    blocks.append("")
    # NEGATIVE (allowed/invented constraints)
    blocks.append("NEGATIVE: no unauthorized Chinese/English text, no invented products/logos, no "
                  "cartoon/doll/celebrity face, no dark tech mood, keep the overall style consistent.")
    blocks.append("")

    # ---- edit mode ----
    if edit.get("enabled"):
        scope = edit.get("scope", "TEXT_ONLY")
        blocks.append(f"EDIT MODE / EDIT_SCOPE = {scope}")
        blocks.append("Preserve all untouched regions exactly; change only the "
                      f"{scope.lower().replace('_',' ')} scope.")
    return "\n".join(blocks)


def main():
    ap = argparse.ArgumentParser(description="compile a Cover Brief JSON to a Lovart prompt")
    ap.add_argument("brief", help="path to cover-brief.json")
    ap.add_argument("--output", "-o", help="write prompt to file")
    ap.add_argument("--failure", "-f", help="failure code to re-patch, e.g. F03")
    args = ap.parse_args()

    try:
        with open(args.brief, encoding="utf-8") as fh:
            brief = json.load(fh)
    except Exception as e:
        print(f"cannot read brief: {e}"); return 1

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import validate_brief as vb
    if not vb.validate(brief):
        print("brief invalid:")
        for e in vb.ERRORS:
            print("  - " + e)
        return 1

    preview = render(brief)  # build prompt
    if args.failure:
        if args.failure not in FAILURE_LAYER:
            print(f"unknown failure code {args.failure}"); return 2
        # re-lock the owning section (directional re-patch). For copy: reassert allowed text.
        layer = FAILURE_LAYER[args.failure]
        # simplest honest directive: recompile the full prompt but lock
        # identity / copy verbatim on relevant failure classes
        tip = {
            "copy": "ALLOWED TEXT ONLY - the image may only contain the exact whitelist; "
                    "no extra Chinese. Re-check & fix every glyph.",
            "identity": "FACE: freeze to Image 1 exactly; do not reface / alter / wander.",
            "asset": "Real product reference: keep exactly, only reposition."
        }.get(layer, "")
        preview += "\n\nFix focus (" + args.failure + "): " + (tip or "fix only the failing layer")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(preview + "\n")
        print(f"wrote {args.output}")
    else:
        print(preview)
    return 0


if __name__ == "__main__":
    sys.exit(main())
