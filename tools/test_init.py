#!/usr/bin/env python3
"""Regression tests for first-run setup."""
import json
import os
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import init as setup


def main():
    with tempfile.TemporaryDirectory() as td:
        cfg = Path(td) / "config.json"

        old_ak = os.environ.pop("LOVART_ACCESS_KEY", None)
        old_sk = os.environ.pop("LOVART_SECRET_KEY", None)
        try:
            c = setup.initialize(identity="default", lovart="no", path=cfg)
            assert c["initialized"] is True
            assert c["identity"]["mode"] == "default"
            assert c["identity"]["reference"] == setup.DEFAULT_IDENTITY
            assert c["generation"]["enabled"] is False
            assert "access" not in cfg.read_text()
            assert "secret" not in cfg.read_text()

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
            assert c["identity"]["reference"] == str(custom.resolve())
            assert c["generation"]["enabled"] is True
            raw = cfg.read_text(encoding="utf-8")
            assert "ak_test" not in raw and "sk_test" not in raw
            print("OK: first-run setup regression tests passed")
        finally:
            if old_ak is not None:
                os.environ["LOVART_ACCESS_KEY"] = old_ak
            if old_sk is not None:
                os.environ["LOVART_SECRET_KEY"] = old_sk


if __name__ == "__main__":
    main()
