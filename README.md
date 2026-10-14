# fmri-emotion-hcpl

The Human Connectome Project – Lifespan (HCP-L) **EMOTION** fMRI task,
updated to run on Python 3 and current PsychoPy.

EMOTION is a block-design face/shape matching task. It is a localizer for
emotion and face processing networks, derived from Hariri et al. (2002).
On each trial the participant sees one image at the top and two below, and
presses a button to say which bottom image matches the top one. Face blocks
show angry or fearful faces; shape blocks show ovals and circles.

This repository is a modernized copy of the original HCP-L PsychoPy task,
which is publicly available from the HCP-Development task protocols page:
<https://www.humanconnectome.org/study/hcp-lifespan-development/project-protocol/task-protocols-hcp-development>

The first commit in this repository is the original upstream task, unmodified
(HCP-L revision `a5004dcb`, see `VERSION`). Every change since is in the git
history and summarized in [Changes from the original](#changes-from-the-original).

## Citation

If you use this task, please cite the original paradigm, as HCP requests:

> Hariri, Ahmad R., Alessandro Tessitore, Venkata S. Mattay, Francesco Fera,
> and Daniel R. Weinberger. 2002. "The Amygdala Response to Emotional Stimuli:
> A Comparison of Faces and Scenes." *NeuroImage* 17 (1): 317–23.
> doi: [10.1006/nimg.2002.1179](https://doi.org/10.1006/nimg.2002.1179)

The same task, with different face stimuli, was used in the original Human
Connectome Project:

> Barch, Deanna M., Gregory C. Burgess, Michael P. Harms, Steven E. Petersen,
> Bradley L. Schlaggar, Maurizio Corbetta, Matthew F. Glasser, et al. 2013.
> "Function in the Human Connectome: Task-fMRI and Individual Differences in
> Behavior." *NeuroImage* 80: 169–89.

The PsychoPy implementation is by Erik K. Kastman, Constanza M. Vidal
Bustamante and Leah H. Somerville.

## Task design

| | Practice (`EMOTION_Practice.py`) | Scan (`EMOTION_Scan.py`) |
| --- | --- | --- |
| Blocks | 2 (1 shape, 1 face) | 6 (3 shape, 3 face) |
| Trials | 12 (6 per block) | 36 (6 per block) |
| Run length from trigger | 58.4 s | 142.4 s |
| Waits for scanner trigger | No (`mriMode=Off`) | Yes (`mriMode=scan`) |

Each block starts with a 3 s cue, followed by 6 trials of 2 s stimulus + 1 s
fixation. Each run starts with an 8 s countdown and ends with an 8.4 s
fixation. Before the timed run, the practice script also shows instructions,
a button-mapping introduction and example trials with feedback.

There are three counterbalance orders of the face stimuli (`CB1`, `CB2`,
`CB3`), roughly balanced on sex, expression and ethnicity, so participants
scanned more than once can see different faces. If your study has one scan per
participant, use the same order for everyone.

All timestamps in the output files are in seconds from the first scanner
trigger.

## Requirements

- Python 3.10. Current PsychoPy does not support newer Python versions.
- [uv](https://docs.astral.sh/uv/) to create the environment (plain
  `python -m venv` + `pip` also works).
- Two displays: the experimenter's instructions appear on the primary screen
  and the task on the second screen. With only one screen the script warns
  and both windows open on the same display.
- Tested on Linux (Ubuntu, X11/XWayland). The original task ran on macOS and
  Windows; those platforms have not been retested since the update.

Python packages are pinned in `requirements.txt`:

| Package | Version | Why |
| --- | --- | --- |
| `psychopy` | 2026.2.4 | Stimulus presentation |
| `psychopy-mri-emulator` | 0.0.2 | Scanner-trigger wait (`launchScan`), which current PsychoPy moved into this plugin |

## Install

```bash
git clone https://github.com/ironictoo/fmri-emotion-hcpl.git
cd fmri-emotion-hcpl
uv venv --python 3.10 .venv
uv pip install --python .venv/bin/python -r requirements.txt
cp siteConfig.yaml.example siteConfig.yaml
```

`siteConfig.yaml` is not tracked by git, because it holds per-site settings.
Edit your copy before the first run (see the next section).

## Site configuration (`siteConfig.yaml`)

```yaml
trigger: '7'                # key the scanner sends at the start of each volume
keys:
  'left': ['1', 'num_1']    # any of these keys means "left image matches"
  'right': ['2', 'num_2']   # any of these keys means "right image matches"
'style':                    # text sizes, in degrees of visual angle
  ...
'monitor':
  'width': 28.5             # visible screen width in the scanner, cm
  'distance': 70            # eye-to-screen distance, cm
  'screen': 1               # display index for the participant window
```

- **Trigger and buttons:** set these to whatever your button box and scanner
  send as keypresses. The trigger has to arrive as a USB keypress.
- **Stimulus size:** stimuli are sized in degrees of visual angle. To match
  HCP, enter the real visible width and distance. To make the task fill your
  screen, adjust `distance`: increase it if the task is cut off, decrease it
  if it looks too small.

The finger-introduction screens in the practice script always use keys
`1` and `2`, whatever `keys` is set to.

## Running the task

```bash
source .venv/bin/activate
python EMOTION_Practice.py   # before scanning, outside the scanner
python EMOTION_Scan.py       # in the scanner
```

A dialog asks for:

| Field | Values |
| --- | --- |
| `sessionID` | Participant ID, used in output filenames |
| `mriMode` | `Off` to skip waiting for the trigger. Any other value (default for scan: `scan`) waits for the trigger. Case-sensitive: `off` or `OFF` will wait. |
| `counterbalance` | `CB1`, `CB2` or `CB3` for the scan (no default; type it in); `practice` for the practice script |

Space advances instruction screens. In scan mode, the "Get ready!" screen
waits for the trigger key; to test outside the scanner you can press `7`
yourself. Press Escape at any time to quit.

Each script runs one run. To rerun after an interruption, start the script
again; output files are timestamped, so nothing is overwritten.

## Output files

Files are written to `data/` next to the scripts. `data/` is ignored by git;
never commit participant logs.

| File | Contents |
| --- | --- |
| `*_wide.csv` | One row per trial: onsets, responses, RTs, accuracy. The main file for analysis. Columns are described in `documentation/columns-dictionary-EMOTION.{csv,json}`. |
| `*_design.csv` | One row per event (`run`, `condition`, `duration`, `onset`), for building fMRI design matrices. |
| `*.log` | Timestamped log of everything drawn and every key pressed. |
| `*.psydat` | PsychoPy's pickled experiment data. |

Filenames are `EMOTION_<sessionID>_run<N>_<YYYY-MM-DD_HHMMSS>_*`, where the
time is when the trigger arrived and practice runs are `run0`. The `.log` file
is named from when the script started, and always says `run1`.

## Changes from the original

The original targets PsychoPy 1.83.04 on Python 2.7, which can no longer be
installed from PyPI. The update makes the smallest changes needed to run on
current PsychoPy, and does not change the task's stimuli, timing or output
format:

- Python 3: removed `str.decode()` on the script path, replaced `basestring`
  with `str`, wrapped `dict.keys()` in `list()`, decoded `git` output before
  logging it, and made the imports in `hcpcommon` relative.
- pyglet: `pyglet.window.get_platform()` was removed; screens are now found with
  `pyglet.canvas.get_display()`.
- PsychoPy: trial rows are now plain dicts, so `thisTrial.stimTop` became
  `thisTrial['stimTop']`. `launchScan` is imported from the
  `psychopy-mri-emulator` plugin, falling back to the old location.
- Repository: removed `.gitmodules` (`hcpcommon/` is included directly, not a
  submodule), added `requirements.txt`, test scripts and this README, and
  corrected the practice run length in `test/responsesKey.yaml` (50 s →
  58.4 s, which includes the 8.4 s final fixation).

`EMOTION_Scan.py` and `EMOTION_Practice.py` are still identical except for
their dialog defaults. `documentation/EMOTION.psyexp` is the original Builder
file and has not been updated.

## Testing

The test runs a script on a virtual two-screen display, presses keys at
the times listed in `test/responses*.csv`, and checks the trial counts and
timings in the output against `test/responsesKey.yaml`. Each test runs in a
temporary copy of the repo, so `data/` stays empty. You need `xvfb-run`
(`sudo apt install xvfb`).

```bash
source .venv/bin/activate
xvfb-run -a -s "-screen 0 1920x1080x24 -screen 1 1920x1080x24 +xinerama +extension GLX" \
    python test/run_emulated.py EMOTION_Scan.py test/responsesScan.csv \
    sessionID=testScan mriMode=scan counterbalance=CB1
```

`run_emulated.py` prints `Output: <folder>` when it starts. Check that run:

```bash
python test/check_outputs.py Scan <output folder>/*_wide.csv
```

Test names are `Practice`, `Scan`, `Scan_CB2` and `Scan_CB3`. For the
practice script use `EMOTION_Practice.py`, `test/responsesPractice.csv` and
`mriMode=Off counterbalance=practice`. A scan test takes about 3 minutes.

On the virtual display, trial counts, cue and fixation durations, and run
length all match the expected values, and trial onsets stay on the 3 s grid.
Stimulus durations measure 1.95–1.99 s rather than 2.00 s, so the 2 s duration
check can fail there by a few milliseconds. The task is non-slip (each routine
is timed against a shared countdown), so a slow previous trial shortens the next
one rather than shifting later onsets. Check `trialEndTime - trialStartTime` in
a `_wide.csv` from your real stimulus computer before collecting data.

## Known limitations

- Not yet validated on real stimulus hardware, a button box or a scanner
  trigger since the update.
- The parallel-port trigger option in the scripts (`trigger = 'parallel'`, off
  by default) depends on `psychopy.contrib.parallel`, which no longer exists.
  Use a USB keypress trigger.
- Logs contain many `Clock.add() is deprecated` messages. These are harmless:
  the method still behaves as it did in PsychoPy 1.83.
- `README.pdf` and `documentation/EmotionSummary.pdf` are the original
  documentation. They still describe the PsychoPy 1.83.04 install and dialog
  fields (`nRuns`, `runNumber`) that this version of the script does not show.

## License

Distributed under the Human Connectome Task fMRI Battery license
(`documentation/LICENSE.txt`), which allows research and commercial use and
modification, but not sale. Modified versions must be shared under the same or
similar terms. The license requires this notice on all copies:

> Used (and/or modified) with permission. Copyright 2017. The Human Connectome
> Task fMRI Battery is a copyrighted instrument of the Human Connectome
> Consortium. All Rights Reserved. Please contact Deanna Barch
> (dbarch@artsci.wustl.edu) for use of the Human Connectome Task fMRI Battery
> for any other intended purpose. If any aspect of the Human Connectome Task
> fMRI Battery is in the public domain under applicable laws, this license does
> not affect that status.
