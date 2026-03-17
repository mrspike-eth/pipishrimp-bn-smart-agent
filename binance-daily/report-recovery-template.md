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
- 输出格式（按固定模板）：
  - 标题：`📊 币安广场日报（最近24小时）`
  - 第一部分：`一、TOP10 热门文章（仅展示标题）`
    - 每条格式：`N. 标题（最多120字，超出以…省略）`
  - 第二部分：`二、热点话题 TOP5`
    - 每条格式：`N. #话题（浏览 x｜讨论 y）`
  - 第三部分：`三、Top10 热门讨论币种（Social Hype）`
    - 数据源：Binance Web3 Social Hype
    - 必须“竖向排列”逐条输出，不允许逗号横排汇总
    - 每条格式：`N. 币种（热度值）`

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
- `act:daily.square` 默认发送“完整内容版”（含 TOP10 全量正文），不发送精简摘要版
