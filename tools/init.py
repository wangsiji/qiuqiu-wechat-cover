#!/usr/bin/env python3
"""First-run setup for qiuqiu-wechat-cover.

Stores only non-secret preferences in ~/.qiuqiu-wechat-cover/config.json.
Lovart credentials are never written to this file; they are read only from
LOVART_ACCESS_KEY / LOVART_SECRET_KEY in the current runtime environment.

Agent runtimes should use --check (or --bootstrap) as a status probe and follow
references/agent-bootstrap.md for the user-facing initialization conversation.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Optional

DEFAULT_CONFIG_DIR = Path.home() / ".qiuqiu-wechat-cover"
DEFAULT_CONFIG = DEFAULT_CONFIG_DIR / "config.json"
DEFAULT_IDENTITY = "references/assets/qiuqiu-face-reference.jpg"
DEFAULT_STYLE = "references/assets/qiuqiu-style-reference.png"
CONFIG_VERSION = 2


def load_config(path: Path = DEFAULT_CONFIG) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read config {path}: {exc}")


def save_config(config: dict, path: Path = DEFAULT_CONFIG) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def credentials_status() -> str:
    has_access = bool(os.environ.get("LOVART_ACCESS_KEY"))
    has_secret = bool(os.environ.get("LOVART_SECRET_KEY"))
    if has_access and has_secret:
        return "configured"
    if has_access or has_secret:
        return "partial"
    return "missing"


def credentials_configured() -> bool:
    return credentials_status() == "configured"


def resolve_identity(choice: str, custom: Optional[str]) -> str:
    if choice == "default":
        return DEFAULT_IDENTITY
    if not custom:
        raise SystemExit("Custom identity requires --identity-path.")
    p = Path(custom).expanduser()
    if not p.is_file():
        raise SystemExit(f"Identity reference does not exist: {p}")
    return str(p.resolve())


def setup_status(path: Path = DEFAULT_CONFIG) -> dict:
    config = load_config(path)
    initialized = bool(config.get("initialized"))
    generation = config.get("generation", {})
    provider = generation.get("provider", "lovart")
    enabled = bool(generation.get("enabled", False))
    cred_status = credentials_status() if provider == "lovart" else "not_applicable"

    if not initialized:
        next_action = "ask_identity_and_generation"
    elif provider == "lovart" and enabled and cred_status != "configured":
        next_action = "configure_lovart_credentials"
    else:
        next_action = "continue_workflow"

    return {
        "initialized": initialized,
        "identity": config.get("identity", {}),
        "generation": {
            "provider": provider,
            "enabled": enabled,
            "credentials_source": generation.get("credentials_source", "environment"),
            "credentials_status": cred_status,
        },
        "lovart_credentials_configured": credentials_configured(),
        "needs_setup": next_action != "continue_workflow",
        "next_action": next_action,
        "config_path": str(path),
    }


def initialize(
    *,
    identity: str = "default",
    custom_identity: Optional[str] = None,
    lovart: str = "auto",
    path: Path = DEFAULT_CONFIG,
) -> dict:
    config = load_config(path)

    if identity == "custom":
        identity_ref = resolve_identity("custom", custom_identity)
        identity_mode = "custom"
    else:
        identity_ref = DEFAULT_IDENTITY
        identity_mode = "default"

    if lovart not in {"auto", "yes", "no"}:
        raise SystemExit("lovart must be one of: auto, yes, no")

    if lovart == "yes":
        if not credentials_configured():
            raise SystemExit(
                "Lovart selected, but credentials are not configured. "
                "Set LOVART_ACCESS_KEY and LOVART_SECRET_KEY, then rerun init."
            )
        lovart_enabled = True
    elif lovart == "no":
        lovart_enabled = False
    else:
        lovart_enabled = credentials_configured()

    config.update(
        {
            "version": CONFIG_VERSION,
            "initialized": True,
            "identity": {"mode": identity_mode, "reference": identity_ref},
            "generation": {
                "provider": "lovart",
                "enabled": lovart_enabled,
                "credentials_source": "environment",
            },
        }
    )
    save_config(config, path)
    return config


def interactive(path: Path) -> dict:
    existing = load_config(path)
    if existing.get("initialized"):
        return existing

    print("qiuqiu-wechat-cover 首次使用初始化")
    print()
    print("1. 人物身份")
    print("  [1] 使用默认「秋秋」人物")
    print("  [2] 替换为自己的真人身份图")
    identity_choice = input("请选择 [1/2]（默认 1）：").strip() or "1"

    if identity_choice == "2":
        custom = input("请输入 identity reference 图片路径：").strip()
        identity = "custom"
    else:
        identity, custom = "default", None

    print()
    print("2. Lovart 图片生成")
    print("  [1] 使用 Lovart")
    print("  [2] 暂不配置 Lovart，先使用 Brief / Prompt 工作流")
    lovart_choice = input("请选择 [1/2]（默认 1）：").strip() or "1"

    if lovart_choice == "1" and not credentials_configured():
        print()
        print("已选择 Lovart，但当前环境没有完整的 Lovart 密钥。")
        print("请通过当前智能体支持的安全 Secret / 环境变量配置：")
        print("  LOVART_ACCESS_KEY")
        print("  LOVART_SECRET_KEY")
        print("不要把 API Key / Secret 直接发送到聊天中。")
        raise SystemExit(2)

    return initialize(
        identity=identity,
        custom_identity=custom,
        lovart="yes" if lovart_choice == "1" else "no",
        path=path,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize qiuqiu-wechat-cover")
    parser.add_argument("--path", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--identity", choices=["default", "custom"])
    parser.add_argument("--identity-path", dest="custom_identity")
    parser.add_argument("--lovart", choices=["yes", "no", "auto"], default="auto")
    parser.add_argument(
        "--check", "--bootstrap", dest="check", action="store_true",
        help="Print machine-readable first-run/bootstrap status without secrets",
    )
    args = parser.parse_args()

    if args.check:
        print(json.dumps(setup_status(args.path), ensure_ascii=False, indent=2))
        return

    if args.identity:
        config = initialize(
            identity=args.identity,
            custom_identity=args.custom_identity,
            lovart=args.lovart,
            path=args.path,
        )
    else:
        config = interactive(args.path)

    print(json.dumps(config, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
