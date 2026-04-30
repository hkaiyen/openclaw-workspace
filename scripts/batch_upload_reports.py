#!/usr/bin/env python3
"""批量上傳報告到網站，自動分類刪除重複"""
import os
import sys
import glob
import subprocess
from docx import Document

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from upload_website import upload_to_website, update_index_page

# 報告位置
report_dirs = [
    "/root/.openclaw/workspace/reports",
    "/Users/hsuehkaiyen/Desktop/📂 OpenClaw_下載/reports/daily"
]

# 收集所有報告，按名稱分組
reports_by_type = {}

for dir_path in report_dirs:
    if not os.path.exists(dir_path):
        continue
    
    for file_path in glob.glob(f"{dir_path}/*.docx"):
        file_name = os.path.basename(file_path)
        
        # 判斷類型
        if "資產報酬率" in file_name or "股市" in file_name or "股票" in file_name:
            category = "股市"
            base_name = "資產報酬率報告"
        elif "房地產" in file_name or "房價" in file_name:
            category = "房地產"
            base_name = "房地產報告"
        elif "促銷" in file_name or "活動" in file_name:
            category = "促銷"
            base_name = "促銷活動報告"
        elif "壓力" in file_name or "心理" in file_name or "健康" in file_name:
            category = "研究"
            base_name = "壓力管理報告"
        elif "人際" in file_name or "情感" in file_name:
            category = "研究"
            base_name = "人際關係報告"
        elif "遠距" in file_name or "自由工作者" in file_name:
            category = "研究"
            base_name = "遠距工作報告"
        else:
            category = "研究"
            base_name = file_name.replace('.docx', '')
        
        # 只保留最新的一份
        if base_name not in reports_by_type:
            reports_by_type[base_name] = {'path': file_path, 'category': category, 'mtime': 0}
        
        # 檢查時間
        file_mtime = os.path.getmtime(file_path)
        if file_mtime > reports_by_type[base_name]['mtime']:
            reports_by_type[base_name] = {'path': file_path, 'category': category, 'mtime': file_mtime}

print(f"找到 {len(reports_by_type)} 種不同報告\n")

# 上傳每個報告
for base_name, info in sorted(reports_by_type.items()):
    print(f"📤 上傳：{base_name}")
    print(f"   位置：{info['category']}")
    upload_to_website(info['path'])
    print()

# 更新首頁
print("📝 更新首頁...")
update_index_page()

# Git push
print("🚀 推送到 GitHub...")
try:
    subprocess.run(['git', 'add', '.'], cwd='/root/.openclaw/workspace/reports_site', check=True, capture_output=True)
    subprocess.run(['git', 'commit', '-m', f'批量上傳報告 {len(reports_by_type)} 份'], 
                   cwd='/root/.openclaw/workspace/reports_site', check=True, capture_output=True)
    subprocess.run(['git', 'push', 'origin', 'master'], 
                   cwd='/root/.openclaw/workspace/reports_site', check=True, capture_output=True, timeout=30)
    print("✅ 完成！")
except Exception as e:
    print(f"⚠️ Git推送失敗: {e}")