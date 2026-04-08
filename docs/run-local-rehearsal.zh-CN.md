# 本地一键演练

如果你只是想在本地 Qwen 上直接开演，不要再手写超长 PowerShell 拼接。

直接用仓库根目录下这两个脚本：

- [run-local-counselor.ps1](./../run-local-counselor.ps1)
- [run-local-counselor-summary.ps1](./../run-local-counselor-summary.ps1)

## 1. 最推荐的用法

在 PowerShell 里进入仓库目录：

```powershell
Set-Location '<your-local-repo-path>'
```

然后直接运行：

```powershell
.\run-local-counselor.ps1
```

它会：

- 自动读取 `bundle.json`
- 自动关闭思维链显示
- 自动让 Qwen 只扮演辅导员

## 2. 想换场景

直接传场景参数：

```powershell
.\run-local-counselor.ps1 -Scene "我已经给你发过请假消息了，你回得很冷，我现在来继续找你。"
```

或者：

```powershell
.\run-local-counselor.ps1 -Scene "我明天要去办公室，现在来找你。"
```

## 3. 如果 raw bundle 版还是太重

有些本地模型即使关闭 thinking，也可能被长 JSON 带偏。

这时改用摘要版：

```powershell
.\run-local-counselor-summary.ps1
```

它不用 `bundle.json` 原文，只用已经提炼好的关键人格摘要，通常更稳。

## 4. 为什么你之前会失败

主要有两个原因：

1. 你前面一度不在仓库目录，路径错了。
2. `qwen3.5:4b` 本身支持 thinking，如果不关掉，就容易先输出一大段思考过程。

这两个脚本已经帮你处理了第二个问题：

- `--think=false`
- `--hidethinking`

## 5. 最稳的建议

第一次先跑：

```powershell
.\run-local-counselor-summary.ps1
```

如果效果不错，再跑：

```powershell
.\run-local-counselor.ps1
```
