#!/usr/bin/env python3
"""
CCI 多周期监控系统 - 不同周期不同频率
15m: 每30秒
1h: 每3分钟
4h: 每5分钟
1d: 每10分钟
"""

import requests
import json
import hmac
import base64
import datetime
import time
import os
import sys
from urllib.parse import urlencode
from typing import List, Dict, Optional
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from config.config import key, secret, phrase

# API 配置
api_config = {
    "api_key": key,
    "secret_key": secret,
    "passphrase": phrase,
}
BASE_URL = "https://web3.okx.com"

# Pushover 配置
PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

# 日志
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "..", "cci_trader.log")

# 上次检测时间记录
last_check_times = {}

# 上次告警推送时间记录（用于各K线独立休眠）
last_alert_times = {}

def log_message(msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {msg}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(log_line)
    print(log_line.strip())

def send_pushover_message(title, message, priority=2, retry=30, expire=3600):
    if not PUSHOVER_APP_TOKEN or not PUSHOVER_USER_KEY:
        log_message("❌ Pushover 未配置")
        return False
    
    data = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title[:100],
        "message": message[:500],
        "priority": priority,
        "retry": retry,
        "expire": expire
    }
    
    try:
        response = requests.post(PUSHOVER_URL, data=data, timeout=10)
        response.raise_for_status()
        log_message(f"✅ Pushover 已发送: {title[:30]}... (优先级: {priority})")
        return True
    except Exception as e:
        log_message(f"❌ Pushover 发送失败: {e}")
        return False

def get_signature(method, request_path, body_str, secret_key):
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    prehash_string = timestamp + method.upper() + request_path + body_str
    hmac_obj = hmac.new(secret_key.encode('utf-8'), prehash_string.encode('utf-8'), 'sha256')
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')
    return signature, timestamp

def send_get_request(request_path, params):
    query_string = urlencode(params)
    full_request_path = f"{request_path}?{query_string}" if params else request_path
    signature, timestamp = get_signature("GET", full_request_path, '', api_config['secret_key'])
    headers = {
        'OK-ACCESS-KEY': api_config['api_key'],
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': api_config['passphrase'],
    }
    while True:
        try:
            response = requests.get(BASE_URL + full_request_path, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log_message(f"请求失败: {e}")
            time.sleep(5)

def prepare_dataframe_from_data(kline_data):
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'volume_currency', 'confirm']
    df = pd.DataFrame(kline_data, columns=columns)
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    if len(str(int(df['timestamp'].iloc[0]))) == 10:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Singapore')
    df = df.iloc[::-1].reset_index(drop=True)
    return df

def calculate_cci(df, n=20):
    tp = (df['high'] + df['low'] + df['close']) / 3
    sma = tp.rolling(n, min_periods=1).mean()
    md = tp.rolling(n, min_periods=1).apply(lambda x: (abs(x - x.mean())).mean())
    cci = (tp - sma) / (0.015 * md)
    df['CCI'] = cci
    return df

