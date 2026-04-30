#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小歐 Sub-Agent 腳本
國際財經專家 - 創意觀點、風險提示、財報除錯

使用方式：python3 xiaoou_subagent.py "<研究主題>"
"""

import sys
import requests

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """你是小歐，國際財經專家。

⚠️ 強制規定：所有輸出必須使用繁體中文，嚴禁簡體中文！

你的特點：
- 回覆簡潔有力，拒絕冗長廢話
- 使用條列式或表格呈現數據
- 數據結果要標註單位與時間
- 異常情況用 ⚠️ 標註
- 禁止思考標籤（如）
- 禁止敷衍（「可能」「也許」），要確定

你的專長：
- 財經分析
- 風險提示
- 創意觀點
- 國際趨勢"""

def get_response(topic):
    prompt = f"""{SYSTEM_PROMPT}

主題：深度研究「{topic}」

請自由發表你的觀點，口頭言論風格，直接說重點。100-200字。"""
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-oss-120b",
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