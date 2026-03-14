---
name: binance-square-daily
description: |
  币安广场日报生成工具。
  自动抓取币安广场热门文章、话题，生成格式化的日报。
version: 1.0.0
author: wali
requires:
  bins: ["python3"]
  env: []
---

# Binance Square Daily

币安广场日报生成工具

## 功能

- 抓取热门话题标签
- 生成热点总结
- TOP 10 文章排行
- 格式化输出

## 使用

```bash
python3 scripts/generate_daily.py
```

## 配置

编辑 `config/settings.json` 自定义设置
