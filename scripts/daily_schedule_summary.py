#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日行程摘要 - 自動執行腳本
==========================================

排程：每天早上 08:00

功能：
1. 讀取 DAILY_TASKS 任務清單
2. 整理當日執行的行程
3. 發送到 Telegram

"""

import subprocess
import json
import datetime
import os
import re

# ===== 常數 =====
BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

# ===== 任務定義 =====
DAILY_TASKS_FILE = '/root/.openclaw/media/inbound/DAILY_TASKS---8dfc3a19-ab4a-4f81-a6ad-d693d1b206e2.md'

# 任務時間對照表（根據 DAILY_TASKS 設定）
DAILY_SCHEDULE = {
    "01:00": "🏪 591店面出租報告",
    "02:00": "☀️ 晨間摘要",
    "04:45": "📈 股市早盤",
    "06:00": "📰 全方位新聞快報",
    "每6小時": "🌍 中東局勢追蹤",
    "14:00": "📈 股市午盤",
    "23:00": "💾 OpenClaw 備份",
}

WEEKLY_SCHEDULE = {
    "週一 09:00": "🧠 記憶維護",
    "週一 09:30": "📋 Notion 每週報告",
    "週五 14:30": "🏷️ 促銷活動報告",
    "週五 16:00": "🌴 週末行程規劃",
    "週六 03:00": "📔 每週日記報告",
    "週六 09:00": "📊 股票績效分析",
}

MONTHLY_SCHEDULE = {
    "每月 1日 00:00": "📊 資產報酬率報告",
    "每季 15日 00:00": "📊 台積電財報分析",
    "每季 15日 00:00": "📊 輝達財報分析",
    "每季 15日 00:00": "📊 美股七雄彙整",
}

def get_current_time_slot():
    """取得當前時間對應的任務"""
    now = datetime.datetime.now()
    current_hour = now.hour
    weekday = now.weekday()  # 0=週一, 6=週日
    
    tasks = []
    
    # 檢查每日任務
    for time_str, task_name in DAILY_SCHEDULE.items():
        if ":" in time_str:
            hour = int(time_str.split(":")[0])
            if hour <= current_hour:
                tasks.append({"time": time_str, "task": task_name, "status": "待執行"})
    
    # 檢查每週任務
    week_keys = {
        0: "週一",  # 週一
        1: "週二",  # 週二
        2: "週三",  # 週三
        3: "週四",  # 週四
        4: "週五",  # 週五
        5: "週六",  # 週六
        6: "週日",  # 週日
    }
    today_prefix = week_keys.get(weekday, "")
    
    for time_str, task_name in WEEKLY_SCHEDULE.items():
        if time_str.startswith(today_prefix):
            time_part = time_str.split(" ")[1] if " " in time_str else "09:00"
            hour = int(time_part.split(":")[0])
            if hour <= current_hour:
                tasks.append({"time": time_str, "task": task_name, "status": "待執行"})
    
    return tasks

def generate_schedule_summary():
    """產生行程摘要"""
    now = datetime.datetime.now()
    weekday_names = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    
    summary = f"""
📅 **川寶投顧小安 - 每日行程摘要**

📆 日期：{now.strftime('%Y年%m月%d日')} {weekday_names[now.weekday()]}

━━━━━━━━━━━━━━━━━━

📊 **今日待執行任務**

"""
    
    # 每日任務
    summary += "\n**【每日任務】**\n"
    for time_str, task_name in sorted(DAILY_SCHEDULE.items()):
        summary += f"• {time_str} → {task_name}\n"
    
    # 每週任務（根據今天）
    summary += f"\n**【每週任務 - {weekday_names[now.weekday()]}】**\n"
    today_prefix = weekday_names[now.weekday()]
    for time_str, task_name in WEEKLY_SCHEDULE.items():
        if time_str.startswith(today_prefix):
            summary += f"• {time_str} → {task_name}\n"
    
    # 下班前任務
    summary += f"""
━━━━━━━━━━━━━━━━━━

💡 **小安提醒**

• 每日 06:00 前記得查看「全方位新聞快報」
• 股市開盤前（04:45）記得開啟晨間摘要
• 每週一、三、五記得追蹤任務執行

━━━━━━━━━━━━━━━━━━

🐰 **川寶投顧小安，專屬您的智能助理**

"""
    return summary

def send_telegram_message(text):
    """發送 Telegram 訊息"""
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
        '-d', f'chat_id={CHAT_ID}',
        '-d', f'text={text}',
        '-d', 'parse_mode=Markdown'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        response = json.loads(result.stdout)
        return response.get('ok', False)
    except:
        return False

# ===== 主程式 =====
def main():
    print("=" * 60)
    print("每日行程摘要 - 自動執行")
    print("=" * 60)
    print(f"時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 產生行程摘要
    summary = generate_schedule_summary()
    print(summary)
    
    # 發送到 Telegram
    if send_telegram_message(summary):
        print("\n✅ 已發送到 Telegram")
    else:
        print("\n❌ 發送失敗")
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()