# Tickets: done and discarded

Closed tickets, newest first. Reopen with `scripts/tickets.js reopen <id>`.

- [x] #7 !1 Bring the commit-first hook and replayer in line with pim-ideas.txt  owner:user  assignee:claude  started:2026-11-15  revised:2026-11-15  closed:2026-11-15  due:2026-11-15
    Changes: show 'resolved' as the test result; the two-submit flow (the first asks the agent to clean up); pre-generated verdicts for the demo; a filter for clean runs; an agent CLAUDE.md for the simulated pipeline. Done in main-chat.
    Done 2026-11-15: Done in c2e18f6 on tab/main-chat. The hook now waves the first submit through and reviews the second; 'resolved' is shown as the test-suite result; replay.py has --pretty (clean runs) and --verdicts a,d (pre-generated answers); code/hook/AGENT_CLAUDE.md holds the simulated agent instructions. Tested on 2 clean runs (bleach, tornado). Part B now measures patch quality, with the injected patch as reference.

- [x] #6 !2 Download one SWE-smith-trajectories (tool split) file and the matching SWE-smith tasks, then answer Pim's data questions  owner:user  assignee:claude  started:2026-11-15  revised:2026-11-15  closed:2026-11-15  due:2026-11-15
    Input for Part A (replaying recorded runs through the commit-first hook) and for the walkthrough's "problems in the data" section.
    Done 2026-11-15: Done: findings in notes/data.md (branch tab/6-download-data-inspect, commit d2d8ee3), data in data/raw/ (git-ignored). Key points: (1) the trajectory `patch` column looks misaligned with its rows (2320 of 2364 non-empty patches touch files the run never mentions; 649 empty), so rebuild the agent's diff from its edit calls; SWE-smith's patch is the injected bug. (2) There are two tool-call formats in the tool split (2052 structured, 961 inline XML). (3) Submit usually happens twice. (4) Confident success claims barely predict resolved (phi 0.15; 53% vs 37%). (5) Resolved 47%; 160 instances have repeated runs.

- [x] #5 !2 Work out how to record and host the 5-min walkthrough video on Pim's Linux laptop  owner:user  assignee:claude  started:2026-11-15  revised:2026-11-15  closed:2026-11-15  due:2026-11-15
    Needed for the take-home submission: a screen recording with voice, hosted so anyone with the link can view it. The recording slot is around 11:50-12:00 GMT today.
    Done 2026-11-15: Checklist (Ubuntu 24.04, GNOME 46, Wayland; checked read-only).
    Found: ffmpeg, arecord, Chrome, Firefox, Chromium and snap are installed. OBS, Kooha and SimpleScreenRecorder are not. A mic exists (sof-hda-dsp, DMIC), and a 2 s arecord test wrote data. Screen capture with ffmpeg doesn't work on Wayland. GNOME's built-in recorder (Ctrl+Shift+Alt+R) has no mic as far as I know. I haven't tested it, so don't rely on it.
    PLAN A, OBS (needs your OK to install: `sudo snap install obs-studio`, ~2 min; do it BEFORE 11:50):
    1. Open OBS. If the wizard shows, pick "Optimize just for recording".
    2. Sources: + > Screen Capture (PipeWire) > pick "Entire screen" in the GNOME dialog > OK. Mic: + > Audio Input Capture > default device.
    3. Mic check: speak and watch the Audio Mixer meter hit about -12 to -6 dB (green/yellow, not red). Optionally also run `arecord -d 5 -f cd /tmp/t.wav && aplay /tmp/t.wav`.
    4. Settings > Output > Recording Format: mp4 (or mkv, then File > Remux). Files land in ~/Videos.
    5. Start Recording, speak for 5 min, Stop Recording. Play the file for 10 s to confirm you can hear your voice.
    PLAN B, no install: Loom in Chrome (free account, extension or loom.com). It records screen plus mic and gives a link at once, but the free plan caps videos at 5:00, so aim for 4:30. Set the link to "anyone with the link" in Share. Google Meet recording needs a paid Workspace plan, so skip it.
    UPLOAD (Plan A):
    - Google Drive (quickest): drive.google.com > New > File upload > right-click the file > Share > General access > "Anyone with the link" > Viewer > Copy link. Test it in a private window.
    - Or YouTube: Create > Upload > Visibility "Unlisted". Processing takes a few minutes.
    READABLE TERMINAL: one maximised terminal only, font Ctrl+= until about 18-20 pt, close other windows, and turn off notifications (GNOME: Settings > Notifications > Do Not Disturb).
    Timing: install OBS and do a 20 s test recording now. Then record at 11:50 and upload at about 11:56.

