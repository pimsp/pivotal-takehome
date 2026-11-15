# The app's own tools

Kiteline gives each tab these tools besides Claude Code's built-in ones (an in-process MCP server named `inbox`; the model sees them as `mcp__inbox__<name>`). Each start in a transcript lists the ones that tab had. Below, each as the model read it: description, then input schema.

## add_ticket

Add a ticket to ANOTHER project's list in Kiteline (one of the owner's registered projects), for something that came up here but belongs there (e.g. a personal item in a code project's chat belongs in the todo project). It runs the ticket script there and commits only its ticket files; the ticket notes it came from this tab. The owner confirms each call. Not for this project's own tickets: use ticket_add. An unknown project is refused with the list of projects.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "project": {
      "type": "string",
      "description": "The other project: its name as in the app's project list, or its folder"
    },
    "title": {
      "type": "string",
      "description": "One line: what needs doing"
    },
    "body": {
      "description": "Detail lines: why, context, pointers. A line saying where it came from is added",
      "type": "string"
    },
    "importance": {
      "description": "1 urgent … 5 for fun; default 3",
      "type": "integer",
      "minimum": 1,
      "maximum": 5
    },
    "for": {
      "description": "Who does it: the owner (default) or Claude",
      "type": "string",
      "enum": [
        "user",
        "claude"
      ]
    },
    "tags": {
      "description": "Tags without +, e.g. [\"work\"]",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "due": {
      "description": "YYYY-MM-DD or YYYY-MM",
      "type": "string"
    }
  },
  "required": [
    "project",
    "title"
  ],
  "additionalProperties": false
}
```

## ticket_list

List this project's tickets (default: the open ones), one line each; filters combine.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "text": {
      "description": "A substring of the title or detail",
      "type": "string"
    },
    "owner": {
      "description": "Who wants it",
      "type": "string",
      "enum": [
        "user",
        "claude"
      ]
    },
    "for": {
      "description": "Who does it (the assignee)",
      "type": "string",
      "enum": [
        "user",
        "claude"
      ]
    },
    "importance": {
      "description": "This importance or more urgent (2 lists !0, !1 and !2)",
      "type": "integer",
      "minimum": 0,
      "maximum": 5
    },
    "tags": {
      "description": "Tags without +; all must match",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "status": {
      "description": "Default open",
      "type": "string",
      "enum": [
        "open",
        "done",
        "discarded",
        "all"
      ]
    },
    "due": {
      "description": "Due within this many days, overdue included",
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991
    },
    "blocked": {
      "description": "Only tickets waiting on an open ticket or on someone",
      "type": "boolean"
    },
    "part": {
      "description": "Only steps of this goal",
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991
    },
    "long": {
      "description": "Include the detail lines",
      "type": "boolean"
    }
  },
  "additionalProperties": false
}
```

## ticket_show

One ticket in full, open or closed.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991,
      "description": "The ticket number, e.g. 12 for #12"
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

## ticket_counts

Open tickets by importance, overdue and blocked; closed in the last 7 days.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {},
  "additionalProperties": false
}
```

## ticket_check

Check the ticket files: no ticket missing, duplicated or malformed. Run it before committing work that changed tickets.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {},
  "additionalProperties": false
}
```

## ticket_add

