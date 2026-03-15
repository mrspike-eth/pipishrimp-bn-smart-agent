# 币安日报恢复模板（三日报固定版）

## 固定入口（nav:daily）
点击后必须直接展示按钮菜单（禁止文本兜底）：
1. 🟨 币安广场日报（act:daily.square）
2. 🟦 币安活动日报（act:daily.activity）
3. 🟪 推特日报（act:daily.twitter）
4. ⬅️ 返回主菜单（nav:main）

## 三日报实现方式与输出格式

### A) 币安广场日报
- 实现脚本：`skills/binance-square-daily/scripts/generate_daily.py`
- 主数据源（前端同源接口）：
  - 文章列表：`/bapi/composite/v3/friendly/pgc/content/article/list?pageIndex=1&pageSize=20&type=1`
  - 热门话题：`/bapi/composite/v2/public/pgc/hashtag/hot-list`
- 降级数据源：Binance Web3 Social Hype（当主源失效时自动切换）
- 输出文件：`binance_daily_YYYY-MM-DD.txt`
- 日志：`binance_daily.log`
- 输出格式：
  - TOP10 热门文章每条固定为：`第一名🥇 文章标题-作者-浏览量` + 下一行 `文章简介（<50字）`
  - 热门话题 TOP5：`第N名 #话题` + `浏览量｜讨论数`
  - 在热门话题 TOP5 后固定追加：`🪙 币安广场Top10热门讨论币种`
    - 数据源：Binance Web3 Social Hype
    - 每条格式：`第N名 币种` + 下一行 `热度值：xxxx`

### B) 币安活动日报
- 实现脚本：`skills/binance-activity-daily/scripts/generate_daily.py`
- 数据来源：Binance 公告 CMS（只读）
- 输出文件：`activity_daily_YYYY-MM-DD.txt`
- 日志：`activity_daily.log`
- 输出格式：最近24小时公告资讯，含分类分布与 TOP15（标题/时间/链接）

### C) 推特日报
- 实现脚本：`skills/twitter-daily/scripts/generate_daily.py`
- 数据来源：apidance.pro（币安系账号）
- 输出文件：`twitter_daily_YYYY-MM-DD.txt` + `twitter_prompt_YYYY-MM-DD.txt`
- 日志：`twitter_daily.log`
- 输出格式：账号推文明细 + AI总结提示词

## 验收标准
- `nav:daily` 固定为“三日报按钮版”
- 三个日报动作回调可达
- 不出现“查看今日日报/手动生成日报”这类简化旧菜单
