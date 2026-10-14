"""Run a task script unattended, for testing.

Copies the task into a temporary directory (so test logs never land in this
repo's data/), fills in the start dialog from key=value arguments, and injects
the keypresses listed in a test/responses*.csv file (seconds, key), timed from
when both windows have opened.

Usage (from the repo root, inside the venv):
    python test/run_emulated.py EMOTION_Scan.py test/responsesScan.csv \
        sessionID=testScan mriMode=scan counterbalance=CB1

Prints the output data directory when the run finishes. Use xvfb-run to run
without a real display (see README).
"""
import os
import shutil
import sys
import tempfile
import threading
import time

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
script, responses = sys.argv[1:3]
fields = dict(a.split('=', 1) for a in sys.argv[3:])
responses = os.path.abspath(responses)

task_dir = os.path.join(tempfile.mkdtemp(prefix='emotion-test-'), 'task')
shutil.copytree(repo, task_dir,
                ignore=shutil.ignore_patterns('.venv', '.git', 'data'))
if not os.path.exists(os.path.join(task_dir, 'siteConfig.yaml')):
    shutil.copy(os.path.join(task_dir, 'siteConfig.yaml.example'),
                os.path.join(task_dir, 'siteConfig.yaml'))

from psychopy import gui, visual, event  # noqa: E402


class FakeDlg:
    def __init__(self, dictionary, title='', **kw):
        dictionary.update(fields)
        self.OK = True

    def show(self):
        return True


gui.DlgFromDict = FakeDlg

presses = []
with open(responses) as f:
    for line in f:
        if line.strip():
            t, k = line.split(',')
            presses.append((float(t), k.strip()))


def inject():
    t0 = time.time()
    for t, k in presses:
        time.sleep(max(0, t - (time.time() - t0)))
        event._onPygletKey(k, 0, emulated=True)
    # Keep tapping space so trailing "press to continue" screens don't hang.
    while True:
        time.sleep(5)
        event._onPygletKey('space', 0, emulated=True)


_orig_init = visual.Window.__init__
_nwin = [0]


def init(self, *a, **kw):
    _orig_init(self, *a, **kw)
    _nwin[0] += 1
    if _nwin[0] == 2:  # participant window + RA window both up
        threading.Thread(target=inject, daemon=True).start()


visual.Window.__init__ = init

print('Output: %s' % os.path.join(task_dir, 'data'))
os.chdir(task_dir)
sys.path.insert(0, task_dir)
sys.argv = [script]
path = os.path.join(task_dir, script)
exec(compile(open(path).read(), path, 'exec'),
     {'__file__': path, '__name__': '__main__'})
