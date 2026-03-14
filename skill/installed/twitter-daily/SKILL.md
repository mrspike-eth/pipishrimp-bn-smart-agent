---
name: twitter-daily
description: |
  推特日报生成工具（使用 apidance.pro API）。
  自动监控币安系6大推特账号最近24小时的发帖，生成AI总结提示词，
  使用 OpenClaw AI 进行专业总结。
version: 1.0.0
author: wali
requires:
  bins: ["python3"]
  env: ["TWITTER_API_KEY"]
---

# Twitter Daily

使用 [apidance.pro](https://apidance.pro) API 的推特日报生成工具。

## 功能

- 📱 **多账号监控** - 同时监控6个币安系推特账号
- 📝 **24小时抓取** - 获取最近24小时的发帖、转推
- 🤖 **OpenClaw AI 总结** - 生成提示词，使用 OpenClaw AI 进行专业总结
- 🔔 **Pushover推送** - 自动推送到手机

## 监控账号（币安系6大账号）

| 账号 | 身份 |
|------|------|
| @cz_binance | CZ (币安创始人) |
| @binance | 币安官方 |
| @YZiLabs | YZi Labs |
| @heyibinance | 何一 (币安联合创始人) |
| @BNBCHAIN | BNB Chain 官方 |
| @_RichardTeng | Richard Teng (币安CEO) |

## API 来源

- **API Provider**: [apidance.pro](https://apidance.pro)
- **文档**: https://doc.apidance.pro
- **Endpoint**: `https://api.apidance.pro/sapi/UserTweets`

## 安装依赖

```bash
pip3 install requests
```

## 配置

### 1. 获取 API Key

1. 访问 https://apidance.pro
2. 注册并获取 API Key
3. 编辑 `config/env.sh`：

```bash
export TWITTER_API_KEY="your_api_key"
```

### 2. 其他配置已预设

- 监控账号已配置为币安系6大账号
- Pushover 已配置
- 统计时间：最近24小时

## 使用

### 运行生成日报
```bash
cd ~/.openclaw/workspace/skills/twitter-daily
./scripts/run.sh run_once
```

### 查看生成的提示词
```bash
cat twitter_prompt_2026-03-11.txt
```

### 使用 OpenClaw AI 总结
将生成的提示词发送给 OpenClaw AI，即可获取专业总结。

### 定时运行（每天10:00）
```bash
# 添加到 crontab
0 10 * * * cd ~/.openclaw/workspace/skills/twitter-daily && ./scripts/run.sh run_once
```

### 查看日志
```bash
tail -f twitter_daily.log
```

## 输出格式

### 1. 日报文件 (`twitter_daily_YYYY-MM-DD.txt`)
- 原始推文数据
- AI 总结提示词
- 统计数据

### 2. 提示词文件 (`twitter_prompt_YYYY-MM-DD.txt`)
- 可直接复制给 OpenClaw AI
- 包含所有推文内容和总结要求

### 3. 控制台输出
- 显示 AI 总结提示词
- 方便直接复制使用

## AI 总结内容

OpenClaw AI 将提供以下总结：

1. **按人物分类** - 每个账号的关注重点和态度
2. **热点事件** - 币安系最近关注的3-5个热点事件
3. **市场情绪** - 整体市场情绪分析（积极/消极/中性）
4. **关键信息** - 最值得关注的1-2条重要信息

## 注意事项

1. **API 限制** - apidance.pro 有请求频率限制
2. **无需 OpenAI Key** - 使用 OpenClaw AI，无需额外 API 费用
3. **手动总结** - 需要将提示词发送给 OpenClaw AI 获取总结

---
