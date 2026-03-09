# AI Code Bot 🤖

> **This project has been archived.** See the note below.

---

## A Note on This Project

I built AICodeBot in June 2023 — back when "AI coding assistant" wasn't really a product
category yet. The idea was simple but felt radical at the time: what if your terminal had
an AI pair programmer baked in? One that understood your git history, reviewed your code,
wrote your commit messages, and helped you think through hard problems?

At the time, the tools didn't exist. So I built one.

AICodeBot could:
- Generate quality commit messages from your staged changes
- Run AI-powered code reviews on diffs and PRs
- Debug errors by capturing command output and reasoning through it
- Act as a terminal-based AI sidekick that understood your codebase
- Integrate directly into GitHub Actions for automated PR reviews

It worked. People used it. It was useful.

### Then the industry caught up.

In 2024, Anthropic released **[Claude Code](https://claude.ai/code)** — a natively agentic
coding assistant that does everything AICodeBot did, and far more, far better. It can edit
files, run commands, navigate large codebases, and operate with real autonomy. It's the
terminal-based AI coding partner I was trying to build, built by the people who know how
to build it best.

**If you're looking for an AI coding assistant, use Claude Code.** It's the real deal.

I'm proud of what AICodeBot was: an early bet on a future that turned out to be exactly
right. The hypothesis — that developers needed an AI peer in their terminal, not just a
chatbot in a browser — was validated by every major AI lab. We just got there first with
the resources we had.

That's enough. This repo is now archived as a record of that early work.

---

## What AICodeBot Did

```bash
aicodebot commit      # Generate a commit message from staged changes
aicodebot review      # AI code review on diffs or a commit hash
aicodebot debug cmd   # Run a command, capture errors, get AI debugging help
aicodebot sidekick    # Codebase-aware AI pair programmer in your terminal
```

Also shipped as a [GitHub Action for automated PR reviews](https://github.com/TechNickAI/AICodeBot-action).

Built on top of Anthropic's Claude and OpenAI's GPT-4. Funny how that worked out.

---

## Go Here Instead

**[Claude Code](https://claude.ai/code)** — Anthropic's official agentic coding assistant.
Everything this project aspired to be, and then some.

---

*Built with ❤️ + 🤖 by [Nick Sullivan](https://github.com/TechNickAI) in 2023.*
*Archived 2026 — not because the idea failed, but because it succeeded.*
