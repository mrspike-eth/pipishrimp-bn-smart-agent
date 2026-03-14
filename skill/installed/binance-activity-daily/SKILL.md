---
name: binance-activity-daily
description: |
  币安公告/资讯日报（仅信息流）。按定时任务拉取最近24小时公告并生成日报，不涉及下单、划转、提现等交易权限。
version: 1.2.0
author: wali
requires:
  bins: ["python3", "pip3"]
  env: []
---

# Binance Activity Daily（公告资讯版）

仅做“公告和资讯”聚合日报，不做交易动作。

## 功能

- 定时拉取 Binance 公告公开接口
- 汇总最近24小时公告
- 生成本地日报文件
- 本地保存日报文件

## 权限说明

- 该方案使用**公开公告接口（只读）**
- 不依赖交易权限，不执行任何资金相关操作

## 使用方法

```bash
cd skills/binance-activity-daily
pip3 install -r requirements.txt

# 运行一次日报
python3 scripts/generate_daily.py
```

## 自动任务（推荐）

每天固定时间生成并推送：

```bash
# 例如每天 09:00
0 9 * * * cd /path/to/Wali-Smart-Agent-based-on-Binance/skills/binance-activity-daily && python3 scripts/generate_daily.py >> activity_daily.log 2>&1
```

## 输出

- 日报文件：`activity_daily_YYYY-MM-DD.txt`
- 日志文件：`activity_daily.log`
