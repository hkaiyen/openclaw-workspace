#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 深度研究報告 NotebookLM PPT 生成腳本
川寶投顧 × NotebookLM

流程：
1. 上傳 Word 報告到 NotebookLM
2. 生成 PPT
3. 發送到 Telegram
"""

import subprocess
import sys
import datetime
import time
import os

# 研究主題（從命令列參數取得）
TOPIC = sys.argv[1] if len(sys.argv) > 1 else "深度研究報告"
DATE_STR = datetime.datetime.now().strftime("%Y%m%d")

# NotebookLM 設定
NOTEBOOK_NAME = f"深度研究_{TOPIC}_{DATE_STR}"

# Telegram 設定
BOT_TOKEN = "8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw"
CHAT_ID = "8779713208"

def run_cmd(cmd, timeout=30):
    """執行命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"錯誤: {str(e)}"

def notebooklm_cmd(args_str):
    """執行 NotebookLM 命令"""
    cmd = f"notebooklm {args_str}"
    return run_cmd(cmd, timeout=60)

def send_telegram(docx_path, caption):
    """發送到 Telegram"""
    import requests
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    with open(docx_path, 'rb') as f:
        files = {'document': f}
        data = {
            'chat_id': CHAT_ID,
            'caption': caption
        }
        try:
            response = requests.post(url, files=files, data=data, timeout=60)
            result = response.json()
            if result.get('ok'):
                print(f"✅ 已發送到 Telegram")
                return True
            else:
                print(f"❌ Telegram 發送失敗: {result}")
                return False
        except Exception as e:
            print(f"❌ Telegram 發送例外: {e}")
            return False

def find_latest_report():
    """找最新研究報告"""
    report_dir = "/root/.openclaw/reports/daily/"
    if not os.path.exists(report_dir):
        report_dir = "/root/.openclaw/workspace/reports/"
    
    # 找最新的 docx 檔案
    cmd = f"find {report_dir} -name '*深度研究*.docx' -type f 2>/dev/null | sort -r | head -1"
    result = run_cmd(cmd).strip()
    return result if result and os.path.exists(result) else None

def main():
    print(f"[{datetime.datetime.now()}] === NotebookLM PPT 生成 ===")
    print(f"主題：{TOPIC}")
    print()
    
    # Step 1: 找最新研究報告
    print("Step 1: 找最新研究報告...")
    report_path = find_latest_report()
    
    # 如果有指定報告路徑，用指定的
    if len(sys.argv) > 2:
        report_path = sys.argv[2]
    
    if not report_path or not os.path.exists(report_path):
        print(f"❌ 找不到研究報告，請確認 Word 報告已生成")
        sys.exit(1)
    
    print(f"✅ 研究報告：{report_path}")
    print()
    
    # Step 2: 建立 NotebookLM 筆記本
    print("Step 2: 建立 NotebookLM 筆記本...")
    result = notebooklm_cmd(f'create "{NOTEBOOK_NAME}"')
    if "Created notebook:" in result or "created:" in result.lower():
        # 取出 notebook ID
        for line in result.split('\n'):
            if 'Created notebook:' in line or '-' in line and len(line) > 30:
                notebook_id = line.split()[-1].strip()
                print(f"✅ Notebook ID：{notebook_id}")
                break
        else:
            # 從 result 中解析
            import re
            match = re.search(r'([a-f0-9-]{36})', result)
            if match:
                notebook_id = match.group(1)
            else:
                print(f"❌ 無法解析 Notebook ID：{result}")
                sys.exit(1)
    else:
        print(f"❌ 建立筆記本失敗：{result}")
        sys.exit(1)
    print()
    
    # Step 3: 上傳研究報告
    print("Step 3: 上傳研究報告...")
    result = notebooklm_cmd(f'source add "{report_path}" --notebook {notebook_id}')
    if "Added source:" in result or "added source" in result.lower():
        print(f"✅ 研究報告已上傳")
    else:
        print(f"⚠️ 上傳結果：{result}")
    print()
    
    # Step 4: 通知開始生成 PPT
    print("Step 4: 要求 NotebookLM 生成 PPT...")
    prompt = """請用繁體中文回答。我希望生成PPT演示文稿，風格要求：採用顧問報告風格（麥肯錫 / BCG-like），每頁使用金字塔原理結構：頁首大標題 + 3–4 個關鍵論點 bullet，每個 bullet 後接 1 句支撐說明 + 數據 / 圖示佐證，配色為深藍 + 灰 + 少量亮藍強調，背景全白或極淺漸層，加入細線分隔與小型圖標輔助理解，整體邏輯清晰，專業嚴謹。請用中文繁體生成。"""
    result = notebooklm_cmd(f'ask "{prompt}" --notebook {notebook_id}')
    print(f"✅ 已要求生成 PPT")
    print()
    
    # Step 5: 生成 PPT（後台執行）
    print("Step 5: 啟動 PPT 生成...")
    generate_cmd = f"notebooklm generate slide-deck --notebook {notebook_id} --language zh_Hant --wait"
    print(f"📝 命令：{generate_cmd}")
    
    # 使用 nohup 後台執行
    log_file = f"/root/.openclaw/logs/notebooklm_ppt_{DATE_STR}.log"
    bg_cmd = f"nohup {generate_cmd} > {log_file} 2>&1 &"
    run_cmd(bg_cmd)
    print(f"✅ PPT 生成已啟動（日誌：{log_file}）")
    print()
    
    # 發送進度通知
    send_telegram(report_path, f"📊 深度研究報告：{TOPIC}\n\n✅ Word 報告完成\n🔄 NotebookLM PPT 生成中...\n\nPPT 完成後將自動發送。")
    
    print("=" * 50)
    print("📋 執行完成！")
    print("PPT 生成完成後會自動發送到 Telegram")
    print("=" * 50)

if __name__ == '__main__':
    main()
