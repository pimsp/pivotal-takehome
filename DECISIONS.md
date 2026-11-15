# Decisions

What this adds: the binding decisions, one line each (the decision, who, when, ticket, a clause of why). A superseded
decision is removed (git remembers it). Don't re-argue one unless a fact under it changed; then say which.

- 2026-11-15, Pim, #7: the hook targets Claude Code (a PreToolUse hook on `submit`) and is fed by replaying recorded runs, not a live agent; it's simple, and the assignment names Claude Code.
- 2026-11-15, Pim, #7: the review screen shows `resolved` as the test result; the reviewer judges whether the patch is good, not whether it passes tests.
