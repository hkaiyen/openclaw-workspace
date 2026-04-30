#!/usr/bin/env python3
"""
川寶投顧 - TTS 快捷發送腳本
============================
用途：快速將文字轉換為語音並發送到Telegram

使用方式：
    python3 /root/.openclaw/workspace/scripts/tts_send.py "要說的話"

範例：
    python3 /root/.openclaw/workspace/scripts/tts_send.py "各位聽眾好，歡迎收聽川寶投顧"
"""

import asyncio
import edge_tts
import subprocess
import sys
import json

BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

async def tts_send(text, voice="zh-TW-HsiaoChenNeural"):
    """生成語音並發送到Telegram"""
    output_file = "/root/.openclaw/reports/daily/tts_quick.mp3"
    
    print(f"🎧 正在生成語音...")
    print(f"📝 內容：{text[:50]}...")
    
    # 生成語音
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"✅ 語音已生成")
    
    # 發送到Telegram
    print(f"📤 發送到Telegram...")
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendAudio',
        '-F', f'chat_id={CHAT_ID}',
        '-F', f'audio=@{output_file}',
        '-F', 'caption=🎧 川寶投顧 TTS 快捷語音'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        response = json.loads(result.stdout)
        if response.get('ok'):
            print(f"✅ 發送成功！")
        else:
            print(f"❌ 發送失敗：{response}")
    except:
        print(f"❌ 發送錯誤：{result.stdout}")

def main():
    if len(sys.argv) < 2:
        print("使用方法：python3 tts_send.py \"要說的話\"")
        print("範例：python3 tts_send.py \"各位聽眾好，歡迎收聽川寶投顧\"")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    asyncio.run(tts_send(text))

if __name__ == "__main__":
    main()