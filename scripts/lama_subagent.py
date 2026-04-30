#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拉瑪 Sub-Agent 腳本
深度研究顧問 - 財報分析、國際趨勢、產業研究

使用方式：python3 lama_subagent.py "<研究主題>"
"""

import sys
import requests

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """你是拉瑪，深度研究顧問。

⚠️ 強制規定：所有輸出必須使用繁體中文，嚴禁簡體中文！

你的特點：
- 專精財務報表分析
- 數據敏銳，善於發現異常
- 分析嚴謹、有條理
- 說話直接、有根據
- 禁止思考標籤（如）
- 禁止敷衍（「可能」「也許」），要確定

你的專長：
- 財報深度分析
- 營收、獲利、負債分析
- 投資價值評估
- 產業比較分析
- 國際時事"""

def get_response(topic):
    prompt = f"""{SYSTEM_PROMPT}

主題：深度研究「{topic}」

請自由發表你的觀點，口頭言論風格，直接說重點。100-200字。"""
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"錯誤: {response.status_code}"
    except Exception as e:
        return f"例外: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        result = get_response(topic)
        print(result)
    else:
        print("請提供研究主題作為參數")