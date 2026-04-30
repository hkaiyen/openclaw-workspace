#!/usr/bin/python3
"""
產品總監型自動化 AI Agent
從 0 到 1 建立產品的自主代理
"""

import json
import os
from datetime import datetime

MEMORY_FILE = '/root/.openclaw/workspace/memory/product_director_memory.json'

# ========== 預設 Memory ==========
DEFAULT_MEMORY = {
    "goal": "7天內建立AI工具",
    "product_idea": "",
    "current_task": "",
    "tasks_done": [],
    "progress": 0,
    "problems": [],
    "created_at": "",
    "last_updated": ""
}

# ========== 工具函數 ==========

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_MEMORY.copy()

def save_memory(memory):
    memory['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# ========== 主程式 ==========

def run_agent():
    memory = load_memory()
    
    # 輸出 JSON 格式
    output = {
        "thinking": "讀取 memory，檢查當前狀態",
        "task": memory.get('current_task', '尚未設定任務'),
        "type": "research",
        "tool": "file",
        "expected_output": "更新後的 memory 狀態",
        "progress_percent": memory.get('progress', 0),
        "tasks_done_count": len(memory.get('tasks_done', [])),
        "status": memory.get('current_task', '等待任務'),
        "done": False
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    return output

def get_status():
    """取得 Agent 狀態"""
    memory = load_memory()
    return {
        "goal": memory.get('goal', ''),
        "product_idea": memory.get('product_idea', '未設定'),
        "current_task": memory.get('current_task', '無'),
        "progress_percent": memory.get('progress', 0),
        "tasks_done_count": len(memory.get('tasks_done', [])),
        "tasks_done": memory.get('tasks_done', []),
        "last_updated": memory.get('last_updated', '從未更新')
    }

def reset_agent():
    """重置 Agent"""
    memory = DEFAULT_MEMORY.copy()
    memory['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_memory(memory)
    
    output = {
        "thinking": "Agent 已重置",
        "task": "等待新任務",
        "type": "system",
        "tool": "none",
        "expected_output": "Memory 已清空",
        "progress_percent": 0,
        "tasks_done_count": 0,
        "status": "已重置",
        "done": False
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--status':
            status = get_status()
            print(json.dumps(status, ensure_ascii=False, indent=2))
        elif sys.argv[1] == '--reset':
            reset_agent()
        else:
            print('用法: python3 product_director_agent.py [--status|--reset]')
    else:
        run_agent()
