# 案件状态管理器

## 任务

在每轮场景推进后，更新 `state.json`，保证案件不是只有对话，没有状态。

## 更新时机

### Round 1 结束后

更新：

- `stage`
- `attitude.current_read`
- `scores.trust_level`

### Round 2 或亮证据后

更新：

- `scores.evidence_level`
- `scores.risk_level`
- `attitude.history`
- `branch_notes`

### 收口后

更新：

- `stage` 为 `resolved`
- `result.tier`
- `result.label`
- `result.reasons`
- `next_actions`

## 更新原则

### 1. 只改必要字段

不要每轮把整个 state 重写成另一套结构。

### 2. 行为要能映射到字段

例如：

- 学生承认问题：`trust_level` 可回升
- 学生继续甩锅：`risk_level` 上升
- 辅导员亮出截图：`evidence_level` 上升

### 3. 记录过程痕迹

`attitude.history` 和 `branch_notes` 不应该永远空着。
这两个字段是复盘的重要依据。

## 推荐输出

每轮结束后输出一个最小 patch：

```json
{
  "stage": "pressure",
  "scores": {
    "trust_level": -1,
    "risk_level": 3
  },
  "attitude": {
    "current_read": "deflecting",
    "history": [
      "学生先用模糊理由解释缺席"
    ]
  },
  "branch_notes": [
    "任课老师反馈即将被亮出"
  ]
}
```
