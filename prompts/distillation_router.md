# 蒸馏路由器

你的任务是在用户导入材料时，先判断：

> 这份材料属于哪种来源？最适合提取哪类信号？应该交给哪个分析器？

## 目标

避免所有材料都走同一套抽取逻辑。

## 来源判断

### 通知 / 公告

特征：

- 行政语气
- 大量“必须 / 不得 / 请各位 / 后续”

优先读取：

- `tools/notice_parser.py`

### 私聊记录

特征：

- 有明确说话人
- 一问一答
- 追问明显

优先读取：

- `tools/chat_parser.py`

### 制度文本

特征：

- 规则条文
- “情节严重”“上报”“约谈”“书面说明”等

优先读取：

- `tools/policy_parser.py`

### 班会 / 办公室谈话转写

特征：

- 长段讲话
- 连续施压
- 经常有“我再强调一次”“你们不要觉得”之类表达

优先读取：

- `tools/meeting_parser.py`

### 用户手打印象 / 口述

特征：

- 主观判断多
- 会出现“更像”“不会这样”“他其实是”这类句式

优先读取：

- `tools/manual_profile_parser.py`

### 批注 / 审批反馈

特征：

- 句子短
- 明显指向材料缺口或流程要求

优先读取：

- `tools/annotation_parser.py`

## 路由后的统一动作

每份来源在分析后，都应尽量输出：

- `source_type`
- `tone_guess`
- `behavior_signals`
- `rule_signals`
- `conflict_candidates`

然后再交给统一 bundle merger。

## 最终目标

蒸馏层不应像“一个 parser 处理一切”，而应像：

> 来源识别 -> 定向抽取 -> 统一 merge。
