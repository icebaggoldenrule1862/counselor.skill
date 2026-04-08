# 真实反馈回流整轮示例

这份样例用来展示：

> 用户真的把系统建议拿去现实里用了之后，一条真实回复是怎样改写整个辅导员系统的。

## 1. 这一轮发生了什么

用户先在系统里练了一条临时请假消息，然后现实里真的发了。

系统原本预估：

- 对方会追问“具体说”
- 会卡“为什么现在才说”
- 可能会问“任课老师知不知道”

真实辅导员回复则更明确：

> 具体说，为什么现在才讲？任课老师那边你自己沟通过没有，别等老师找到我这里你再来补。

## 2. 这条真实回复暴露了什么

最关键的新信息不是“更凶”，而是：

- 她第一轮就检查了任课老师前置沟通
- 她不只是卡时间线，还卡“你有没有先做该做的动作”
- 她的压力释放点比之前更偏向 `teacher-first`

## 3. 这条真实回复怎么被路由

### correction

系统要立即修正：

- 这位辅导员会在第一轮更早检查任课老师沟通
- `teacher_feedback` 不只是“早”，而是“前置验证点”

### session

系统要记住：

- 用户在这一轮最容易漏掉“老师那边是否先沟通过”
- 下一次类似问题，应该先准备这层回答

### archive

系统要沉淀：

- “任课老师前置沟通”已经成为活跃风险点
- 对类似请假 / 缺勤问题，下次更适合先走 `follow-up`

## 4. 这轮的具体回流文件

- 原始反馈包：[real-feedback-packet.json](./real-feedback-packet.json)
- 新 session：[sessions/20260408_214200_real-reply-follow-up.md](./sessions/20260408_214200_real-reply-follow-up.md)
- 新 correction：[corrections/20260408_214500_real-reply-correction.json](./corrections/20260408_214500_real-reply-correction.json)
- 回流前档案：[archive-before-real-feedback.json](./archive-before-real-feedback.json)
- 回流后档案：[archive-after-real-feedback.json](./archive-after-real-feedback.json)

## 5. 这一轮证明什么

这个项目的价值不只是“模拟很像”。
它真正想做的是：

> 用户带回一条真实回复之后，系统知道该立刻修哪一层、记哪一层、沉淀哪一层。
