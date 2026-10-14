"""Check a run's _wide.csv against the expectations in test/responsesKey.yaml.

Usage:
    python test/check_outputs.py <test name> <path/to/*_wide.csv>

Test names are the `name` entries in responsesKey.yaml (Practice, Scan,
Scan_CB2, Scan_CB3). Exits non-zero if any check fails.
"""
import os
import sys

import pandas as pd
import yaml

TOL = 0.05  # seconds

name, wide = sys.argv[1:3]
key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'responsesKey.yaml')
spec = next(t for t in yaml.safe_load(open(key_file)) if t['name'] == name)
df = pd.read_csv(wide)
ok = True


def report(passed, msg):
    global ok
    ok &= passed
    print(('PASS ' if passed else 'FAIL ') + msg)


for check in spec['checks']:
    for col, val, n in check.get('counts', []):
        got = int((df[col] == val).sum())
        report(got == n, '%s == %s: %d trials (expect %d)' % (col, val, got, n))
    for col, val in check.get('values', []):
        got = df[col].dropna().max()
        report(abs(got - val) < TOL, '%s: %.3f s (expect %s)' % (col, got, val))
    for expr, dur in check.get('durations', []):
        d = df.eval(expr).dropna()
        report(len(d) > 0 and (d - dur).abs().max() < TOL,
               '%s: n=%d, %.3f-%.3f s (expect %s)'
               % (expr, len(d), d.min(), d.max(), dur))

sys.exit(0 if ok else 1)
