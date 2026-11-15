# Tickets

Open tickets between the user and Claude. Done and discarded ones move to tickets-done.md.
Manage with `scripts/tickets.js` (list, add, close, update, check); format in its header comment.

- [ ] #2 !1 Install Python 3.13 and gh, and log in to GitHub, before the take-home starts  owner:user  assignee:user  started:2026-11-15  revised:2026-11-15  due:2026-11-15
    From assignment.md's prerequisites: a GitHub account and Python 3.13+. Checked today: this machine has only Python 3.12.3, and neither gh nor uv is installed. Disk space is fine (776 GB free).
    Python, no sudo needed: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then `uv python install 3.13`, then check with `uv run --python 3.13 python --version`.
    gh: `sudo apt install gh`, then `gh auth login`, then check with `gh auth status`.
    Finish this before about 13:20 GMT, when the 90 minutes have to start at the latest (deadline 14:54 GMT).
