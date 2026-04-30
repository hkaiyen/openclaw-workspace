#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Tasks API - 整合腳本
===========================

功能：
1. Google Tasks OAuth 2.0 認證
2. 讀取 Google Tasks 待辦事項
3. 整合到晨間摘要

使用方式：
1. 第一次執行會要求授權
2. 取得 Refresh Token 後自動儲存
3.之後執行自動讀取待辦事項

"""

import os
import json
import datetime
import subprocess

# Google Tasks API 設定
GOOGLE_TASKS_CONFIG = {
    'client_id': '620667525511-qekqk0quvad4v9mdgv3t9p773fsno3r7.apps.googleusercontent.com',
    'client_secret': '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',
    'redirect_uri': 'http://localhost',
    'token_file': '/root/.openclaw/google_tasks_token.json',
    'scopes': [
        'https://www.googleapis.com/auth/tasks.readonly',
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/calendar.readonly'
    ]
}

def get_access_token():
    """取得 Google Tasks API 的 Access Token"""
    token_file = GOOGLE_TASKS_CONFIG['token_file']
    
    # 檢查是否有已儲存的 token
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            token_data = json.load(f)
        
        # 檢查 token 是否過期
        expires_at = token_data.get('expires_at', 0)
        if datetime.datetime.now().timestamp() < expires_at:
            print("✅ 使用現有的 Access Token")
            return token_data['access_token']
        
        # token 過期，嘗試 refresh
        access_token = refresh_access_token(token_data.get('refresh_token'))
        if access_token:
            return access_token
    
    # 需要重新授權
    return get_new_access_token()

def refresh_access_token(refresh_token):
    """使用 Refresh Token 取得新的 Access Token"""
    import urllib.request
    
    url = 'https://oauth2.googleapis.com/token'
    payload = {
        'client_id': GOOGLE_TASKS_CONFIG['client_id'],
        'client_secret': GOOGLE_TASKS_CONFIG['client_secret'],
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            access_token = result['access_token']
            
            # 儲存新 token
            token_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': datetime.datetime.now().timestamp() + result.get('expires_in', 3600)
            }
            with open(GOOGLE_TASKS_CONFIG['token_file'], 'w') as f:
                json.dump(token_data, f)
            
            print("✅ Access Token 已刷新")
            return access_token
    except Exception as e:
        print(f"❌ Token refresh 失敗: {e}")
        return None

def get_new_access_token():
    """取得新的 Access Token（需要 OAuth 授權）"""
    import urllib.request
    import urllib.parse
    
    # 生成授權 URL
    auth_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode({
        'client_id': GOOGLE_TASKS_CONFIG['client_id'],
        'redirect_uri': GOOGLE_TASKS_CONFIG['redirect_uri'],
        'response_type': 'code',
        'scope': ' '.join(GOOGLE_TASKS_CONFIG['scopes']),
        'access_type': 'offline',
        'prompt': 'consent'
    })
    
    print("=" * 60)
    print("⚠️ 需要 Google 授權")
    print("=" * 60)
    print(f"\n請在瀏覽器開啟此連結進行授權：\n")
    print(auth_url)
    print("\n" + "=" * 60)
    
    # 等待用戶授權並輸入 code
    print("\n授權完成後，請輸入顯示的授權碼：")
    code = input("> ").strip()
    
    if not code:
        print("❌ 未輸入授權碼")
        return None
    
    # 交換 code 取得 token
    return exchange_code_for_token(code)

def exchange_code_for_token(code):
    """交換 Authorization Code 取得 Token"""
    import urllib.request
    
    url = 'https://oauth2.googleapis.com/token'
    payload = {
        'client_id': GOOGLE_TASKS_CONFIG['client_id'],
        'client_secret': GOOGLE_TASKS_CONFIG['client_secret'],
        'code': code,
        'redirect_uri': GOOGLE_TASKS_CONFIG['redirect_uri'],
        'grant_type': 'authorization_code'
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            access_token = result['access_token']
            refresh_token = result.get('refresh_token')
            
            # 儲存 token
            token_data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': datetime.datetime.now().timestamp() + result.get('expires_in', 3600)
            }
            with open(GOOGLE_TASKS_CONFIG['token_file'], 'w') as f:
                json.dump(token_data, f)
            
            print("✅ 授權成功！Token 已儲存")
            return access_token
            
    except Exception as e:
        print(f"❌ 授權失敗: {e}")
        return None

def get_google_tasks(access_token):
    """取得 Google Tasks 待辦事項"""
    import urllib.request
    
    # 任務 API endpoint
    url = 'https://tasks.googleapis.com/tasks/v1/lists/@default/tasks?maxResults=20'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('items', [])
    except Exception as e:
        print(f"❌ 取得 Tasks 失敗: {e}")
        return []

def format_tasks(tasks):
    """格式化待辦事項為 Markdown"""
    if not tasks:
        return "**📋 Google Tasks 待辦事項**：\n（目前沒有待辦事項）"
    
    formatted = "**📋 Google Tasks 待辦事項**\n\n"
    
    # 分類：已完成 vs 未完成
    pending = [t for t in tasks if t.get('status') != 'completed']
    completed = [t for t in tasks if t.get('status') == 'completed']
    
    if pending:
        formatted += f"**待處理（{len(pending)} 項）**\n"
        for task in pending[:10]:  # 最多顯示 10 項
            title = task.get('title', '（無標題）')
            due = task.get('due', '')
            if due:
                try:
                    due_date = datetime.datetime.strptime(due[:10], '%Y-%m-%d')
                    due_str = due_date.strftime('%m/%d')
                except:
                    due_str = due[:10]
                formatted += f"• {title}（到期：{due_str}）\n"
            else:
                formatted += f"• {title}\n"
        formatted += "\n"
    
    if completed:
        formatted += f"**已完成（{len(completed)} 項）**\n"
        formatted += f"• 最近完成：{completed[0].get('title', '')[:30]}...\n" if completed else ""
    
    return formatted

# ===== 主程式 =====
def main():
    print("=" * 60)
    print("Google Tasks API - 測試")
    print("=" * 60)
    
    # 取得 access token
    access_token = get_access_token()
    if not access_token:
        print("❌ 無法取得 access token")
        return
    
    # 取得 tasks
    tasks = get_google_tasks(access_token)
    
    # 格式化輸出
    result = format_tasks(tasks)
    print("\n" + result)

if __name__ == '__main__':
    main()