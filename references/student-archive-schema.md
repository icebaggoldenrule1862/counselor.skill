# 学生长期档案结构

这份文档定义的是：

> 同一个学生在连续多次使用后，系统应该长期记住什么？

它不是单场景 `state.json` 的替代品，而是更慢、更稳、更长期的一层。

## 为什么需要它

只有 session 和 correction 还不够。

因为用户真正长期会关心的，不只是：

- 我上次练了什么
- 导员口气改成什么样

还包括：

- 这个学期我到底反复卡在哪些问题上
- 导员对我的长期印象在变好还是变差
- 哪些风险已经在累计
- 哪些主题现在还没处理完

这就是长期档案层存在的意义。

## 推荐文件位置

建议放在：

- `generated/counselors/{slug}/archive.json`

示例见：

- `examples/systems/quiet-pressure-system/archive.json`

## 顶层结构

```json
{
  "student_profile": {},
  "communication_profile": {},
  "relationship_state": {},
  "risk_ledger": {},
  "active_threads": [],
  "longitudinal_notes": [],
  "recommended_next_modes": [],
  "updated_at": ""
}
```

## 1. `student_profile`

记录相对稳定、低频变化的信息。

建议字段：

- `display_name`
- `grade`
- `department`
- `current_focus`
- `background_notes`

例子：

```json
{
  "display_name": "未命名学生",
  "grade": "大二",
  "department": "计算机学院",
  "current_focus": ["临时请假沟通", "缺课后的办公室约谈"],
  "background_notes": ["表达偏谨慎", "面对压力时解释顺序容易混乱"]
}
```

## 2. `communication_profile`

记录用户长期沟通特征。

建议字段：

- `preferred_style`
- `common_failure_points`
- `stable_strengths`
- `effective_moves`

这一层要回答：

- 这个学生更适合怎样开口
- 最常在哪些环节翻车
- 哪些表达方式对他最稳

## 3. `relationship_state`

记录“这个辅导员系统对这个学生”的长期读法。

建议字段：

- `counselor_impression`
- `trust_trend`
- `latest_read`
- `pressure_pattern`

这里不要求绝对客观，而是要求可追踪。

例如：

- 由“中性观察”变成“谨慎关注”
- 由“先听解释”变成“证据优先”

## 4. `risk_ledger`

记录长期风险，而不是只看眼前一局。

建议字段：

- `active_flags`
- `historical_flags`
- `escalation_watchpoints`
- `protected_areas`

例子：

- `active_flags`: “考勤印象偏弱”
- `escalation_watchpoints`: “再出现一次临时沟通失控，可能进入正式记录”

## 5. `active_threads`

记录还没完结的长期主题。

每条 thread 推荐包含：

- `topic`
- `status`
- `last_mode`
- `last_updated`
- `next_risk`

这一步很关键，因为它能让系统知道：

- 这个学生现在不是“空白状态”
- 某件事还在持续

## 6. `longitudinal_notes`

记录跨多轮才会看出来的结论。

例如：

- 用户并不嘴硬，但一紧张就会把事实说乱
- 周老师系统在 correction 后更像“先听解释，再慢慢收口”

这一层更像长期观察笔记。

## 7. `recommended_next_modes`

记录系统默认推荐的下一步，而不是让用户每次都重新选。

例如：

- `office-talk`
- `debrief`
- `statement-writing`

## 更新原则

### 原则 1：慢变量优先

长期档案不是每轮都大改。

优先记录：

- 稳定特征
- 累计风险
- 长期印象

不要把每一轮瞬时情绪都硬写进去。

### 原则 2：单场景 state 和长期 archive 分开

- `state.json` 管当前局
- `archive.json` 管长期轨迹

不要混用。

### 原则 3：session 可以喂给 archive，但不能直接替代 archive

session 是一次使用的总结。
archive 是跨多轮之后沉淀下来的长期视图。

## 最终目标

这层结构真正想做到的是：

> 让用户下一次再来时，不只是“系统记得上次说了什么”，而是“系统记得我这个人最近长期卡在哪、风险积累到哪、导员会怎么继续看我”。
