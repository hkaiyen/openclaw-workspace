#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
川寶投顧 - 圖片生成腳本
==================
支援多種圖片生成方式：
1. MiniMax API
2. Gemini API (使用OAuth)
3. 備用：使用已有圖片

使用方式：
    python3 generate_daily_image.py "金句內容" "風格描述"
    python3 generate_daily_image.py "學習是最佳的投資" "一本打開的書漂浮在星空背景上"
"""

import os
import sys
import json
import urllib.request
import base64
import datetime

# ===== 設定 =====
OUTPUT_DIR = '/root/.openclaw/media'
MINIMAX_API_KEY = ''  # MiniMax API Key
GEMINI_API_KEY = ''  # Gemini API Key
BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

def generate_image_minimax(prompt, output_path):
    """使用 MiniMax API 生成圖片"""
    if not MINIMAX_API_KEY:
        print("❌ MiniMax API Key 未設定")
        return False
    
    print(f"🎨 嘗試 MiniMax API...")
    
    url = "https://api.minimax.chat/v1/image_generation"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "num_images": 1,
        "aspect_ratio": "16:9"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        if 'data' in result and len(result['data']) > 0:
            image_url = result['data'][0].get('url', '')
            if image_url:
                # 下載圖片
                img_req = urllib.request.Request(image_url)
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    with open(output_path, 'wb') as f:
                        f.write(img_resp.read())
                print(f"✅ MiniMax 成功！")
                return True
        
        print(f"❌ MiniMax 失敗: {result}")
        return False
        
    except Exception as e:
        print(f"❌ MiniMax 錯誤: {e}")
        return False

def generate_image_gemini(prompt, output_path):
    """使用 Gemini API 生成圖片"""
    if not GEMINI_API_KEY:
        print("❌ Gemini API Key 未設定")
        return False
    
    print(f"🎨 嘗試 Gemini API...")
    
    # 嘗試多個模型
    models = [
        'gemini-2.0-flash-exp',
        'imagen-3.0-generate-preview'
    ]
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"請生成一張精美的圖片，主題是：{prompt}。圖片要專業、美觀、適合作為每日金句海報。"}]
            }]
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            if 'candidates' in result:
                parts = result['candidates'][0].get('content', {}).get('parts', [])
                for part in parts:
                    if 'inlineData' in part:
                        image_data = part['inlineData']['data']
                        image_bytes = base64.b64decode(image_data)
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)
                        print(f"✅ Gemini ({model}) 成功！")
                        return True
            
        except Exception as e:
            print(f"  ❌ {model}: {e}")
            continue
    
    return False

def generate_image_gemini_oauth(prompt, output_path):
    """使用 Gemini OAuth (已認證的 NotionLM)"""
    print(f"🎨 嘗試 Gemini OAuth...")
    
    # 檢查是否有認証檔案
    storage_path = '/root/.notebooklm/storage_state.json'
    if not os.path.exists(storage_path):
        print("  ❌ 未找到 NotebookLM 認証檔案")
        return False
    
    try:
        with open(storage_path, 'r') as f:
            storage = json.load(f)
        
        cookies = storage.get('cookies', [])
        
        # 找 SID cookie
        sid_cookie = None
        for c in cookies:
            if c.get('name') in ['SID', '__Secure-1PSID', 'OSID']:
                sid_cookie = c
                break
        
        if not sid_cookie:
            print("  ❌ 未找到認証 cookie")
            return False
        
        # 嘗試使用 cookie 訪問 Gemini
        print("  ⚠️ Gemini OAuth 需要瀏覽器，無法直接使用")
        return False
        
    except Exception as e:
        print(f"  ❌ OAuth 錯誤: {e}")
        return False

def use_placeholder_image(quote, output_path):
    """使用備用圖片（已有的金句圖）"""
    print(f"📦 使用備用圖片...")
    
    # 檢查是否有已生成的圖片
    today = datetime.datetime.now().strftime('%Y%m%d')
    placeholder_paths = [
        f'{OUTPUT_DIR}/daily_quote_{today}.png',
        f'{OUTPUT_DIR}/daily_quote.png',
        f'{OUTPUT_DIR}/quote_template.png',
        '/root/.openclaw/media/cat_meme.png',  # 借用貓咪圖
    ]
    
    for path in placeholder_paths:
        if os.path.exists(path):
            import shutil
            shutil.copy(path, output_path)
            print(f"✅ 已複製備用圖片: {path}")
            return True
    
    print("❌ 無備用圖片可用")
    return False

def create_text_image(quote, output_path):
    """建立純文字圖片（最後備用方案）"""
    print(f"📝 建立純文字圖片...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 創建圖片
        width, height = 1200, 630
        bg_color = (25, 35, 50)  # 深藍色
        text_color = (255, 255, 255)  # 白色
        
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # 嘗試載入字體
        try:
            font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)
            font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 36)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # 繪製標題
        title = "🦅 川寶投顧"
        draw.text((width//2, 100), title, fill=text_color, font=font_large, anchor='mm')
        
        # 繪製金句
        draw.text((width//2, height//2), f"「{quote}」", fill=(255, 215, 0), font=font_large, anchor='mm')
        
        # 繪製底部
        today = datetime.datetime.now().strftime('%Y年%m月%d日')
        draw.text((width//2, height-80), today, fill=(150, 150, 150), font=font_small, anchor='mm')
        
        img.save(output_path, 'PNG')
        print(f"✅ 純文字圖片已生成: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 文字圖片錯誤: {e}")
        return False

def send_to_telegram(image_path, caption):
    """發送到 Telegram"""
    if not os.path.exists(image_path):
        print(f"❌ 圖片不存在: {image_path}")
        return False
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto',
        '-F', f'chat_id={CHAT_ID}',
        '-F', f'photo=@{image_path}',
        '-F', f'caption={caption}'
    ]
    
    result = os.system(' '.join(cmd) + ' > /dev/null 2>&1')
    if result == 0:
        print(f"✅ 已發送到 Telegram")
        return True
    else:
        print(f"❌ Telegram 發送失敗")
        return False

def main():
    print("=" * 60)
    print("川寶投顧 - 圖片生成腳本")
    print("=" * 60)
    
    # 解析參數
    if len(sys.argv) >= 3:
        quote = sys.argv[1]
        style = sys.argv[2]
    else:
        # 預設值
        quote = "學習是最佳的投資。"
        style = "一本打開的書漂浮在星空背景上，書頁散發柔和光芒，文字清晰可讀，極簡風格，深藍色夜空襯托。"
    
    prompt = f"每日金句：「{quote}」。設計：{style}"
    
    print(f"\n💬 金句：{quote}")
    print(f"🎨 風格：{style}")
    print(f"📝 Prompt：{prompt[:100]}...")
    
    # 設定輸出路徑
    today = datetime.datetime.now().strftime('%Y%m%d')
    output_path = f'{OUTPUT_DIR}/daily_quote_{today}.png'
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    success = False
    
    # 嘗試各種方法
    methods = [
        ("MiniMax", lambda: generate_image_minimax(prompt, output_path)),
        ("Gemini", lambda: generate_image_gemini(prompt, output_path)),
        ("Gemini OAuth", lambda: generate_image_gemini_oauth(prompt, output_path)),
        ("備用圖片", lambda: use_placeholder_image(quote, output_path)),
        ("文字圖片", lambda: create_text_image(quote, output_path)),
    ]
    
    for name, func in methods:
        print(f"\n嘗試 {name}...")
        if func():
            success = True
            break
    
    if success:
        # 發送到 Telegram
        caption = f"💬 每日金句：「{quote}」| 川寶投顧"
        send_to_telegram(output_path, caption)
        print(f"\n✅ 完成！")
        print(f"📁 圖片：{output_path}")
    else:
        print(f"\n❌ 所有方法都失敗了")
    
    print("=" * 60)

if __name__ == '__main__':
    main()