# 辅导员.skill

> *“你来办公室一趟。”*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-green)](/README.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-brightgreen)](https://agentskills.io)

**天下大学生苦导员久矣。**  
把辅导员的通知、私聊、班会、批注、制度语气蒸馏成一个可持续进化的 AI Skill。  
不只是“像他会怎么说”，还要“像他会怎么压、怎么收、怎么卡流程、怎么让你回去补材料”。

一句话说，这不是请假模板库，也不是聊天角色扮演。  
它要做的是一个面向大学生真实沟通困境的：

**单一高保真辅导员交互系统。**

[English](./README_EN.md) · [安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [功能特性](#功能特性) · [项目结构](#项目结构) · [致谢与灵感](#致谢与灵感)

---

## 功能特性

### 1. 不是“场景模板”，而是“你的辅导员系统”

这个仓库最终生成的不是几段请假话术，而是一整套会持续变化的系统：

- `Persona`：这位辅导员到底是什么人
- `Archive`：他现在怎么看你，哪些风险已经在积累
- `Sessions`：你们之前都怎么沟通过
- `Corrections`：你一句“他不会这么说”，系统下轮就改
- `Modes`：开口、追问、约谈、说明文、补救、求助、复盘都能切

### 2. 蒸馏的是“学校管理逻辑”，不只是口头禅

蒸馏时会尽量抓这些层：

- 私聊里的第一句和下一句
- 通知里的命令语气
- 办公室约谈里的证据节奏
- 说明文批注里的收口标准
- 制度文本里的升级路径

所以它不是单纯学说话，而是在学：

> 这个导员平时怎么处理事。

### 3. 现实同步优先，不做空转模拟

这个 Skill 最重要的不是“演得像”，而是：

- 给你一条今天就能发的消息
- 给你一句被追问后的下一句
- 给你一份能改的说明文结构
- 给你一轮真实对话后的复盘结论

### 4. 持续进化

- 追加素材：增量 merge，不推翻旧结论
- 对话纠偏：一句“他不会这么说”立即改
- 长期记忆：下次再来，它还记得你卡在哪
- 版本化：系统不是一次性 prompt，而是逐渐长出来的

### 5. 单一人格一致性优先

这个项目明确不做多角色群像戏。  
我们只做一件事：

> 无论你是在练请假、补材料、办公室约谈还是求助复盘，对面都要像同一个辅导员。

---

## 安装

仓库建议名：

- `辅导员.skill`
- 或者更通用一点：`counselor.skill`

如果你要发 GitHub，我更推荐：

- 对外展示名：`辅导员.skill`
- GitHub 仓库名：`counselor.skill` 或 `office-call-skill`

这样兼顾中文辨识度和链接可用性。

### Claude Code / Codex / OpenClaw

把本仓库 clone 到你的 skill 目录即可。

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

## 使用

在 Claude Code / Codex / OpenClaw 里调用：

```text
Use $office-call-skill
```

然后按流程做这几步：

1. 输入辅导员的基础印象
2. 选择导入素材
3. 生成第一版人格
4. 跑一轮真实沟通预演
5. 如果不像，直接 correction
6. 如果现实里已经用了，再把真实反馈带回来

### 典型素材来源

- 私聊截图 / 转写
- 班群通知
- 班会发言
- 约谈转写
- 说明文批注
- 学校制度
- 你对这个导员的主观印象

### 你真正的入口，不是“请假 / 旷课 / 夜不归宿”

更合理的入口其实是：

- 我还没开口，不知道第一句怎么发
- 我已经发了，但不知道下一句怎么接
- 我明天要去办公室，先预演一下
- 我想写情况说明
- 我刚刚聊崩了，想补救
- 我其实是要求助，但不敢开口

---

## 效果示例

> 输入画像：`官僚主义强，不懂变通，喜欢统一要求，回复短冷硬，喜欢把问题拖一下再让学生自己跑流程`

**场景一：你已经发了请假消息，对方只回“具体什么情况”**

```text
你 ❯ 老师，我这两天家里临时有点事，想请一天假。

辅导员.skill ❯ “有点事”不够。
                时间、哪几节课、有没有提前跟任课老师说，先讲清楚。
```

**场景二：你明天要去办公室，想先预演**

```text
你 ❯ 老师，我那天确实是临时出了点情况。

辅导员.skill ❯ 先别用“临时有事”糊弄。
                任课老师那边已经反馈过来了，你现在要解决的是流程问题，不是措辞问题。
```

**场景三：你不是违规，是想求助**

```text
你 ❯ 老师，我最近状态有点乱，想和您说一下。

辅导员.skill ❯ 你先别绕。
                你现在卡的是考勤、课程、宿舍还是情绪状态？先说清楚，我才知道这事归不归我管。
```

**场景四：这位导员的另一种典型风格**

```text
你 ❯ 老师，这个流程我现在真有点来不及。

辅导员.skill ❯ 大家都一样，不是只有你特殊。
                你先按统一要求走，后面要补的再补。
```

---

## 项目结构

```text
counselor.skill/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── custom_intake.md
│   ├── persona_builder.md
│   ├── start_router.md
│   ├── system_orchestrator.md
│   ├── scene_engine.md
│   ├── correction_handler.md
│   ├── distillation_router.md
│   ├── distillation_merger.md
│   └── ...
├── references/
│   ├── start-here.md
│   ├── system-modes.md
│   ├── system-lifecycle.md
│   ├── distillation-authenticity-protocol.md
│   ├── cross-mode-consistency-rules.md
│   └── ...
├── tools/
│   ├── chat_parser.py
│   ├── notice_parser.py
│   ├── meeting_parser.py
│   ├── policy_parser.py
│   ├── manual_profile_parser.py
│   ├── distillation_bundle_builder.py
│   ├── distillation_authenticity_report.py
│   └── ...
├── examples/
│   ├── onboarding/
│   ├── distillation/
│   ├── import-kit/
│   └── systems/
├── docs/
└── generated/
```

---

## 注意事项

- 原材料质量决定还原度：私聊和约谈 > 通知 > 主观印象
- 本项目不是“请假造假器”，不用于伪造材料或绕过学校管理
- 如果涉及心理危机、自伤风险、严重现实冲突，应优先寻求现实帮助
- 这个 Skill 只是沟通训练与系统蒸馏工具，不替代真实辅导员，也不替代正式校方流程

---

## 致谢与灵感

本项目在首页结构、叙事方式和技能表达上，重点学习并致敬以下开源项目：

- [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill)
- [UniversePeak/Supervisor.skill](https://github.com/UniversePeak/Supervisor.skill)
- [tmstack/awesome-persona-skills](https://github.com/tmstack/awesome-persona-skills)

我从它们身上主要学到三件事：

1. 首页不能只讲“有什么文件”，要先让人一眼感到“这东西真能用”
2. Skill 不该只是 prompt 集合，而应该是会生成、会记忆、会纠偏、会进化的系统
3. 一个好 Skill 除了功能，还要有气质，有一点幽默，也有一点对现实的理解

---

## 写在最后

大学里最抽象的，不一定是期末周。  
也不一定是论文、早八和点名。  
很多时候，是你站在聊天框前，盯着“老师”两个字，想了十分钟，还是不知道第一句怎么发。

你不是不会说话。  
你只是太知道，有些人一句“你来办公室一趟”，就足够让人脑袋空白。

这个 Skill 想做的，不是让你变成一个更会糊弄的人。  
而是至少在你真的要开口之前，给你一个能先练一下的地方。

先把最难说出口的那句话说出来。  
先把最容易翻车的那一步走一遍。  
先把现实里的压迫感，变成一点点可执行的动作。

如果它最后真有价值，价值不是“像”，而是：

- 让用户更早说清楚问题
- 让求助比硬扛更容易发生
- 让一些本来会彻底聊崩的现实沟通，至少多一点准备

MIT License © contributors
