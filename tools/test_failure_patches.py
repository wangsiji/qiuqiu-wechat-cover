#!/usr/bin/env python3
"""Regression tests for additive failure patches."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import compile_prompt as cp

with open(os.path.join(ROOT, 'examples', 'sample-brief.json'), encoding='utf-8') as fh:
    brief = json.load(fh)
with open(os.path.join(ROOT, 'references', 'failure-codes.json'), encoding='utf-8') as fh:
    failures = json.load(fh)

base = cp.render_sections(brief)
expected = {
    'F01': 'ref_roles', 'F02': 'copy', 'F03': 'asset_fidelity', 'F04': 'asset_fidelity',
    'F05': 'layout', 'F06': 'article', 'F07': 'style', 'F08': 'copy',
    'F09': 'opener', 'F10': 'style'
}

for code, owner in expected.items():
    patched = cp.apply_failure(base, code, failures)
    changed = {k for k in base if base.get(k) != patched.get(k)}
    assert changed == {owner}, f'{code}: expected only {owner} to change, got {sorted(changed)}'
    assert base[owner] in patched[owner], f'{code}: original {owner} content was not preserved'
    assert 'FAILURE PATCH ' + code in patched[owner], f'{code}: patch marker missing'

patched = cp.apply_failure(base, 'F03', failures)
assert 'image_3' in patched['asset_fidelity'] and 'image_4' in patched['asset_fidelity']
assert 'level 2' in patched['asset_fidelity']
patched = cp.apply_failure(base, 'F02', failures)
assert '100件长期好物' in patched['copy'] and '戴了6年还在戴' in patched['copy']

print('OK    failure patch regression (F01-F10)')
