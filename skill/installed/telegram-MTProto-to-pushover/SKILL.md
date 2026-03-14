---
name: telegram-MTProto-to-pushover
description: Telegram 频道秒级监控（基于 MTProto 个人号）并推送到 Pushover。支持频道订阅监听、关键词过滤、去重、FloodWait 自动等待重试、后台 watchdog 崩溃自动重启。用于无法加 bot 的频道监控场景。
---

# Telegram MTProto to Pushover

使用个人号 MTProto 监听 Telegram 频道新消息，并实时推送到 Pushover。

## 必需环境变量

- `TG_API_ID`
- `TG_API_HASH`
- `TG_PHONE`
- `TG_CHANNELS`（逗号分隔）
- `PUSHOVER_APP_TOKEN`
- `PUSHOVER_USER_KEY`

可选：
- `TG_KEYWORDS`（逗号分隔；为空表示全量推送）
- `TG_SESSION_NAME`（默认 `tg_monitor`）

## 启动方式

### 前台运行

```bash
cd skills/telegram-MTProto-to-pushover
cp .env.example .env
# 填写 .env 后
./run.sh
```

### 后台守护（推荐）

```bash
./watchdog.sh start
./watchdog.sh status
./watchdog.sh stop
```

## 日志

- `logs/monitor.out.log`
- `logs/monitor.err.log`
- `logs/watchdog.log`

## 推送级别

默认按 Pushover `priority=2`（emergency）发送，参数：
- `retry=30`
- `expire=3600`