Add a ticket to this project's list (the next free number, dated today). A question for the owner: owner claude, for user, tag question, its options in the body as "Options: (a) … (b) …".

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "One line: what needs doing"
    },
    "owner": {
      "type": "string",
      "enum": [
        "user",
        "claude"
      ],
      "description": "Who wants it, is accountable"
    },
    "for": {
      "type": "string",
      "enum": [
        "user",
        "claude"
      ],
      "description": "Who does the work"
    },
    "importance": {
      "description": "0 blocker, 1 urgent … 5 for fun; default 3",
      "type": "integer",
      "minimum": 0,
      "maximum": 5
    },
    "tags": {
      "description": "Tags without +, e.g. [\"question\"]",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "body": {
      "description": "Detail lines (newlines become detail lines)",
      "type": "string"
    },
    "due": {
      "description": "YYYY-MM-DD or YYYY-MM",
      "type": "string"
    },
    "waits": {
      "description": "Tickets this one waits on",
      "type": "array",
      "items": {
        "type": "integer",
        "minimum": -9007199254740991,
        "maximum": 9007199254740991
      }
    },
    "waiting": {
      "description": "Someone outside the list it waits on",
      "type": "string"
    },
    "part": {
      "description": "The goal (a +goal ticket) it is a step towards",
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991
    }
  },
  "required": [
    "title",
    "owner",
    "for"
  ],
  "additionalProperties": false
}
```

## ticket_update

Change a ticket's fields (only those given); a note appends a dated detail line, now replaces the ticket's current-state line. Prefer now over a note when the state changed: one line, not a story. A ticket another tab claimed can only get a note, unless forced.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991,
      "description": "The ticket number, e.g. 12 for #12"
    },
    "title": {
      "description": "The new title",
      "type": "string"
    },
    "importance": {
      "description": "The new importance",
      "type": "integer",
      "minimum": 0,
      "maximum": 5
    },
    "owner": {
      "description": "Who wants it",
      "type": "string",
      "enum": [
        "user",
        "claude"
      ]
    },
    "for": {
      "description": "Who does it",
      "type": "string",
      "enum": [
        "user",
        "claude"
      ]
    },
    "tag": {
      "description": "Tags to add",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "untag": {
      "description": "Tags to remove",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "note": {
      "description": "A dated detail line to append",
      "type": "string"
    },
    "now": {
      "description": "The ticket's current state in one line (\"Now (date): ...\"), replacing the previous one; \"\" removes it",
      "type": "string"
    },
    "due": {
      "description": "YYYY-MM-DD, YYYY-MM or \"none\"",
      "type": "string"
    },
    "waits": {
      "description": "Replaces the list, e.g. \"#4,#7\"; \"none\" clears",
      "type": "string"
    },
    "waiting": {
      "description": "Replaces it; \"none\" clears",
      "type": "string"
    },
    "part": {
      "description": "Replaces the goal, e.g. \"#3\"; \"none\" clears",
      "type": "string"
    },
    "force": {
      "description": "Only when another tab holds the claim and that tab is gone or done: the owner is asked (Allow/Deny) before it goes through",
      "type": "boolean"
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

## ticket_start

Claim an open ticket for this tab before working on it (refused if another tab has it: leave it then, or force it if that tab is gone).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991,
      "description": "The ticket number, e.g. 12 for #12"
    },
    "note": {
      "description": "A dated detail line to append",
      "type": "string"
    },
    "force": {
      "description": "Only when another tab holds the claim and that tab is gone or done: the owner is asked (Allow/Deny) before it goes through",
      "type": "boolean"
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

## ticket_stop

Release this tab's claim on a ticket it leaves unfinished; it stays open. Another tab's claim is refused unless forced.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991,
      "description": "The ticket number, e.g. 12 for #12"
    },
    "note": {
      "description": "Where it was left",
      "type": "string"
    },
    "force": {
      "description": "Only when another tab holds the claim and that tab is gone or done: the owner is asked (Allow/Deny) before it goes through",
      "type": "boolean"
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

## ticket_close

Close a ticket as done (its outcome as the note), or as discarded (decided against; say why in the note).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991,
      "description": "The ticket number, e.g. 12 for #12"
    },
    "note": {
      "description": "The outcome: what was done, or why it was dropped",
      "type": "string"
    },
    "discard": {
      "description": "Discarded, not done",
      "type": "boolean"
    },
    "force": {
      "description": "Only when another tab holds the claim and that tab is gone or done: the owner is asked (Allow/Deny) before it goes through",
      "type": "boolean"
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

## ticket_reopen

Move a closed ticket back to the open list.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": -9007199254740991,
      "maximum": 9007199254740991,
      "description": "The ticket number, e.g. 12 for #12"
    },
    "note": {
      "description": "Why it is open again",
      "type": "string"
    },
    "claim": {
      "description": "Reopen it claimed by this tab",
      "type": "boolean"
    }
  },
  "required": [
    "id"
  ],
  "additionalProperties": false
}
```

## open_tab

Open a new chat tab in Kiteline (it shows under Running, marked "Send?"; the owner isn't switched to it) with `prompt` drafted in its message box: it does not start until the owner reads the brief, maybe edits it, and presses Send, so tell the owner it is there. It always works on one open `ticket` of this project; if the work has none, file it first with ticket_add. Its first message quotes the ticket and tells it to claim it, then to close it with its result as the close note (or stop it with a note if unfinished): that is where the owner finds the result. You are not told when it closes; read the ticket if you need the result later. It runs as an independent session that shares no context with you: the new tab's session already has the operating rules, the project file, the ticket tools and the project path, so leave those out and write only what it cannot find: what done looks like, what to check, what not to touch, and the choices made so far. Use it when the owner asks you to hand work to a tab of its own. The new tab can't open tabs itself. At most 3 such tabs are at work at once (a brief waiting for the owner's Send, a turn running, a card waiting for the owner, or a branch, where tabs have one, not yet merged or discarded); a finished tab whose branch merged frees its slot, even while it stays open for the owner to read. `model` (default sonnet): opus when the work is judgement (ambiguous approach, design or taste, subtle debugging, cross-cutting changes, critique or review); sonnet when the brief fits in about five lines with a clear done and a way to check it (tests, or a read-through) that would catch mistakes.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "ticket": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": -9007199254740991,
          "maximum": 9007199254740991
        },
        {
          "type": "string"
        }
      ],
      "description": "The open ticket of this project the new tab works on and closes, e.g. 88 or \"#88\""
    },
    "title": {
      "type": "string",
      "description": "Short tab title, e.g. \"#88 Auto-merge with checks\""
    },
    "prompt": {
      "type": "string",
      "description": "The brief, without what the tab already knows (rules, project file, ticket commands, the ticket's text): drafted after the quoted ticket as the new tab's first message, sent when the owner presses Send"
    },
    "model": {
      "description": "The new tab's model; default sonnet",
      "type": "string",
      "enum": [
        "opus",
        "sonnet",
        "haiku"
      ]
    }
  },
  "required": [
    "ticket",
    "title",
    "prompt"
  ],
  "additionalProperties": false
}
```

# Subagent types Kiteline defines

```json
{
  "writer": {
    "description": "A general-purpose subagent that may also edit files and run any command (tests, builds), under the tab's guards; every other type, general-purpose included, is read-only. Every call asks the owner first, in every mode: a card shows the brief, which the owner may edit, then Allow or Deny. So use it only when that is worth a card: a change spread over many files, a long check to run and fix. It can't touch the ticket list or the app's tools and leaves commits to you; it reports what it changed. Brief it fully: it gets no context from the tab.",
    "prompt": "You are a subagent that does the work its brief asks, editing files and running commands, then reports what it changed and how it checked it."
  }
}
```
