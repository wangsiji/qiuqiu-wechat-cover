#!/usr/bin/env python3
"""Regression tests for first-run/bootstrap setup."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import init as setup


def run_check(cfg: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "init.py"),
         "--check", "--path", str(cfg)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def main():
    with tempfile.TemporaryDirectory() as td:
        cfg = Path(td) / "config.json"
        old_ak = os.environ.pop("LOVART_ACCESS_KEY", None)
        old_sk = os.environ.pop("LOVART_SECRET_KEY", None)
        try:
            status = run_check(cfg)
            assert status["initialized"] is False
            assert status["needs_setup"] is True
            assert status["next_action"] == "ask_identity_and_generation"
            assert status["generation"]["credentials_status"] == "missing"

            c = setup.initialize(identity="default", lovart="no", path=cfg)
            assert c["initialized"] is True
            assert c["version"] == 2
            assert c["generation"]["enabled"] is False

            status = run_check(cfg)
            assert status["next_action"] == "continue_workflow"

            try:
                setup.initialize(identity="default", lovart="yes", path=cfg)
            except SystemExit as exc:
                assert exc.code == 1
            else:
                raise AssertionError("Lovart must fail closed without credentials")

            custom = Path(td) / "identity.jpg"
            custom.write_bytes(b"fake")
            os.environ["LOVART_ACCESS_KEY"] = "ak_test"
            os.environ["LOVART_SECRET_KEY"] = "sk_test"
            c = setup.initialize(
                identity="custom",
                custom_identity=str(custom),
                lovart="yes",
                path=cfg,
            )
            assert c["identity"]["mode"] == "custom"
            assert c["generation"]["enabled"] is True

            status = run_check(cfg)
            assert status["next_action"] == "continue_workflow"
            assert status["generation"]["credentials_status"] == "configured"

            raw = cfg.read_text(encoding="utf-8")
            assert "ak_test" not in raw and "sk_test" not in raw
            assert "sk_test" not in json.dumps(status)
            print("OK: first-run/bootstrap regression tests passed")
        finally:
            if old_ak is not None:
                os.environ["LOVART_ACCESS_KEY"] = old_ak
            if old_sk is not None:
                os.environ["LOVART_SECRET_KEY"] = old_sk


if __name__ == "__main__":
    main()
