# counselor.skill

> *“Come to my office.”*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-green)](/README_EN.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-brightgreen)](https://agentskills.io)

**College students have suffered enough under counselor chat windows.**  
This project distills a real counselor from notices, private chats, office talks, comments, and policy language into an evolving AI Skill.  
It should not only sound like them, but also pressure like them, delay like them, and close the conversation the way they would.

This is not a leave-request template pack.  
This is not just roleplay.

It aims to be:

**a single high-fidelity counselor interaction system for real student communication dilemmas.**

[中文](./README.md) · [Install](#install) · [Usage](#usage) · [Examples](#examples) · [Features](#features) · [Structure](#project-structure) · [Credits](#credits--inspirations)

---

## Features

### 1. Not a template pack, but your counselor system

What this project builds is not a few canned excuses.  
It is a system with:

- `Persona`: who this counselor really is
- `Archive`: how they currently see you and what risks are accumulating
- `Sessions`: what has happened in previous conversations
- `Corrections`: one “they wouldn’t say that” can change the next round
- `Modes`: opening, follow-up, office talk, statement writing, repair, help-seeking, debrief

### 2. It distills school management logic, not just catchphrases

The system tries to capture:

- how the first reply opens
- how follow-up pressure works in private chat
- how evidence is revealed in office talks
- how statement reviews are framed
- how policy escalation actually works

So this is not just “how they talk”.  
It is also “how they process a case”.

### 3. Reality-sync first

The goal is not to simulate beautifully.  
The goal is to help users walk away with:

- one message they can send today
- one safer next sentence after being questioned
- one editable statement structure
- one useful post-conversation debrief

### 4. Continuous evolution

- append new material
- merge incrementally
- correct by saying “that’s not how they’d talk”
- preserve long-term memory
- evolve instead of resetting every time

### 5. Single-person consistency

This repository explicitly avoids multi-character theater.

We only want one thing:

> whether you rehearse leave requests, office talks, help-seeking, or damage control, it should still feel like the same counselor.

---

## Install

Recommended public repository name:

- `counselor.skill`

Display name:

- `辅导员.skill`

### Claude Code / Codex / OpenClaw

Clone this repository into your local skills directory.

#### Windows PowerShell

```powershell
# Claude Code
$repo="https://github.com/xiexie-qiuligao/counselor.skill.git"
$target="$HOME\.claude\skills\create-counselor"
if (Test-Path "$target\.git") { git -C $target pull --ff-only } else { New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null; git clone $repo $target }

# Codex
$repo="https://github.com/xiexie-qiuligao/counselor.skill.git"
$target="$HOME\.codex\skills\create-counselor"
if (Test-Path "$target\.git") { git -C $target pull --ff-only } else { New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null; git clone $repo $target }

# OpenClaw
$repo="https://github.com/xiexie-qiuligao/counselor.skill.git"
$target="$HOME\.openclaw\workspace\skills\create-counselor"
if (Test-Path "$target\.git") { git -C $target pull --ff-only } else { New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null; git clone $repo $target }
```

#### Linux / macOS

```bash
# Claude Code
REPO="https://github.com/xiexie-qiuligao/counselor.skill.git"; TARGET="$HOME/.claude/skills/create-counselor"; mkdir -p "$(dirname "$TARGET")"; if [ -d "$TARGET/.git" ]; then git -C "$TARGET" pull --ff-only; else git clone "$REPO" "$TARGET"; fi

# Codex
REPO="https://github.com/xiexie-qiuligao/counselor.skill.git"; TARGET="$HOME/.codex/skills/create-counselor"; mkdir -p "$(dirname "$TARGET")"; if [ -d "$TARGET/.git" ]; then git -C "$TARGET" pull --ff-only; else git clone "$REPO" "$TARGET"; fi

# OpenClaw
REPO="https://github.com/xiexie-qiuligao/counselor.skill.git"; TARGET="$HOME/.openclaw/workspace/skills/create-counselor"; mkdir -p "$(dirname "$TARGET")"; if [ -d "$TARGET/.git" ]; then git -C "$TARGET" pull --ff-only; else git clone "$REPO" "$TARGET"; fi
```

---

## Usage

Invoke the skill in Claude Code / Codex / OpenClaw:

```text
Use $office-call-skill
```

Then follow this flow:

1. describe the counselor
2. import material
3. generate the first persona
4. rehearse one real situation
5. correct when it feels wrong
6. bring real feedback back into the system

Typical material sources:

- private chat screenshots or transcripts
- class-group notices
- office-talk transcripts
- statement comments
- policy text
- your own subjective impression

Your real entry point is usually not “leave / truancy / late return”.

Better entry points are:

- I haven’t sent the first message yet
- I already sent it, but don’t know what to say next
- I have to go to the office tomorrow
- I need to write a statement
- I just ruined the conversation and want to repair it
- I actually need help, but don’t know how to ask

---

## Examples

> Input portrait: `bureaucratic, rigid, loves uniform requirements, replies cold and short, likes to delay and make students run the process themselves`

**Scenario 1: you already sent a leave request, and they reply with “what exactly happened?”**

```text
You ❯ Teacher, I have something urgent at home these two days and want to ask for one day off.

counselor.skill ❯ “Something urgent” is not enough.
                   Time, classes affected, and whether you contacted the course teacher first. Start there.
```

**Scenario 2: you need to rehearse an office talk**

```text
You ❯ Teacher, I really did have a sudden issue that day.

counselor.skill ❯ Don’t use “sudden issue” to blur it.
                   The course teacher has already reported this. What you need to fix now is process, not phrasing.
```

**Scenario 3: this is not misconduct, you actually need help**

```text
You ❯ Teacher, I’ve been in a messy state lately and wanted to talk to you.

counselor.skill ❯ Don’t circle around it.
                   Is this attendance, classwork, dorm, or emotional state? Say that first so I know whether this is even my lane.
```

---

## Project Structure

```text
counselor.skill/
├── SKILL.md
├── README.md
├── README_EN.md
├── agents/
│   └── openai.yaml
├── prompts/
├── references/
├── tools/
├── examples/
├── docs/
└── generated/
```

---

## Notes

- raw material quality determines fidelity
- this is not a forgery tool for leave slips or fake proof
- this should not be used to bypass school management
- if the situation involves crisis, self-harm risk, or serious real-life conflict, real support should come first

---

## Credits & Inspirations

This project’s structure, tone, and public presentation were heavily inspired by:

- [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill)
- [UniversePeak/Supervisor.skill](https://github.com/UniversePeak/Supervisor.skill)
- [tmstack/awesome-persona-skills](https://github.com/tmstack/awesome-persona-skills)

What I learned most from them:

1. a homepage should feel usable before it feels technical
2. a skill should be a system, not a pile of prompts
3. a good skill needs function, but also voice, humor, and a point of view

---

## Final Note

One of the strangest parts of college is not always exams.
Sometimes it is just the chat box.

You stare at the word “Teacher” for ten minutes and still do not know how to send the first sentence.

This skill is not here to make people better liars.
It is here to give them one place to rehearse before reality gets heavy.

If it is worth anything, it will not be because it “sounds real”.
It will be because:

- it helps users say the real problem sooner
- it makes asking for help a little more possible
- it gives some difficult conversations at least a bit more preparation

MIT License © contributors
