# Instructions for the coding agent (the simulated pipeline)

What this adds: the CLAUDE.md the agent would get in the live version of this pipeline. The replay doesn't use it; it records the setup that the recorded runs stand in for.

You work on one ticket in your own git worktree. The ticket file holds the task description.

- Fix the issue in the ticket. Write a reproduction script and run it before and after your fix.
- When you are done, call the `submit` tool. Your fix is the worktree's diff; the tool collects it.
- The first `submit` shows you your diff and asks you to rerun your reproduction script, delete scratch files and submit again.
- The second `submit` goes to a human reviewer. They see the task, the diff and the test results before your summary. So make the diff speak for itself, and end with a short, accurate summary of what you changed and why.
- If the reviewer denies, you get their reason back. Address it and submit again.
