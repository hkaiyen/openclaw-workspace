#!/usr/bin/env python3
"""
川寶投顧 - Edge-TTS 快捷語音腳本
====================================
用途：快速將文字轉換為中文語音

使用方法：
    python3 /root/.openclaw/workspace/scripts/tts_quick.py "要說的話"

範例：
    python3 /root/.openclaw/workspace/scripts/tts_quick.py "各位聽眾好，歡迎收聽川寶投顧"
"""

import asyncio
import edge_tts
import sys

async def tts(text, voice="zh-TW-HsiaoChenNeural"):
    """快速生成中文語音"""
    output_file = "/root/.openclaw/reports/daily/tts_output.mp3"
    
    print(f"🎧 正在生成語音...")
    print(f"📝 內容：{text[:50]}...")
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    
    print(f"✅ 已生成：{output_file}")
    return output_file

def main():
    if len(sys.argv) < 2:
        print("使用方法：python3 tts_quick.py \"要說的話\"")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    asyncio.run(tts(text))

if __name__ == "__main__":
    main()