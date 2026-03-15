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
- 数据来源：Binance Square 热门列表
- 输出文件：`binance_daily_YYYY-MM-DD.txt`
- 日志：`binance_daily.log`
- 输出格式：最近24小时热门文章 TOP10，含作者/点赞/浏览

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
