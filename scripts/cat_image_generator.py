#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
貓咪梗圖生成器 - 由潔咪 sub-agent 生成
"""
import sys
import os

# 載入 OpenClaw tools
sys.path.insert(0, '/root/openclaw')

from tools import sessions_spawn

def main():
    print("🖼️ 潔咪：生成貓咪梗圖...")
    
    prompt = """Generate a funny cat meme image for '貓咪研究社' weekly report.
Style: Cute cartoon cat wearing a tiny business suit, sitting like a CEO in front of multiple computer screens showing stock charts. 
The cat should have a confident smirk expression, holding a tiny coffee cup.
Colorful, high quality cartoon style.
Save the image to: /root/.openclaw/media/cat_meme.png"""
    
    try:
        result = sessions_spawn(
            task=f'Generate and save a funny cat meme image. Prompt: {prompt}. Save to /root/.openclaw/media/cat_meme.png',
            runtime='subagent',
            agent_id='jie_mi',
            mode='run',
            timeout=120
        )
        print(f"✅ 潔咪完成: {result}")
        
        if os.path.exists('/root/.openclaw/media/cat_meme.png'):
            print("✅ 圖片已生成: /root/.openclaw/media/cat_meme.png")
        else:
            print("⚠️ 圖片未生成")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == '__main__':
    main()
