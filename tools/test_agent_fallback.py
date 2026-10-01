#!/usr/bin/env python3
"""Regression: credit-insufficient detection + backup cred resolution.

Uses only the pure helpers in lovart-agent (no network).
"""
import importlib.util
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

def _load():
    path = Path(__file__).resolve().parents[1] / "tools" / "lovart-agent.py"
    spec = importlib.util.spec_from_file_location("lovart_agent_module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

m = _load()

# credit detection
_for = [
    ("Insufficient credits", True),
    ("你的账户积分不足", True),   # multi-byte path
    ("HTTP 400 bad request", False),
    ("", False),
]
for msg, exp in _for:
    got = m._credit_insufficient(m.AgentSkillError(msg, 402))
    assert got == exp, f"expected {exp} for {msg!r}, got {got}"

# backup pool: none set -> []
for k in ("LOVART_BACKUP_ACCESS_KEY", "LOVART_BACKUP_SECRET_KEY",
          "LOVART_BACKUP2_ACCESS_KEY", "LOVART_BACKUP2_SECRET_KEY",
          "LOVART_BACKUP3_ACCESS_KEY", "LOVART_BACKUP3_SECRET_KEY"):
    os.environ.pop(k, None)
assert m._backup_cred_pool() == []

# one backup pair
os.environ["LOVART_BACKUP_ACCESS_KEY"] = "ak_a"
os.environ["LOVART_BACKUP_SECRET_KEY"] = "sk_a"
assert m._backup_cred_pool() == [("ak_a", "sk_a")]

# two backup pairs, in env order
os.environ["LOVART_BACKUP2_ACCESS_KEY"] = "ak_b"
os.environ["LOVART_BACKUP2_SECRET_KEY"] = "sk_b"
assert m._backup_cred_pool() == [("ak_a", "sk_a"), ("ak_b", "sk_b")]

# incomplete second pair is skipped
os.environ.pop("LOVART_BACKUP2_SECRET_KEY", None)
assert m._backup_cred_pool() == [("ak_a", "sk_a")]

print("OK  lovart fallback regression passed")