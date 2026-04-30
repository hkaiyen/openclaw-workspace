#!/usr/bin/env python3
"""
川寶投顧 × NotebookLM 研究報告自動化腳本
=================================================
用途：將Word報告自動上傳至NotebookLM，生成含封面簡報，並發送到Telegram

使用方式：
    python3 notebooklm_report.py "研究主題" "/path/to/report.docx"

範例：
    python3 notebooklm_report.py "下週台股挑戰40,000點分析" "/root/.openclaw/reports/daily/下週台股挑戰40,000點可行性分析.docx"
"""

import subprocess
import sys
import os
import json
import time
import re

# ===== 設定區 =====
TELEGRAM_BOT_TOKEN = "8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw"
TELEGRAM_CHAT_ID = "8779713208"

def run_cmd(cmd, timeout=30, yield_ms=10000):
    """執行命令並回傳結果"""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=timeout
    )
    return result.stdout, result.stderr, result.returncode

def send_telegram(file_path, caption):
    """發送檔案到Telegram"""
    cmd = f'''curl -s -X POST "https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument" -F "chat_id={TELEGRAM_CHAT_ID}" -F "document=@{file_path}" -F "caption={caption}"'''
    stdout, stderr, code = run_cmd(cmd, timeout=60)
    try:
        result = json.loads(stdout)
        if result.get('ok'):
            print("✅ 發送到Telegram成功")
            return True
        else:
            print(f"❌ Telegram發送失敗: {result}")
            return False
    except:
        print(f"❌ Telegram錯誤: {stdout}")
        return False

def notebooklm_create(title):
    """建立新的NotebookLM notebook"""
    print(f"📝 建立NotebookLM：{title}")
    stdout, stderr, code = run_cmd(f'notebooklm create "{title}"', timeout=30)
    if code != 0:
        print(f"❌ 建立notebook失敗: {stderr}")
        return None
    
    # 解析輸出的notebook ID
    match = re.search(r'Created notebook: (\S+) -', stdout)
    if match:
        notebook_id = match.group(1)
        print(f"✅ Notebook ID: {notebook_id}")
        return notebook_id
    else:
        print(f"❌ 無法解析notebook ID: {stdout}")
        return None

def notebooklm_add_source(file_path, notebook_id):
    """新增來源檔案到notebook"""
    print(f"📄 新增來源：{file_path}")
    cmd = f'notebooklm source add "{file_path}" --notebook "{notebook_id}"'
    stdout, stderr, code = run_cmd(cmd, timeout=60)
    
    if "Added source:" in stdout or code == 0:
        print(f"✅ 來源已新增")
        return True
    else:
        print(f"⚠️ 新增來源: {stdout} {stderr}")
        return True  # 繼續執行

def notebooklm_generate_slide(notebook_id, prompt):
    """生成簡報（含封面）"""
    print(f"🎨 生成簡報中...")
    cmd = f'notebooklm generate slide-deck "{prompt}" --notebook "{notebook_id}"'
    stdout, stderr, code = run_cmd(cmd, timeout=30)
    
    if "Started:" in stdout:
        artifact_id = stdout.split("Started:")[1].strip()
        print(f"✅ 生成任務已啟動，ID: {artifact_id}")
        return artifact_id
    else:
        print(f"❌ 生成失敗: {stderr}")
        return None

def notebooklm_wait_complete(notebook_id, artifact_id, timeout=300):
    """等待簡報生成完成"""
    print(f"⏳ 等待簡報生成...")
    elapsed = 0
    while elapsed < timeout:
        time.sleep(30)
        elapsed += 30
        
        stdout, stderr, code = run_cmd(
            f'notebooklm artifact list --notebook "{notebook_id}"',
            timeout=30
        )
        
        if artifact_id in stdout:
            if "completed" in stdout:
                print(f"✅ 簡報生成完成")
                return True
            elif "failed" in stdout:
                print(f"❌ 簡報生成失敗")
                return False
        print(f"⏳ 等待中... ({elapsed}秒)")
    
    print(f"⏰ 逾時")
    return False

