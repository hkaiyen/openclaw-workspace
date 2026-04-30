#!/usr/bin/env python3
"""
Google Drive 自動備份腳本
川寶投顧 × 小安
"""

import os
import sys
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 設定
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = '/root/.openclaw/google_drive/service_account.json'
FOLDER_ID = '15-_eQI-Xurs5WWwh0aLuFb3Z13gGwxDe'

# 備份來源目錄
BACKUP_SOURCES = [
    '/root/.openclaw/workspace/scripts/',
    '/root/.openclaw/reports/daily/',
    '/root/.openclaw/workspace/memory/',
]

def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

def upload_file(service, file_path, folder_id):
    """上傳檔案到 Google Drive"""
    if not os.path.exists(file_path):
        return None
    
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(file_path)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink'
    ).execute()
    
    return file

def backup_directory(service, directory, folder_id, extensions=None):
    """備份整個目錄"""
    if not os.path.exists(directory):
        print(f"  ⚠️ 目錄不存在：{directory}")
        return []
    
    uploaded = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if extensions and not any(file.endswith(ext) for ext in extensions):
                continue
            
            file_path = os.path.join(root, file)
            try:
                result = upload_file(service, file_path, folder_id)
                if result:
                    print(f"  ✅ {result['name']}")
                    uploaded.append(result)
            except Exception as e:
                print(f"  ❌ {file}: {e}")
    
    return uploaded

def main():
    print("=" * 50)
    print("📤 OpenClaw 備份到 Google Drive")
    print(f"時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        service = get_drive_service()
        print("✅ Google Drive 連線成功")
        
        total_uploaded = 0
        
        for source in BACKUP_SOURCES:
            print(f"\n📁 備份：{source}")
            uploaded = backup_directory(service, source, FOLDER_ID, 
                                       extensions=['.py', '.json', '.txt', '.md', '.docx', '.xlsx', '.pptx'])
            total_uploaded += len(uploaded)
            print(f"   已上傳 {len(uploaded)} 個檔案")
        
        print("\n" + "=" * 50)
        print(f"✅ 備份完成！共上傳 {total_uploaded} 個檔案")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ 備份失敗：{e}")
        return False

if __name__ == '__main__':
    main()