def should_send_alert(token_name, bar, alert_tag="default"):
    """按K线级别做独立休眠：只抑制通知，不影响检测"""
    global last_alert_times

    # 各K线通知休眠时间（秒）
    cooldown_seconds = {
        '15m': 15 * 60,      # 15分钟
        '1h': 50 * 60,       # 50分钟
        '4h': 3 * 60 * 60,   # 3小时（主阈值 ±180）
        '4h_soft130': 3 * 60 * 60,   # 3小时（4h 软阈值 <-130）
        '4h_soft135': 3 * 60 * 60,  # 3小时（4h 软阈值 <-135）
        '4h_soft140': 3 * 60 * 60,  # 3小时（4h 软阈值 <-140）
        '1d': 23 * 60 * 60   # 23小时
    }

    cooldown_key = bar if alert_tag == "default" else f"{bar}_{alert_tag}"
    key = f"{token_name}_{cooldown_key}"
    now = datetime.datetime.now()
    last_time = last_alert_times.get(key)
    cooldown = cooldown_seconds.get(cooldown_key, cooldown_seconds.get(bar, 15 * 60))

    if not last_time:
        return True

    elapsed = (now - last_time).total_seconds()
    if elapsed >= cooldown:
        return True

    remain = int(cooldown - elapsed)
    remain_min = max(1, remain // 60)
    log_message(f"  🔕 {token_name} [{bar}] 告警休眠中，剩余约 {remain_min} 分钟")
    return False


def mark_alert_sent(token_name, bar, alert_tag="default"):
    global last_alert_times
    cooldown_key = bar if alert_tag == "default" else f"{bar}_{alert_tag}"
    key = f"{token_name}_{cooldown_key}"
    last_alert_times[key] = datetime.datetime.now()


def check_cci_threshold(token_name, token_address, bar, df_with_cci):
    latest = df_with_cci.iloc[-1]
    cci = latest['CCI']
    price = latest['close']
    timestamp = latest['timestamp'].strftime('%m-%d %H:%M')
    chart_link = f"https://dexscreener.com/bsc/{token_address}"

    if cci > 180:
        if not should_send_alert(token_name, bar):
            return False
        title = f"🚨 严重超买 [{bar}] - {token_name}"
        message = (
            f"代币: {token_name}\n"
            f"周期: {bar}\n"
            f"时间: {timestamp}\n\n"
            f"⚠️ CCI: {cci:.2f} (严重超买 > 180)\n"
            f"价格: {price:.6f}\n\n"
            f"建议: 🔴 可能回调，考虑减仓\n\n"
            f"📈 查看图表: {chart_link}"
        )
        # 紧急优先级 (priority=2) - 持续推送直到确认或过期
        if send_pushover_message(title, message, priority=2, retry=30, expire=3600):
            mark_alert_sent(token_name, bar)
            return True
        return False

    elif cci < -180:
        if not should_send_alert(token_name, bar):
            return False
        title = f"🚨 严重超卖 [{bar}] - {token_name}"
        message = (
            f"代币: {token_name}\n"
            f"周期: {bar}\n"
            f"时间: {timestamp}\n\n"
            f"⚠️ CCI: {cci:.2f} (严重超卖 < -180)\n"
            f"价格: {price:.6f}\n\n"
            f"建议: 🟢 可能反弹，关注买入机会\n\n"
            f"📈 查看图表: {chart_link}"
        )
        # 紧急优先级 (priority=2) - 持续推送直到确认或过期
        if send_pushover_message(title, message, priority=2, retry=30, expire=3600):
            mark_alert_sent(token_name, bar)
            return True
        return False

    # 4h 软阈值规则（互不影响）
    elif bar == '4h' and cci < -140:
        if not should_send_alert(token_name, bar, alert_tag="soft140"):
            return False
        title = f"⚠️ 4h 弱超卖-2 [{bar}] - {token_name}"
        message = (
            f"代币: {token_name}\n"
            f"周期: {bar}\n"
            f"时间: {timestamp}\n\n"
            f"⚠️ CCI: {cci:.2f} (4h 弱超卖 < -140)\n"
            f"价格: {price:.6f}\n\n"
            f"策略: 强观察区，注意风险放大\n"
            f"冷却: 3小时\n\n"
            f"📈 查看图表: {chart_link}"
        )
        if send_pushover_message(title, message, priority=1, retry=30, expire=1800):
            mark_alert_sent(token_name, bar, alert_tag="soft140")
            return True
        return False

    elif bar == '4h' and cci < -135:
        if not should_send_alert(token_name, bar, alert_tag="soft135"):
            return False
        title = f"⚠️ 4h 弱超卖-1 [{bar}] - {token_name}"
        message = (
            f"代币: {token_name}\n"
            f"周期: {bar}\n"
            f"时间: {timestamp}\n\n"
            f"⚠️ CCI: {cci:.2f} (4h 弱超卖 < -135)\n"
            f"价格: {price:.6f}\n\n"
            f"策略: 观察区，注意下行延续\n"
            f"冷却: 3小时\n\n"
            f"📈 查看图表: {chart_link}"
        )
        if send_pushover_message(title, message, priority=1, retry=30, expire=1800):
            mark_alert_sent(token_name, bar, alert_tag="soft135")
            return True
        return False

    # 4h CCI < -130：保留1小时冷却，不影响 -135/-140 规则
    elif bar == '4h' and cci < -130:
        if not should_send_alert(token_name, bar, alert_tag="soft130"):
            return False
        title = f"⚠️ 4h 弱超卖 [{bar}] - {token_name}"
        message = (
            f"代币: {token_name}\n"
            f"周期: {bar}\n"
            f"时间: {timestamp}\n\n"
            f"⚠️ CCI: {cci:.2f} (4h 弱超卖 < -130)\n"
            f"价格: {price:.6f}\n\n"
            f"策略: 进入观察区，等待进一步确认\n"
            f"冷却: 1小时\n\n"
            f"📈 查看图表: {chart_link}"
        )
        if send_pushover_message(title, message, priority=1, retry=30, expire=1800):
            mark_alert_sent(token_name, bar, alert_tag="soft130")
            return True
        return False

    return False

def should_check_bar(bar_name, token_key):
    """检查是否应该检测该周期"""
    global last_check_times

    # 定义检测频率（秒）
    check_intervals_seconds = {
        '15m': 30,     # 每30秒
        '1h': 180,     # 每3分钟
        '4h': 300,     # 每5分钟
        '1d': 600      # 每10分钟
    }

    interval_seconds = check_intervals_seconds.get(bar_name, 180)
    key = f"{token_key}_{bar_name}"
    last_time = last_check_times.get(key)

    if not last_time:
        return True

    elapsed_seconds = (datetime.datetime.now() - last_time).total_seconds()
    return elapsed_seconds >= interval_seconds

def update_check_time(bar_name, token_key):
    """更新检测时间"""
    global last_check_times
    key = f"{token_key}_{bar_name}"
    last_check_times[key] = datetime.datetime.now()

def monitor_token(token_name, token_address, manual_creation_time=None):
    """监控单个代币"""
    bars = {
        '15m': {'bar': '15m', 'limit': 100},
        '1h': {'bar': '1H', 'limit': 100},
        '4h': {'bar': '4H', 'limit': 100},
        '1d': {'bar': '1D', 'limit': 50}
    }
    
    token_key = token_name.replace(" ", "_")
    checked_bars = []
    
    for bar_name, config in bars.items():
        # 检查是否应该检测该周期
        if not should_check_bar(bar_name, token_key):
            continue
        
        try:
            kline_params = {
                'chainIndex': '56',
                'tokenContractAddress': token_address,
                'bar': config['bar'],
                'limit': config['limit']
            }
            
            api_response = send_get_request('/api/v6/dex/market/candles', kline_params)
            
            if api_response and 'data' in api_response and api_response['data']:
                df = prepare_dataframe_from_data(api_response['data'])
                
                if len(df) < 20:
                    continue
                
                df_with_cci = calculate_cci(df)
                latest = df_with_cci.iloc[-1]
                cci = latest['CCI']
                
                checked_bars.append(f"{bar_name}:{cci:.1f}")
                
                if abs(cci) > 180 or (bar_name == '4h' and cci < -130):
                    check_cci_threshold(token_name, token_address, bar_name, df_with_cci)
                
                # 更新检测时间
                update_check_time(bar_name, token_key)
        except Exception as e:
            log_message(f"  {bar_name}: 错误 - {e}")
    
    if checked_bars:
        log_message(f"  检测: {', '.join(checked_bars)}")

def main_loop():
    """主循环 - 每30秒运行一次，根据频率决定是否检测各周期"""
    TOKENS_CONFIG = {
        "龙虾": ("0xeccbb861c0dda7efd964010085488b69317e4444", True, "2026-02-27 16:45"),
        "哈基米": ("0x82ec31d69b3c289e541b50e30681fd1acad24444", False, None)
    }
    
    log_message("=" * 60)
    log_message("🤖 CCI 多频率监控系统启动")
    log_message("检测频率: 15m=30s, 1h=3min, 4h=5min, 1d=10min")
    log_message("=" * 60)
    
    while True:
        start_time = datetime.datetime.now()
        log_message(f"\n===== {start_time.strftime('%H:%M:%S')} 检测 =====")
        
        for token_name, (token_address, enabled, manual_creation_time) in TOKENS_CONFIG.items():
            if not enabled:
                continue
            monitor_token(token_name, token_address, manual_creation_time)
        
        # 每30秒运行一次
        time.sleep(30)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        log_message("\n监控已停止")
    except Exception as e:
        log_message(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