def notebooklm_download(artifact_id, notebook_id, output_path):
    """下載簡報"""
    print(f"📥 下載簡報...")
    cmd = f'notebooklm download slide-deck "{output_path}" --notebook "{notebook_id}" --artifact "{artifact_id}"'
    stdout, stderr, code = run_cmd(cmd, timeout=60, yield_ms=30000)
    
    if os.path.exists(output_path):
        # 檢查實際檔案格式
        result = subprocess.run(['file', output_path], capture_output=True, text=True)
        file_type = result.stdout
        
        if 'PNG image data' in file_type:
            # 資訊圖表是PNG，需要修正副檔名並用Photo發送
            png_path = output_path.replace('.pdf', '.png').replace('.pptx', '.png')
            subprocess.run(['mv', output_path, png_path])
            output_path = png_path
            print(f"✅ 簡報已下載（PNG格式）: {output_path}")
        else:
            print(f"✅ 簡報已下載: {output_path}")
        return True
    else:
        print(f"❌ 下載失敗: {stderr}")
        return False

def main():
    # 解析參數
    if len(sys.argv) < 3:
        print("使用方法：python3 notebooklm_report.py \"研究主題\" \"Word檔路徑\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    docx_path = sys.argv[2]
    
    # 檢查檔案是否存在
    if not os.path.exists(docx_path):
        print(f"❌ 檔案不存在：{docx_path}")
        sys.exit(1)
    
    print("=" * 50)
    print(f"📊 研究主題：{topic}")
    print(f"📄 來源檔案：{docx_path}")
    print("=" * 50)
    
    # Step 1: 建立NotebookLM notebook
    notebook_id = notebooklm_create(topic)
    if not notebook_id:
        print("❌ 流程終止")
        sys.exit(1)
    
    # Step 2: 新增來源檔案
    if not notebooklm_add_source(docx_path, notebook_id):
        print("❌ 新增來源失敗")
    
    time.sleep(5)
    
    # Step 3: 生成簡報（包含封面）
    prompt = f"""請用繁體中文製作一份專業簡報，主題為「{topic}」。第一頁必須是封面頁，內容包括：

【封面頁】
■ 報告標題：{topic}
■ 研究日期：2026年4月26日
■ 研究團隊：
  - 🐰 小安（總體分析師）- MiniMax M2
  - 📚 拉瑪（趨勢分析師）- Groq (Llama)
  - 🔍 千問（技術分析師）- Groq (Qwen3-32B)
  - 💰 小歐（財務分析師）- Groq (GPT-OSS)
  - 🐂 撈仔（行銷分析師）- Groq (Llama)
■ 研究工具：sessions_spawn 模式 + NotebookLM
■ 使用模型：MiniMax M2 / Groq 系列
■ 備註：本報告僅供參考，不構成投資建議

請用繁體中文呈現全部內容。"""
    
    artifact_id = notebooklm_generate_slide(notebook_id, prompt)
    if not artifact_id:
        print("❌ 流程終止")
        sys.exit(1)
    
    # Step 4: 等待生成完成
    if not notebooklm_wait_complete(notebook_id, artifact_id):
        print("❌ 簡報生成逾時")
        sys.exit(1)
    
    # Step 5: 下載簡報
    # 轉換主題為檔名（移除特殊字元）
    safe_name = re.sub(r'[\\/:*?"<>|]', '', topic)
    output_path = f"/root/.openclaw/reports/daily/{safe_name}.pdf"
    
    if not notebooklm_download(artifact_id, notebook_id, output_path):
        print("❌ 下載失敗")
        sys.exit(1)
    
    # Step 6: 發送到Telegram
    caption = f"📊 {topic}（NotebookLM繁體中文版·含封面）| 川寶投顧"
    send_telegram(output_path, caption)
    
    print("=" * 50)
    print("✅ 任務完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()