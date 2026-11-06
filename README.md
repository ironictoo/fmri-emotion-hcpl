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
- One display (default), e.g. a laptop cloned to the scanner screen; or two
  displays, with the experimenter's script on one and the task on the other
  (`monitor: screens` in `siteConfig.yaml`).
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
trigger: 't'                # key the scanner sends at the start of each volume
keys:                       # button box: buttons 1-4 send a b c d
  'left': ['a']             # button 1, pointer (index) finger: left image matches
  'right': ['b']            # button 2, middle finger: right image matches
outputDir: '~/fmri_data/EMOTION_HCPL'   # local folder for data files
'style':                    # text sizes, in degrees of visual angle
  ...
'monitor':
  'screens': 1              # 1 = one display or cloned laptop; 2 = separate experimenter screen
  'screen': 1               # task screen index when screens is 2
  'width': 28.5             # visible screen width in the scanner, cm
  'distance': 70            # eye-to-screen distance, cm
```

- **Trigger and buttons:** the keypresses your scanner and button box send.
  Each of `left`/`right` is a list, so you can add keys (e.g. `['a', 'h']` to
  also accept a laptop key during training). The trigger has to arrive as a
  USB keypress.
- **Screens:** with `screens: 1` the task runs full screen on screen 0 and
  there is no experimenter window (the participant would see it); read the
  script below instead. With `screens: 2` the experimenter window opens on
  screen 0 and the task on screen `screen`.
- **Output:** files go to `outputDir`, a local folder (created if missing).
  A relative path is taken from the repo folder. Copy the files to the network
  drive after each session.
- **Stimulus size:** stimuli are sized in degrees of visual angle. To match
  HCP, enter the real visible width and distance. To make the task fill your
  screen, adjust `distance`: increase it if the task is cut off, decrease it
  if it looks too small.

## Running the task

Training, before scanning, at the laptop:

```bash
source .venv/bin/activate
python EMOTION_Practice.py
```

In the scanner:

```bash
source .venv/bin/activate
python EMOTION_Scan.py
```

A dialog asks for:

| Field | Values |
| --- | --- |
| `sessionID` | Participant ID, used in output filenames |
| `mriMode` | `Off` to skip waiting for the trigger. Any other value (default for scan: `scan`) waits for the trigger. Case-sensitive: `off` or `OFF` will wait. |
| `counterbalance` | `CB1`, `CB2` or `CB3` for the scan (no default; type it in); `practice` for the practice script |

Practice runs the instructions, a button introduction, example trials with
feedback and a short 2-block rehearsal. The scan shows one reminder screen,
then waits for the trigger and runs the 6 blocks.

| When | Key | Effect |
| --- | --- | --- |
| Instruction screens | Space (experimenter) | Next screen |
| Practice button introduction | `a` / `b` (participant) | Pointer / middle finger button, to continue |
| Trials | `a` / `b` | Left / right image matches |
| Scan "Get ready!" screen | `t` (scanner trigger) | Run starts; press `t` yourself to test |
| End | Space | Exit |
| Any time | Escape | Quit |

Each script runs one run. To rerun after an interruption, start the script
again; output files are timestamped, so nothing is overwritten.

### Experimenter script (one screen)

With `screens: 1` these lines are not shown anywhere, so read them from here.
With `screens: 2` they appear on the experimenter screen.

**Practice** (`EMOTION_Practice.py`)

1. "Welcome to the Matching Game!" — Space
2. "In this game, you will see groups of three faces or three shapes, arranged
   in a triangle, as shown here." — Space
3. "If the bottom left picture matches the top picture, like in this example,
   you should push the button under your POINTER finger. Go ahead and press the
   pointer finger button now." — wait for the participant to press button 1
4. "And if the bottom right picture matches the top picture, like in this other
   example, you should push the button under your MIDDLE finger. Press the
   middle finger button now." — wait for button 2
5. "While you play this game, we will remind you what buttons to press at the
   bottom of the screen, as you can see here." — Space
6. "Let's practice a few trials together." — Space, then two example trials
   with feedback: watch, and make sure the participant understands the task
7. "Do you have any questions? Now you will complete a short practice that will
   look exactly like the game you will play in the scanner. In this practice,
   we will not tell you if you are right or wrong. Just try your best to follow
   the instructions and play the game." — Space
8. "Are you ready to begin the practice?" — Space; the rehearsal starts (no
   trigger). Watch and give feedback as needed. At the end, Space to exit.

**Scan** (`EMOTION_Scan.py`)

1. "Welcome back to the Matching Game!" — Space
2. "Remember, in this game, your job is to indicate which face or shape on the
   bottom row matches the face or shape on the top row. If the left picture
   matches the top picture, press the button under your POINTER finger. If the
   right picture matches the top picture, press the button under your MIDDLE
   finger." — Space
3. "Do you have any questions? Are you ready to play the game and be super
   still in this scan?" — Space; the screen shows "Get ready!"
4. Start the scan; the trigger (`t`) starts the run. At the end, Space to exit.

## Output files

Files are written to `outputDir` from `siteConfig.yaml` (default
`~/fmri_data/EMOTION_HCPL`). Keep it outside the repo; `data/` is ignored by
git in case it is used.

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
- Scanner laptop setup: trigger `t` and button box `a`/`b` in
  `siteConfig.yaml.example`; the practice button introduction uses the
  configured keys (it was fixed to `1`/`2`); `monitor: screens` for one
  (cloned) display; output folder set by `outputDir`.
- Repository: removed `.gitmodules` (`hcpcommon/` is included directly, not a
  submodule), added `requirements.txt`, test scripts and this README, and
  corrected the practice run length in `test/responsesKey.yaml` (50 s →
  58.4 s, which includes the 8.4 s final fixation).

`EMOTION_Scan.py` and `EMOTION_Practice.py` are still identical except for
their dialog defaults. `documentation/EMOTION.psyexp` is the original Builder
file and has not been updated.

## Testing

The test runs a script on a virtual display, presses keys at the times
listed in `test/responses*.csv` (`t`, `a`, `b`, Space), and checks the trial
counts and timings in the output against `test/responsesKey.yaml`. Each test
runs in a temporary copy of the repo and writes its output there. You need
`xvfb-run` (`sudo apt install xvfb`).

```bash
source .venv/bin/activate
xvfb-run -a -s "-screen 0 1920x1080x24 +extension GLX" \
    python test/run_emulated.py EMOTION_Scan.py test/responsesScan.csv \
    sessionID=testScan mriMode=scan counterbalance=CB1 screens=1
```

For two screens, use `screens=2` and
`-s "-screen 0 1920x1080x24 -screen 1 1920x1080x24 +xinerama +extension GLX"`.

`run_emulated.py` prints `Output: <folder>` when it starts. Check that run:

```bash
python test/check_outputs.py Scan <output folder>/*_wide.csv
```

Test names are `Practice`, `Scan`, `Scan_CB2` and `Scan_CB3`. For the
practice script use `EMOTION_Practice.py`, `test/responsesPractice.csv` and
`mriMode=Off counterbalance=practice`. A scan test takes about 3 minutes.

On the virtual display, trial counts, cue and fixation durations, and run
length all match the expected values, and trial onsets stay on the 3 s grid.
Stimulus durations measure 1.94–1.99 s rather than 2.00 s, so the 2 s duration
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