- [x] #4 !3 Set git origin  owner:user  assignee:claude  started:2026-11-15  revised:2026-11-15  closed:2026-11-15
    Set git origin to git@github.com:pimsp/pivotal-takehome.git
    Done 2026-11-15: Added remote origin = git@github.com:pimsp/pivotal-takehome.git (git remote add, run from this tab's worktree). Remotes live in the shared .git config, so it applies to the main checkout too. Not pushed or fetched; pushing is done with the app button.

- [x] #3 !3 Download relevant video  owner:user  assignee:claude  started:2026-11-15  revised:2026-11-15  closed:2026-11-15
    Earlier in the application process, we had to watch https://www.youtube.com/watch?v=K5hELUspWq8
    Download its transcript
    Done 2026-11-15: Downloaded the YouTube auto-generated English captions with yt-dlp (about 3,000 words, full talk through the closing applause). Saved as notes/video-transcript.md on the tab branch, commit f4ca5f4; it merges with the Merge button. The captions are unedited, so names and terms may be mis-transcribed.

- [x] #2 !1 Install Python 3.13 and gh, and log in to GitHub, before the take-home starts  owner:user  assignee:user  started:2026-11-15  revised:2026-11-15  closed:2026-11-15  due:2026-11-15
    From assignment.md's prerequisites: a GitHub account and Python 3.13+. Checked today: this machine has only Python 3.12.3, and neither gh nor uv is installed. Disk space is fine (776 GB free).
    Python, no sudo needed: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then `uv python install 3.13`, then check with `uv run --python 3.13 python --version`.
    gh: `sudo apt install gh`, then `gh auth login`, then check with `gh auth status`.
    Finish this before about 13:20 GMT, when the 90 minutes have to start at the latest (deadline 14:54 GMT).
    Done 2026-11-15: Checked: uv 0.13.8 installed, uv run --python 3.13 gives Python 3.13.18; gh 2.45.0 logged in to github.com (git over ssh). PROJECT.md now says to use 3.13 through uv.

- [x] #1 !2 Converted on branch agent-inbox: check and merge +review  owner:claude  assignee:user  started:2026-11-15  revised:2026-11-15  closed:2026-11-15
    Added short DESIGN.md (one leaf), roleMain.md, DECISIONS.md (none yet), the CLAUDE.md stub, .gitignore and notes/conversion.md; PROJECT.md and assignment.md untouched. Commits c9b3a9e, 7885826, 6917e7c.
    Counts: 0 tasks found, 0 tickets made (as asked, suggestions only).
    Choices to overrule: DESIGN.md and its leaf are provisional until the task text arrives; roleMain's project line is about watching the 90-minute clock and the deadline, with no tickets beyond the task.
    Checker: nothing missing. It flagged that roleMain's Dispatch line pulls against "no tickets", so a clause was added. Its note that CLAUDE.md mentions checks PROJECT.md no longer has was rejected: the stub's text is fixed.
    Protected files: DECISIONS.md, DESIGN.md, docs/design/, PROJECT.md, assignment.md.
    Done 2026-11-15: Merged into main as a fast-forward (3418613 → 6917e7c) with the owner's yes. The uncommitted PROJECT.md edit is untouched, and nothing was pushed.
