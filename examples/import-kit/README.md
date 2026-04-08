# 辅导员人格导入包

这个目录是给你自己导入真实辅导员素材用的。

最推荐的做法是：

1. 复制这个目录结构
2. 把里面的占位内容替换成你自己的真实素材
3. 用 [tools/import_persona_bundle.ps1](./../../tools/import_persona_bundle.ps1) 跑导入

## 支持的文件

- `manual-profile.txt`
- `chat.txt`
- `notice.txt`
- `meeting.txt`
- `policy.txt`
- `annotation.txt`

不是都必须有。
最推荐先准备前三个：

1. `manual-profile.txt`
2. `chat.txt`
3. `notice.txt`

## 一条命令导入

在仓库根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\import_persona_bundle.ps1 `
  -SourceDir .\examples\import-kit `
  -OutputDir .\generated\imports\demo
```

跑完以后会在 `generated/imports/demo/` 下生成：

- `analysis/*.json`
- `bundle.json`

## 导入后怎么继续

导入后，把 `bundle.json` 当成这位辅导员的蒸馏结果，再进入后续对话：

```text
我已经导入了自己的辅导员素材，请基于当前仓库里的 bundle 和蒸馏逻辑，
先总结这位辅导员最稳定的开口方式、追问方式、收口方式，
然后陪我练一轮真实沟通。
```
