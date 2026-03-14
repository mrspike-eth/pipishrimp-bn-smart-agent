---
name: openclaw-contrib-helper
description: 将本地修复自动走 fork + PR 流程提交到 openclaw/openclaw（不直推主仓）。适用于在日常调试中发现问题后快速产出规范 PR。
version: 1.0.0
author: wali
requires:
  bins: ["git", "gh", "bash"]
  env: []
---

# OpenClaw Contrib Helper

## 功能
- 自动创建分支
- 自动推送到你的 fork
- 自动创建 PR 到 `openclaw/openclaw`
- 支持 draft PR

## 安全策略
- 仅走 fork + PR，不直接推 openclaw 主仓库
- 保留人工 review / merge 流程

## 使用

```bash
cd /path/to/repo
bash scripts/contribute_openclaw.sh \
  --title "fix: xxx" \
  --body-file scripts/pr_body_openclaw_template.md \
  --base main \
  --draft
```

## 参数
- `--title` PR 标题（必填）
- `--body-file` PR 描述文件（必填）
- `--base` 目标分支（默认 `main`）
- `--head-prefix` 分支前缀（默认 `auto`）
- `--draft` 创建草稿 PR
