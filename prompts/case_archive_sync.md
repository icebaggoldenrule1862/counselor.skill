# 案例档案回流器

你的任务是根据一个已经接近结束或已经结束的深场景，把真正有长期价值的信息写回长期档案。

## 输入

- 当前 `state.json`
- 当前 `archive.json`
- 必要时参考最近 session 和 persona

## 先判断本局是否足够成熟可以回流

满足任一条件时，适合回流：

- `result.tier` 已有明确档位
- `stage` 已到 `closure` 或 `resolved`
- `escalation.current_level` 已清晰
- 已经能判断后续下一步

如果仍在局中早期，不要过早更新长期档案。

## 回流顺序

1. 先更新 `relationship_state`
2. 再更新 `risk_ledger`
3. 再更新 `active_threads`
4. 最后更新 `recommended_next_modes`

## 映射原则

### 结果较稳时

例如：

- 平稳过关
- 口头警告

可以：

- 保留活跃主题但弱化风险
- 推荐进入 `debrief`

### 结果需要补材料时

例如：

- 写情况说明

可以：

- 保持 thread 为 `ongoing`
- 推荐进入 `statement-writing`
- 在 `latest_read` 中加入“仍需看后续配合度”

### 结果正式升级时

例如：

- 正式约谈
- 升级处理

可以：

- 提高长期风险
- 更新 `trust_trend`
- 在 `active_threads` 中保留更强观察状态

## 保守原则

- 回流的是长期有价值的信息，不是整场 transcript
- 不要把一次失败直接写成“永久定性”
- 不要把每个场景都回流成一大堆标签

## 输出目标

输出应足够结构化，便于做成 archive patch。

最理想的结果是：

- 更新后的 `active_threads` 更清晰
- `recommended_next_modes` 更像真实下一步
- 下一次进入时，系统知道该往哪走
