# Transcripts of AI assistance, 2026-11-15T10:23:00.000Z to 2026-11-15T11:57:00.000Z

This folder holds every conversation with an AI model in the recorded projects during that window: 5 sessions and 0 subagents. It was written by Kiteline's transcript export (Kiteline 0.1.0). The models were run through Claude Code 2.1.325.

Each conversation is here twice. **To read them, start at `readable/index.md`**: the human-readable version shows the conversation only (messages, a plain line per tool call, the start of each command's output), in plain text that reads as well in a text editor as rendered. The **full version** in `transcripts/` adds everything the model was given (system prompts, project files, tool descriptions, Claude Code's context) and the complete tool outputs, and the raw logs are the evidence both are made from.

## What Kiteline is

Kiteline is a desktop app for working with Claude (Anthropic's model) on a project. Each conversation is a **tab**: a Claude Code session, run through the Claude Agent SDK, with Claude Code's usual tools (read and edit files, run commands, search). A project has one **main chat**, kept across days, and any number of tabs, each opened by the owner or by another tab (`open_tab`, which drafts a brief the owner sends).

- **Worktrees.** A tab that changes code usually works on its own git branch, in its own folder next to the project (`<project>.worktrees/<name>`). Claude Code keeps one transcript folder per working folder, so a project's transcripts are spread over several; this export collects them all.
- **Subagents.** A tab can hand a narrow job to a subagent: a separate model conversation that gets a brief, works with its own tools, and returns a report. Each subagent has its own file here, linked from the tool call that spawned it.
- **Tickets and git history.** The project's to-do list (`tickets.md`) changes only through ticket tools the tabs call; every change, and every merge of a tab's branch, is a git commit. These are side effects of the conversations, not conversations. `git/<project>.log` lists the commits in the window.
- **Resuming.** A tab's Claude Code process is restarted after idle time or a restart of the app, and the conversation resumes. Kiteline rebuilds the prompt at each start, so a resumed session gets it again, with any changes to the project's files since.
- **The model router.** When the owner replies to a card on the to-do list, or starts a new ticket without choosing a model, a separate one-turn call to a small model reads the message and picks which model the new tab runs on. There were none in this window.

## What is here

| Path | What it holds |
|---|---|
| `readable/index.md`, `readable/<project>/…` | The human-readable version: every session and subagent in order, each file linking to its full version. |
| `transcripts/<project>/<start>-<title>.md` | The full version: one file per session, in order. It opens with exactly what the session was told, and gives it again at each resume. |
| `transcripts/<project>/<start>-<title>/subagent-*.md` | The full version of each subagent of that session. |
| `transcripts/app-tools.md` | The descriptions and input schemas of the app's own tools, once for the whole export; each start lists the ones its tab had. |
| `raw/claude-code/<folder>/` | Claude Code's own transcripts (JSONL, one line per entry), with subagents and saved tool outputs, as written. The only change is that images and PDFs are replaced (see below). |
| `raw/kiteline/<project>/` | Kiteline's own session log (JSONL): the prompt it built at each start, the app's tool descriptions, what the owner typed against what was sent, the router's calls, thinking text, results. |
| `git/<project>.log` | The project's commits in the window (all branches). |
| `manifest.json` | Every session and subagent: ids, times, models, and which files hold it. |

## How to read a full transcript

- **"What this session was told"** is the system prompt exactly as Claude Code recorded it at that start: Claude Code's own preset prompt, then the text Kiteline appends (the app's rules for tabs, the owner's operating rules, the project's file, the main chat's role). A fresh tab is the exception: it is told only its folder and that it only reads, has no app tools and loads no settings files, and Kiteline's note says so. Claude Code doesn't keep a copy at every start; where it kept none, the section gives the part Kiteline appended, from Kiteline's log, and says so. Kiteline's note just above it gives the model, the permission mode, the working folder and the names of the app's own tools; their descriptions are in `transcripts/app-tools.md`. The built-in tools' descriptions belong to Claude Code (version above) and are not recorded anywhere, so only their names are listed, in the "session init" block.
- **Owner** is a message the owner sent. When Kiteline changed or wrapped it (a reply to a card, a note that the main branch moved), a Kiteline note before it shows what the owner typed. Messages Kiteline sent itself are marked.
- **Opening messages are usually Kiteline's text, not the owner's.** A tab's first message, though labelled **Owner** (the owner sent it), is mostly built by Kiteline from its own prompt templates, sometimes with information the owner filled in. Start on a ticket quotes the ticket and says to claim it and close it when done; a routine sends the routine's saved prompt (with the one line Run asked for, if any); a card reply wraps the owner's answer in instructions; Full sweep and Convert send fixed prompts; a chat opened on a ticket starts with a Kiteline line naming it, which the owner goes on to type after; a tab opened by another tab (`open_tab`) gets Kiteline's quote of its ticket and instructions, then a brief written by the other tab's model, which the owner may edit before sending. Only messages typed into an open tab are wholly the owner's. The templates are in Kiteline's source (`src/core/prompts.js`).
- **Injected by Claude Code as a user message (not the owner's words)** is text Claude Code put in the user's turn: skill instructions loaded by the Skill tool, a subagent's hand-back, command output. **Context recorded by Claude Code** blocks are context it attached to a turn (the date, reminders, hook output, queued messages); most of this is given to the model.
- **Thinking** is shown as summarized by the provider: the API returns a summary of the model's reasoning, not the full text.
- **Tool calls** show their full input. Each result is in a collapsible block, as the model got it. When an output was too large, Claude Code saved it to a file and showed the model a preview; the file is under `raw/claude-code/…/tool-results/`.
- Claude Code's bookkeeping entries (titles, queue operations, file-history snapshots, costs) are never sent to the model. They are left out of the readable files, counted at the end of each, and kept in raw/.

## What is not included

- **Images and PDFs** that were pasted or read are not part of these transcripts. Both in the readable files and in the copied JSONL, each is replaced by a placeholder with its file name (if known), type, size and SHA-256, so a copy of the file can be matched to it.
- **Claude Code's own internal calls**, such as the short call that names a session or the summarizing call inside WebFetch, run inside the CLI and are not recorded by it. Kiteline can't see their prompts.
- **Sessions are exported whole.** A session active at any time in the window is included from its first message to its last, even if part of it falls outside the window.
- Sessions in the project folders that weren't started by Kiteline (e.g. `claude` run in a terminal there) are included and marked as such.

## How this was made

From Kiteline: Settings › Transcripts › Export.

Kiteline's session log is written only while Settings › Transcripts › Record transcripts is on. The switch history is `recordings.jsonl` in Kiteline's config folder. Claude Code writes its transcripts on its own, whatever the switch.

---

AI Disclaimer: this README is 100% AI-written.
