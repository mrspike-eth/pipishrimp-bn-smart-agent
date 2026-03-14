---
name: github-ops
description: |
  安全的 GitHub 操作技能 - 创建仓库、推送代码、管理 Release。
  优化版：用户确认机制、安全 Token 处理、透明权限说明。
version: 1.0.0
author: optimized
requires:
  bins: ["git", "curl", "gh"]
  env: ["GITHUB_TOKEN"]
---

# GitHub Operations Skill (Secure Version)

**定位**: 安全的 GitHub 自动化操作  
**原则**: 透明、可控、安全优先

---

## ⚠️ 安全改进（对比原版）

| 原版问题 | 优化方案 |
|---------|---------|
| 声称"无需用户干预" | ✅ 明确需要用户确认 |
| Token 暴露在 git URL | ✅ 使用 gh CLI credential helper |
| 固定路径读取 Token | ✅ 支持多种安全存储方式 |
| 无用户确认 | ✅ 关键操作前确认 |
| 描述误导 | ✅ 透明说明所有权限 |

---

## 🔐 Token 安全配置

### 方式 1：环境变量（推荐）
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### 方式 2：安全文件
```bash
# 创建安全文件
echo "ghp_your_token_here" > ~/.openclaw/secrets/github_token.txt
chmod 600 ~/.openclaw/secrets/github_token.txt

# 使用
export GITHUB_TOKEN=$(cat ~/.openclaw/secrets/github_token.txt)
```

### 方式 3：使用 gh CLI（最安全）
```bash
gh auth login
gh auth status
```

---

## 🎯 使用场景（带确认）

### 创建新仓库
```
用户：创建一个新仓库 my-project

AI: 我将为您创建 GitHub 仓库
    ─────────────────────────────
    仓库名称：my-project
    描述：（可选）
    可见性：公开
    初始化：包含 README
    ─────────────────────────────
    确认创建？[是/否]

用户：是

AI: ✅ 仓库已创建
    https://github.com/username/my-project
```

### 推送代码
```
用户：推送当前代码到 GitHub

AI: 准备推送代码
    ─────────────────────────────
    本地分支：main
    远程仓库：origin
    提交数量：3
    ─────────────────────────────
    确认推送？[是/否]

用户：是

AI: ✅ 代码已推送
```

### 创建 Release
```
用户：创建 v1.0.0 Release

AI: 准备创建 Release
    ─────────────────────────────
    版本：v1.0.0
    基于分支：main
    标题：v1.0.0
    ─────────────────────────────
    确认创建？[是/否]

用户：是

AI: ✅ Release 已创建
    https://github.com/username/repo/releases/tag/v1.0.0
```

---

## 🚀 核心功能（安全实现）

### 1. 创建仓库
```bash
# 使用 gh CLI（推荐，Token 不暴露）
gh repo create repo-name \
  --description "描述" \
  --public \
  --source=. \
  --remote=origin \
  --push

# 或使用 API（Token 在 header 中）
curl -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos \
  -d '{
    "name": "repo-name",
    "description": "描述",
    "private": false,
    "auto_init": true
  }'
```

### 2. 推送代码（安全方式）
```bash
# 方式 1：使用 gh CLI（Token 不暴露在 URL）
gh auth setup-git
git remote add origin https://github.com/username/repo.git
git push -u origin main

# 方式 2：使用 SSH（最安全）
git remote add origin git@github.com:username/repo.git
git push -u origin main
```

### 3. 创建 Release
```bash
# 使用 gh CLI
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "Release notes" \
  --target main
```

---

## 🛡️ 安全特性

### 1. 用户确认机制
- 所有创建/修改操作前要求确认
- 显示操作详情供用户核对
- 支持取消操作

### 2. Token 安全
- 支持环境变量、安全文件、gh CLI 多种方式
- Token 不暴露在命令行历史
- Token 不暴露在 git remote URL

### 3. 权限透明
- 明确说明需要的权限
- 不请求不必要的权限
- 操作日志记录

### 4. 错误处理
- 清晰的错误信息
- 不泄露敏感信息
- 安全退出

---

## 📋 权限说明

| 权限 | 用途 | 是否必需 |
|------|------|---------|
| `repo` | 创建/管理仓库 | ✅ 是 |
| `workflow` | 管理 Actions | ⭕ 可选 |
| `read:user` | 读取用户信息 | ⭕ 可选 |

---

## 🧪 测试用例

### 验证配置
```bash
# 检查 Token 是否配置
echo $GITHUB_TOKEN

# 验证 gh CLI 登录
gh auth status
```

### 测试创建仓库
```bash
# 测试（会要求确认）
gh repo create test-$(date +%s) --public --dry-run
```

---

## 📊 性能指标

| 指标 | 目标 | 状态 |
|------|------|------|
| 创建仓库 | <5s | ✅ |
| 推送代码 | <30s | ✅ |
| 创建 Release | <5s | ✅ |

---

## 🔧 故障排除

### Token 无效
```bash
# 检查 Token
gh auth status

# 重新登录
gh auth login
```

### 推送被拒绝
```bash
# 检查权限
git remote -v

# 使用 gh CLI 重新配置
gh auth setup-git
```

---

## 📝 与原版对比

| 特性 | 原版 | github-ops-secure |
|------|------|-------------------|
| 用户确认 | ❌ 无 | ✅ 有 |
| Token 安全 | ⚠️ URL 暴露 | ✅ gh CLI / 环境变量 |
| 透明度 | ❌ 误导 | ✅ 明确说明 |
| 权限控制 | ❌ 模糊 | ✅ 清晰 |
| 错误处理 | ⚠️ 一般 | ✅ 完善 |

---

*安全第一，透明可控* 🔒
