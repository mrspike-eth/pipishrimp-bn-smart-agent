---
name: cci-trader-pushover
description: |
  CCI 技术指标交易系统 - 多周期监控 + Pushover 推送。
  监控 15m/1h/4h/1d 四个周期的 CCI 指标，当超过 ±180 阈值时自动推送通知。
  支持底背离和顶背离检测。
version: 1.0.0
author: wali
requires:
  bins: ["python3", "pip3"]
  env: ["PUSHOVER_APP_TOKEN", "PUSHOVER_USER_KEY"]
---

# CCI Trader & Pushover

CCI 技术指标交易系统，多周期监控，实时推送。

## 功能特性

- 📊 **多周期监控** - 15m / 1h / 4h / 1d
- 📈 **CCI 指标** - 标准公式，20周期
- 🔔 **阈值告警** - > 180 (超买) / < -180 (超卖)
- 📱 **Pushover 推送** - 实时通知到手机
- 🔄 **底背离检测** - 超卖区买入信号
- 🔴 **顶背离检测** - 超买区卖出信号
- ⏰ **智能定时** - 每15分钟自动运行
- 📝 **日志记录** - 完整运行日志

## 安装依赖

```bash
pip3 install requests pandas
```

## 配置

### 1. OKX API 配置

编辑 `config/config.py`：
```python
key = "your_okx_api_key"
secret = "your_okx_secret"
phrase = "your_okx_passphrase"
```

### 2. Pushover 配置

环境变量：
```bash
export PUSHOVER_APP_TOKEN="your_token"
export PUSHOVER_USER_KEY="your_user_key"
```

### 3. 监控代币

编辑 `scripts/cci_monitor_multi.py` 中的 `TOKENS`：
```python
TOKENS = {
    "龙虾": "0xeccbb861c0dda7efd964010085488b69317e4444",
    "哈基米": "0x82ec31d69b3c289e541b50e30681fd1acad24444"
}
```

## 使用

### 启动监控
```bash
cd ~/.openclaw/workspace/skills/cci-trader-pushover/scripts
./run.sh start
```

### 查看状态
```bash
./run.sh status
```

### 查看日志
```bash
tail -f ~/.openclaw/workspace/skills/cci-trader-pushover/cci_monitor.log
```

### 停止监控
```bash
./run.sh stop
```

## 推送消息示例

### 超买告警
```
🔴 严重超买 [1h] - 龙虾

代币: 龙虾
周期: 1h
时间: 03-11 15:30

⚠️ CCI: 185.32 (严重超买 > 180)
价格: 0.009234

建议: 🔴 可能回调，考虑减仓

📈 查看图表: https://dexscreener.com/bsc/...
```

### 超卖告警
```
🟢 严重超卖 [4h] - 哈基米

代币: 哈基米
周期: 4h
时间: 03-11 15:30

⚠️ CCI: -192.45 (严重超卖 < -180)
价格: 0.008567

建议: 🟢 可能反弹，关注买入机会

📈 查看图表: https://dexscreener.com/bsc/...
```

## 文件结构

```
cci-trader-pushover/
├── SKILL.md                      # 技能文档
├── _meta.json                    # 元数据
├── config/
│   └── config.py                 # OKX API 配置
├── scripts/
│   ├── cci_monitor_multi.py      # 主监控程序
│   └── run.sh                    # 启动脚本
└── cci_monitor.log               # 运行日志（自动生成）
```

## 监控逻辑

### CCI 阈值
- **CCI > 180**: 严重超买，推送卖出警告
- **CCI < -180**: 严重超卖，推送买入警告
- **-180 ~ 180**: 正常区间，不推送

### 检测频率
- 每15分钟运行一次
- 对齐到 00/15/30/45 分钟刻度

## 注意事项

1. **OKX API 限制** - 注意请求频率
2. **Pushover 限制** - 免费版每月 10,000 条
3. **数据延迟** - 链上数据可能有延迟
4. **风险提示** - 信号仅供参考，不构成投资建议

## 故障排除

### 监控无法启动
```bash
# 检查日志
tail -20 cci_monitor.log

# 检查依赖
pip3 install requests pandas

# 检查配置
python3 -c "from config.config import key; print('配置正常')"
```

### Pushover 不推送
```bash
# 检查环境变量
echo $PUSHOVER_APP_TOKEN
echo $PUSHOVER_USER_KEY

# 测试推送
python3 -c "from scripts.cci_monitor_multi import send_pushover_message; send_pushover_message('测试', '消息')"
```

---

*投资有风险，交易需谨慎* 📊
