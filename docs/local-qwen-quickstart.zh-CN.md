# 本地 Qwen 快速使用

这份文档只做一件事：

> 让你在本地已经有 Qwen 的前提下，直接把这个仓库用起来。

我已经确认你本机有：

- `ollama`
- 模型 `qwen3.5:4b`

## 1. 最简单的使用方式

你不需要先写程序。

最简单的方式就是：

1. 保持当前仓库作为工作区
2. 让 Codex 或 Claude Code 读取这个仓库里的 [SKILL.md](./../SKILL.md)
3. 用本地 Qwen 作为你平时的本地对话模型，先把真实素材整理好
4. 再按仓库的流程做“创建 -> 蒸馏 -> 演练 -> 回流”

## 2. 如果你只想先确认本地模型能跑

在 PowerShell 里运行：

```powershell
ollama run qwen3.5:4b "你是谁？请只回答一行。"
```

如果能正常回字，说明本地模型本身是通的。

## 3. 我最推荐的实际工作流

### 方案 A：用 Codex / Claude Code 跑仓库逻辑

这是最适合当前仓库的方式。

你直接在这个仓库里说：

```text
请使用当前仓库里的 skill，先帮我快速创建一个基础辅导员系统。
我的导员平时不太发火，但会把问题一步一步压实。
我现在卡在：已经发过请假消息了，但他回得很冷，我不知道下一句怎么接。
先不要长访谈，先给我一个短预演、一条能发的回复、以及你建议我下一步补什么素材。
```

这时仓库里的规则、模式、样例、蒸馏流程都会被用上。

### 方案 B：先用本地 Qwen 做素材整理，再交给仓库流程

如果你更想把 Qwen 当成本地“素材整理器”，也可以这样用：

1. 先把私聊、通知、班会转写、制度、手打印象整理成 `.txt`
2. 用本仓库的导入脚本生成分析结果和 bundle
3. 再把生成出来的 bundle 交给后续 persona / reality-sync 流程

这个方式更稳，因为它不会要求 4B 模型独自承担整个复杂系统。

## 4. 导入辅导员人格最推荐怎么做

先把你的素材放进一个目录，比如：

```text
generated/imports/my-counselor/
├── manual-profile.txt
├── chat.txt
├── notice.txt
├── meeting.txt
├── policy.txt
└── annotation.txt
```

这些文件不是都必须有。
最推荐优先准备的是：

1. `manual-profile.txt`
2. `chat.txt`
3. `notice.txt`

## 5. 一条命令跑人格导入

这个仓库已经准备了导入脚本：

[tools/import_persona_bundle.ps1](./../tools/import_persona_bundle.ps1)

你只要在仓库根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\import_persona_bundle.ps1 `
  -SourceDir .\generated\imports\my-counselor `
  -OutputDir .\generated\imports\my-counselor\out
```

跑完以后你会得到：

- `analysis/*.json`
- `bundle.json`

其中 `bundle.json` 就是你当前这位辅导员的人格蒸馏包。

## 6. 导入完之后怎么继续用

导入完以后，你可以直接把结果交给后续对话：

```text
我已经导入了自己的辅导员素材。
请基于当前仓库里的蒸馏逻辑，读取这份 bundle，先总结这位辅导员最稳定的三件事：
1. 第一条消息怎么开
2. 被追问时怎么压
3. 最后怎么收口
然后用这个辅导员系统陪我练一轮真实沟通。
```

## 7. 你应该先导入什么素材

优先级建议：

1. `manual-profile.txt`
内容写你对导员的直觉判断，比如“表面温和，但流程很重”“不太会一上来提家长”。

2. `chat.txt`
这是最值钱的，因为最能决定第一句和下一句。

3. `notice.txt`
这能补公共语气和规则压力。

4. `meeting.txt`
这能补办公室约谈时的高压节奏。

5. `policy.txt`
这能补制度路径。

6. `annotation.txt`
这能补说明文、补材料、审批反馈的风格。

## 8. 什么时候算导入得比较真

不是“句子很像”就够了。

更关键的是下面四层都开始稳定：

1. 语气像
2. 追问逻辑像
3. 规则路径像
4. 收口方式像

这时再拿去练现实沟通，价值才大。

详细看：

- [references/distillation-authenticity-protocol.md](./../references/distillation-authenticity-protocol.md)
- [examples/distillation/authenticity-report.json](./../examples/distillation/authenticity-report.json)

## 9. 现阶段最稳的建议

如果你现在就要开始：

1. 先准备 `manual-profile.txt + chat.txt + notice.txt`
2. 跑导入脚本
3. 先练一个真实问题
4. 真正去现实里用一次
5. 再把真实反馈带回来做 correction 和 archive 更新
