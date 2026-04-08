# 案例到档案回流闭环

这份文档定义的是：

> 一局深场景结束之后，哪些信息应该回流进长期档案？

如果只有 `archive -> case` 没有 `case -> archive`，系统仍然是不完整的。

## 为什么这层重要

用户真正想要的不是：

- 每次都重新进入一个新场景

而是：

- 这次约谈、这次说明文、这次补救，真的会改变我后面的系统状态

所以深场景结束后，至少要判断：

- 长期印象变了吗
- 风险是暂时缓和，还是继续累积
- 活跃主题是否已收口
- 下一步最该进入什么模式

## 输入

推荐参考：

- 当前 `state.json`
- 当前 `archive.json`
- 最近 1 份相关 session
- 当前 persona

## 推荐回流项目

### 1. `relationship_state`

根据本局结果更新：

- `counselor_impression`
- `trust_trend`
- `latest_read`

例子：

- 如果用户接住台阶并配合补材料，`latest_read` 可更新为“态度可修复，但仍需观察”
- 如果用户继续嘴硬，`trust_trend` 可从 `fragile-but-recoverable` 变为 `declining`

### 2. `risk_ledger`

根据结果档位和触发条件更新：

- `active_flags`
- `historical_flags`
- `escalation_watchpoints`
- `protected_areas`

例子：

- 结果为“写情况说明”，说明还未彻底升级，但该主题仍应保持活跃
- 如果用户在高压场景中表现出愿意配合，也可以补一条 protected area

### 3. `active_threads`

这是回流里最重要的一层。

每局结束后都要判断：

- 这个主题还在继续吗
- 是 `ongoing`、`watching` 还是 `resolved`
- 下一步最可能进入哪个模式

### 4. `recommended_next_modes`

不要让系统只给结果，不给后续。

推荐根据结果档位生成下一步模式：

- `写情况说明` -> `statement-writing`
- `正式约谈后仍可修复` -> `debrief`
- `高压场景暴露新问题` -> `repair` 或 `debrief`

## 不要回流什么

避免把这些直接写进长期档案：

- 单轮里一时冲动的语气
- 还没坐实的推断
- 只属于本场景、不具可复用价值的细节

## 最终目标

这层闭环真正想做到的是：

> 用户结束一局后，系统的长期视图已经变了，下一次进入时不只是“记得”，而是“状态已经更新了”。
