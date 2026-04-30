#!/usr/bin/env python3
"""
台股AI每日精選 - Telegram Bot 完整版
處理訂閱、用戶管理、每日報告推播
"""

import subprocess
import datetime
import json
import os
import time
import requests

BOT_TOKEN = "8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw"
SUBSCRIBERS_FILE = "/root/.openclaw/workspace/product/tw-stock-ai/subscribers.json"
REPORTS_DIR = "/root/.openclaw/reports/daily"
OFFSET_FILE = "/root/.openclaw/workspace/product/tw-stock-ai/last_offset.txt"

def log(msg):
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def api(method, **params):
    r = requests.post(f"{BASE_URL}/{method}", data=params, timeout=30)
    return r.json()

def get_updates(offset=None, timeout=30):
    params = {"timeout": timeout, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    r = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=timeout + 5)
    return r.json()

def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE) as f:
            return json.load(f)
    return {"subscribers": [], "count": 0}

def save_subscribers(data):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def send_message_to_chat(chat_id, text):
    log(f"發送訊息到 {chat_id}")
    r = requests.post(f"{BASE_URL}/sendMessage", data={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, timeout=30)
    return r.json()

def send_document_to_chat(chat_id, file_path, caption=""):
    log(f"發送文件到 {chat_id}: {file_path}")
    with open(file_path, 'rb') as f:
        r = requests.post(f"{BASE_URL}/sendDocument", data={"chat_id": chat_id, "caption": caption}, files={"document": f}, timeout=60)
    return r.json()

def subscribe_user(chat_id, username=""):
    data = load_subscribers()
    for s in data["subscribers"]:
        if s.get("chat_id") == chat_id:
            return False
    data["subscribers"].append({
        "chat_id": chat_id,
        "username": username,
        "subscribed_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    data["count"] = len(data["subscribers"])
    save_subscribers(data)
    log(f"新訂閱: {chat_id} (@{username})")
    return True

def unsubscribe_user(chat_id):
    data = load_subscribers()
    data["subscribers"] = [s for s in data["subscribers"] if s.get("chat_id") != chat_id]
    data["count"] = len(data["subscribers"])
    save_subscribers(data)
    return True

def broadcast_report():
    log("開始廣播報告...")
    data = load_subscribers()
    if not os.path.exists(REPORTS_DIR):
        return {"sent": 0, "failed": 0, "error": "報告目錄不存在"}

    report_files = sorted([f for f in os.listdir(REPORTS_DIR) if f.startswith('股市觀測站_') and f.endswith('.docx')])
    if not report_files:
        return {"sent": 0, "failed": 0, "error": "今日無報告"}

    report_path = f"{REPORTS_DIR}/{report_files[-1]}"
    today = datetime.datetime.now().strftime('%Y年%m月%d日')
    sent = failed = 0

    for sub in data["subscribers"]:
        cid = sub.get("chat_id")
        try:
            result = send_document_to_chat(cid, report_path, f"📈 台股AI每日精選 ({today})\n\n親愛的用户您好，這是今日的股市報告")
            if result.get('ok'):
                sent += 1
            else:
                failed += 1
                log(f"發送失敗 {cid}: {result}")
        except Exception as e:
            failed += 1
            log(f"例外 {cid}: {e}")

    return {"sent": sent, "failed": failed}

def handle_command(text, chat_id, username=""):
    text = text.strip()

    if text == "/start" or text.startswith("/start "):
        # Deep link: /start subscribe
        param = text.split(" ", 1)[-1]
        success = subscribe_user(chat_id, username)
        if success:
            msg = """✅ <b>訂閱成功！</b>

歡迎加入 台股AI每日精選！

📈 每天8:30為您推送：
• 大盤分析
• 精選3檔潛力股
• 最新新聞摘要

輸入 /help 查看更多指令"""
        else:
            msg = """👋 您已經是訂閱會員了！

輸入 /help 查看可用指令"""
        return send_message_to_chat(chat_id, msg)

    elif text == "/stop":
        unsubscribe_user(chat_id)
        return send_message_to_chat(chat_id, """❌ <b>已取消訂閱</b>

不再為您發送每日精選
輸入 /start 重新訂閱""")

    elif text == "/help":
        return send_message_to_chat(chat_id, """📖 <b>指令說明</b>

/start - 訂閱每日精選
/stop - 取消訂閱
/status - 查詢訂閱狀態
/report - 手動取得今日報告""")

    elif text == "/status":
        data = load_subscribers()
        is_sub = any(s.get("chat_id") == chat_id for s in data["subscribers"])
        if is_sub:
            return send_message_to_chat(chat_id, f"✅ <b>您是訂閱會員</b>\n\n目前共有 {data['count']} 位訂閱者")
        return send_message_to_chat(chat_id, "❌ <b>您尚未訂閱</b>\n\n輸入 /start 開始訂閱")

    elif text == "/report":
        data = load_subscribers()
        if any(s.get("chat_id") == chat_id for s in data["subscribers"]):
            result = broadcast_report()
            return send_message_to_chat(chat_id, f"📤 報告已發送給您\n\n結果: {result}")
        return send_message_to_chat(chat_id, "❌ <b>請先訂閱</b>\n\n輸入 /start 開始訂閱")

    else:
        return send_message_to_chat(chat_id, "🤔 不懂的指令\n\n輸入 /help 查看可用指令")

def load_offset():
    try:
        with open(OFFSET_FILE) as f:
            return int(f.read().strip())
    except:
        return None

def save_offset(offset):
    with open(OFFSET_FILE, 'w') as f:
        f.write(str(offset))

def poll():
    offset = load_offset()
    log("🤖 Bot 啟動，開始接收訊息...")
    try:
        send_message_to_chat("8779713208", "✅ <b>台股AI每日精選 Bot 已上線！</b>\n\n• 訂閱系統：✅\n• 報告廣播：✅\n• 用戶管理：✅")
    except Exception as e:
        log(f"通知管理員失敗: {e}")

    while True:
        try:
            updates = get_updates(offset=offset, timeout=30)
            if not updates.get("ok"):
                time.sleep(5)
                continue
            results = updates.get("result", [])
            if not results:
                continue

            for update in results:
                offset = update["update_id"] + 1
                message = update.get("message")
                if not message:
                    continue
                chat_id = str(message["chat"]["id"])
                text = message.get("text", "")
                username = message.get("from", {}).get("username", "")
                log(f"收到: [{chat_id}] {text}")
                try:
                    handle_command(text, chat_id, username)
                except Exception as e:
                    log(f"處理錯誤: {e}")
                    try:
                        send_message_to_chat("8779713208", f"⚠️ Bot 錯誤：{e}")
                    except:
                        pass

            save_offset(offset)

        except requests.exceptions.RequestException as e:
            log(f"網路錯誤: {e}，5秒後重試...")
            time.sleep(5)
        except Exception as e:
            log(f"未知錯誤: {e}")
            time.sleep(5)

if __name__ == '__main__':
    poll()
