# Tickets: done and discarded

Closed tickets, newest first. Reopen with `scripts/tickets.js reopen <id>`.

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
