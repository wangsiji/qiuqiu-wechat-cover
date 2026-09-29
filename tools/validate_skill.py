#!/usr/bin/env python3
"""Small dependency-free validator for this distributable Codex-style skill."""

from pathlib import Path
import re
import subprocess
import sys


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    required_files = (
        "SKILL.md",
        "README.md",
        "agents/openai.yaml",
        "references/workflow.md",
        "references/style-guide.md",
        "references/prompt-template.md",
        "references/prompt-checklist.md",
        "references/assets/qiuqiu-face-reference.jpg",
        "references/assets/qiuqiu-style-reference.png",
        "tools/resolve_assets.py",
    )
    for relative in required_files:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill = root / "SKILL.md"
    skill_text = ""
    if not skill.is_file():
        errors.append("missing SKILL.md")
    else:
        skill_text = skill.read_text(encoding="utf-8")
        if not skill_text.startswith("---\n"):
            errors.append("SKILL.md must start with YAML frontmatter")
        else:
            closing = skill_text.find("\n---", 4)
            frontmatter = skill_text[4:closing] if closing != -1 else ""
            if closing == -1:
                errors.append("SKILL.md frontmatter is not closed")
            for field in ("name", "description"):
                match = re.search(rf"^{field}:\s*(.+)$", frontmatter, re.MULTILINE)
                if not match or not match.group(1).strip().strip('"\''):
                    errors.append(f"frontmatter field is missing: {field}")

    for markdown in root.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "/")):
                continue
            if not (markdown.parent / target).exists():
                errors.append(f"broken relative link in {markdown.relative_to(root)}: {target}")

    agent_config = root / "agents" / "openai.yaml"
    if agent_config.exists():
        agent_text = agent_config.read_text(encoding="utf-8")
        if "interface:" not in agent_text:
            errors.append("agents/openai.yaml is missing interface section")
        if "$qiuqiu-wechat-cover" not in agent_text:
            errors.append("agents/openai.yaml default_prompt must mention $qiuqiu-wechat-cover")

    # Validate bundled image assets really resolve.
    identity = root / "references/assets/qiuqiu-face-reference.jpg"
    style = root / "references/assets/qiuqiu-style-reference.png"

    def check_image(path: Path, label: str, magic: bytes, min_size: int) -> None:
        if not path.is_file():
            return  # already reported above
        data = path.read_bytes()
        if len(data) < min_size:
            errors.append(f"{label} looks unexpectedly small ({len(data)} bytes)")
        if not data.startswith(magic):
            errors.append(f"{label} is not a valid image (bad file signature)")

    check_image(identity, "identity reference", b"\xff\xd8\xff", 10_000)
    check_image(style, "style reference", b"\x89PNG\r\n\x1a\n", 10_000)

    # Run the resolver to confirm it actually finds and reads the assets.
    resolver = root / "tools" / "resolve_assets.py"
    if resolver.is_file():
        try:
            result = subprocess.run(
                [sys.executable, str(resolver)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                errors.append("tools/resolve_assets.py failed to resolve bundled assets")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"tools/resolve_assets.py could not run: {exc}")

    required_phrases = (
        "2.35:1",
        "references/workflow.md",
        "references/prompt-template.md",
        "tools/resolve_assets.py",
        "qiuqiu-face-reference.jpg",
        "qiuqiu-style-reference.png",
        "待确认",
    )
    for phrase in required_phrases:
        if phrase not in skill_text:
            errors.append(f"SKILL.md is missing required guidance: {phrase}")

    # Lovart execution-channel contract: SKILL.md must reference the bundled
    # backend (tools/lovart-agent.py), and that file must exist and stay
    # stdlib-only so the skill is self-contained on any clean clone.
    lovart_skill_ref = "tools/lovart-agent.py"
    if "Lovart 出图通道" not in skill_text and "references/lovart-channel.md" not in skill_text:
        errors.append("SKILL.md must link the Lovart 出图通道 (or references/lovart-channel.md)")
    elif lovart_skill_ref not in skill_text:
        errors.append(
            f"SKILL.md Lovart section must reference the bundled backend {lovart_skill_ref} "
            "(it used to point at an absolute ~/.codex path that broke on other machines)"
        )
    lovart_script = root / "tools" / "lovart-agent.py"
    if not lovart_script.is_file():
        errors.append("missing bundled backend: tools/lovart-agent.py")
    else:
        script_text = lovart_script.read_text(encoding="utf-8", errors="replace")
        # Enforce stdlib-only imports: split on known stdlib set. If any other
        # import appears, the bundle is not portable.
        allowed = {
            "hashlib", "hmac", "json", "ssl", "time", "urllib", "uuid",
            "typing", "os", "sys", "argparse", "pathlib", "datetime", "re", "collections",
        }
        for line in script_text.splitlines():
            if line.startswith(("import ", "from ")):
                top = line.split()[1].split(".")[0]
                if top not in allowed:
                    errors.append(f"tools/lovart-agent.py has non-stdlib import: {line.strip()}")

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Skill validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

