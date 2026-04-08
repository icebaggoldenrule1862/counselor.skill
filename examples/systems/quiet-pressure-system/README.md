# quiet-pressure-system

这是一个完整的“专属辅导员系统”样例。

它不是单独一份 `persona`，而是一套最小可用系统目录，包含：

- `meta.json`
- `persona.md`
- `archive.json`
- `snapshot.json`
- `distillation-impact.json`
- `distillation-authenticity-report.json`
- `sessions/`
- `corrections/`

它想展示的是：

> 一个辅导员系统如何被创建、蒸馏、纠偏、记忆，然后越来越像真实导员。

## 这个样例里发生了什么

1. 先创建了一个偏“温和拿捏型”的周老师系统
2. 用户第一次用它练“临时请假怎么开口”
3. 第二次用它练“辅导员回‘具体说’之后怎么接”
4. 用户指出这个导员不会一上来就把话说死，于是做了一次 correction
5. correction 之后，系统的人格和后续办公室场景节奏都变了
6. 再通过多源蒸馏，把公开语气、私聊追问、规则路径和说明文标准校准得更像
7. 后面用户把真实回复带回来，系统继续改写 follow-up、session 和 archive

## 推荐阅读顺序

如果你想快速理解“它为什么不是一轮 prompt”，建议这样看：

1. `meta.json`
2. `snapshot.json`
3. `persona.md`
4. `archive.json`
5. `sessions/`
6. `corrections/`

如果你想重点看“蒸馏是不是够真”，再看：

- `distillation-impact.json`
- `distillation-authenticity-report.json`
- `distillation-before-after.md`
- `reality-sync-playbook.md`
- `reality-sync-use-cases.md`
- `reality-sync-leave-demo.md`
- `reality-sync-follow-up-demo.md`
- `reality-sync-help-demo.md`
- `reality-sync-statement-demo.md`
- `real-feedback-roundtrip.md`
- `real-feedback-before-after.md`

如果你想重点看“为什么这些模式依然像同一个周老师”，再看：

- `cross-mode-consistency-map.md`
- `teacher-contact-across-modes.md`
- `help-boundary-across-modes.md`

如果你想按“第一次来怎么一步步用起来”去看，再配合看：

- `../../onboarding/zero-to-first-sync.md`
- `../../onboarding/distill-then-verify.md`
- `../../onboarding/feedback-return-loop.md`

## 这个样例证明什么

它证明项目正在接近一个真正的单一辅导员系统：

- 同一个辅导员可以被反复使用
- 不同使用轮次会留下记忆
- 用户反馈会改变系统本身
- 下次进入时，不是从零开始
- correction 前后，同一个场景的压力结构会变
- 深场景结束后，长期档案和下一步推荐模式也会变
- 多源蒸馏会同时改写公开语气、私聊追问、办公室节奏和说明文标准
- 蒸馏足够真时，系统可以开始给出现实可同步的排练结果
- 现实可同步的结果不只限于请假，还包括被追问后的接话、求助沟通和说明文起草
- 用户把真实回复带回来之后，系统会继续改写 follow-up、session 和 archive
- 同一个周老师在开口、追问、办公室、说明文、求助、复盘里都开始显出稳定的判断轴和边界
