# 案件状态结构

这份文件定义单场景模式下的正式案件结构。

## 目标

让每个 case 都具备一致的状态字段，方便：

- 场景推进
- 结果判定
- 复盘
- 长期档案接入

## 推荐目录结构

```text
generated/cases/{case_id}/
├── case.md
├── state.json
└── transcript.md
```

## state.json 结构

```json
{
  "case_id": "20260407-223442-item-48d7d5b1",
  "scene_type": "truancy",
  "scene_label": "逃课被抓",
  "created_at": "2026-04-07T22:34:42",
  "updated_at": "2026-04-07T22:34:42",
  "stage": "opening",
  "status": "active",
  "persona_slug": "item-4c1e3222",
  "student_profile": {
    "display_name": "未命名学生",
    "history_flags": [],
    "recent_record": []
  },
  "archive_context": {
    "current_focus": [],
    "active_flags": [],
    "active_threads": [],
    "counselor_impression": "neutral",
    "trust_trend": "unknown",
    "pressure_pattern": [],
    "carry_over_notes": []
  },
  "scores": {
    "impression_score": 0,
    "trust_level": 0,
    "evidence_level": 0,
    "risk_level": 0
  },
  "attitude": {
    "current_read": "unknown",
    "history": []
  },
  "evidence_queue": [],
  "escalation": {
    "current_level": "watch",
    "likely_next_steps": [],
    "triggers_met": [],
    "trigger_log": []
  },
  "known_info": [],
  "hidden_evidence": [],
  "redlines": [],
  "branch_notes": [],
  "result": {
    "tier": null,
    "label": null,
    "reasons": []
  },
  "next_actions": []
}
```

## 关键字段说明

### `scene_type`

固定类型名，用于决定 playbook：

- `leave-request`
- `truancy`
- `late-return`

### `stage`

推荐阶段：

- `opening`
- `probing`
- `pressure`
- `closure`
- `resolved`

### `scores`

分值并不是游戏 UI，而是内部决策辅助。
建议范围先统一在 `-3` 到 `+3` 或 `0` 到 `5` 内，避免失控。

### `archive_context`

这是深场景最重要的新层。

它的作用是把长期档案中的慢变量带进单场景：

- 当前长期主题
- 累积风险
- 辅导员长期印象
- 当前更习惯的压迫方式

如果没有这层，深场景容易退化成“每局重开”。

### `known_info`

用户已经明确知道的信息。

例如：

- 任课老师已经反馈
- 宿管登记了
- 请假时间冲突

### `hidden_evidence`

不应在开场全部揭示的信息。

例如：

- 班长私下反馈
- 重复记录
- 课程预警线

### `evidence_queue`

推荐把高压场景里的证据做成显式队列，而不是散在文案里。

每条证据至少应包含：

- `label`
- `source`
- `reveal_stage`
- `impact`
- `revealed`

这样才能更稳定地实现：

- 第一轮先试探
- 第二轮亮任课老师反馈
- 第三轮再补班长、宿管或历史记录

### `redlines`

本场景的硬风险触发器。

例如：

- 连续重复发生
- 明显骗过管理
- 事件已经外溢

### `result`

只在结束或接近结束时写定。

### `escalation`

这一层不是处罚单，而是“接下来最可能怎么升级”。

建议记录：

- 当前所处层级
- 最可能的下一步
- 已触发哪些升级条件
- 每次升级是被哪句话或哪条证据触发的

这会直接提高复盘的信息量。

## 最小闭环要求

一个完整 case 至少要做到：

1. 开场有压力
2. 中段有态度判断
3. 至少有一次证据揭示或台阶给予
4. 结尾有明确结果或下一步
5. 长期档案中的至少一个慢变量进入本局
