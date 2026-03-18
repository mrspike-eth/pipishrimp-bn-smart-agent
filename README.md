# PipiShrimp BN Smart Agent

一个基于 OpenClaw 的 Binance / BNB Chain 交易与投研助手。

核心目标：把 **信息获取 → 信号筛选 → 分析判断 → 执行动作 → 复盘输出** 串成统一工作流。

---

## 1. 项目结构

```text
pipishrimp-bn-smart-agent/
├── binance-daily/                 # 币安日报菜单与配置
├── watchlist/                     # 自选币与买卖逻辑配置
├── binance-spot-trade/            # 现货交易菜单配置
├── bn-wallet-onchain-trade/       # 链上钱包交易菜单配置
├── signal-monitor/                # CCI/聪明钱/榜单/地址/战壕监控
├── smart-investment-assistant/    # 智能投资助理（地址/合约/Surf）
├── content-creation/              # 币安广场创作
├── learning-mode/                 # 币安学院学习路径
├── skill-management/              # Skill 列表与分组管理
├── settings/                      # 菜单管理、可视化配置
├── secure/                        # *.env.template 等模板（不放真实密钥）
├── scripts/                       # 辅助脚本
└── reset-restore                  # reset 后恢复说明
```

---

## 2. 依赖与环境

- OpenClaw 运行环境
- Python 3（部分 skill 脚本会用到）
- Telegram Bot（菜单交互）

建议把真实凭据放在工作区 `secure/` 的本地文件中，不要提交到仓库。

---

## 3. 快速开始

### 3.1 恢复菜单与配置
在 reset 或 /new 后，按项目内 `reset-restore` 指引恢复。

### 3.2 打开主菜单
在 Telegram 发送：

```text
/menu
```

你会看到：
- 📊 币安日报
- ⭐ 币种自选列表
- 💱 币安现货交易
- ⛓️ BN Wallet链上交易
- 📡 信号监控
- 🤖 智能投资助理
- ✍️ 币安广场创作
- 📚 币安学院
- 🧩 Skill技能管理
- ⚙️ 设置

---

## 4. 常用功能

## 4.1 币安日报
入口：`nav:daily`

- `act:daily.square`：币安广场日报
- `act:daily.activity`：币安活动日报
- `act:daily.twitter`：推特日报（结构化结论版）

## 4.2 自选币与交易
入口：`nav:watchlist`

- `act:watchlist.dynamic.tokens`：动态自选列表
- `act:watch.wallet.buy.<symbol>`：链上买入
- `act:watch.wallet.sell.<symbol>`：链上卖出

已内置：
- dust 尾仓跳过（避免无效 gas 消耗）
- 卖出失败多策略重试

## 4.3 现货交易（Spot）
入口：`nav:spot_trade`

- `act:spot.refresh`：刷新资产/仓位/挂单/交易/PnL
- 支持指令式买卖（按 USDT 金额）

## 4.4 链上交易（Wallet）
入口：`nav:onchain_trade`

- `act:onchain.wallet.refresh`
- `act:onchain.wallet.funds`
- `act:onchain.wallet.positions`

## 4.5 信号监控
入口：`nav:monitor`

- `act:smart.report.now`：聪明钱即时报告
- `act:cmr.report.all`：市场币种榜单总报告
- `act:cmr.address_pnl.top10`：地址PnL Top10
- `act:meme.trench.launch_monitor.top5`：代币发射监控
- `act:meme.trench.realtime.boards.top5`：战壕实时榜单

### CCI 监控
入口：`nav:cci`

- `act:cci.start`
- `act:cci.status`
- `act:cci.stop`

## 4.6 智能投资助理
入口：`nav:invest_assistant`

- 地址分析：`query-address-info`
- 合约分析：`query-token-audit` + `query-token-info` + 叙事补充
- Surf 高级投研：`act:invest.surf.research.prompt`

## 4.7 币安广场创作
入口：`nav:content_create`

- `act:square.create.market_view`
- `act:square.create.trade_review`
- `act:square.create.hot_comment`

可结合 `square-post` 一键发布。

---

## 5. Skill 映射（核心）

- 币安活动日报 → `binance-activity-daily`
- 币安广场日报 → `binance-square-daily`
- 推特日报 → `twitter-daily`
- 聪明钱信号监控 → `trading-signal`
- 市场币种榜单 / 地址监控 → `crypto-market-rank`
- 战壕监控 → `meme-rush`
- 钱包地址分析 → `query-address-info`
- 合约分析 → `query-token-audit` + `query-token-info`
- 币安广场发布 → `square-post`
- 现货交易 → `spot`

---

## 6. 安全建议（重要）

1. **不要提交真实密钥**
   - `*.env`
   - 私钥
   - session 文件

2. **只提交模板文件**
   - `*.env.template`

3. **公开仓库前做一次历史扫描**
   - 检查历史 commit 是否误入凭据

4. **交易指令必须二次确认**
   - 金额 + 滑点 + 明确确认语句

---

## 7. 开发路线

- 继续把监控能力下沉为脚本常驻运行
- 增加“判断型 skill”做自动筛选与分级
- 强化回归检查与健康检查
- 从会话驱动升级为工具驱动

---

## License

Private / Competition Use.
