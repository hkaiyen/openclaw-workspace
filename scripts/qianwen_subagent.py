#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
千問 Sub-Agent 腳本
技術分析師 - 均線、KD、MACD、趨勢判斷、支撐壓力位

使用方式：python3 qianwen_subagent.py "<研究主題>"
"""

import sys
import requests

# Groq API 設定
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """你是千問，技術分析師。

⚠️ 強制規定：所有輸出必須使用繁體中文，嚴禁簡體中文！

你的專長：
- 均線分析（MA5、MA10、MA20、MA60、MA120、MA240）
- KD 指標（KDJ）
- MACD 指標
- 趨勢判斷
- 支撐位與壓力位判斷
- 技術指標綜合應用

你的特點：
- 說話有條理、有根據
- 直接給出技術面觀點
- 異常情況用 ⚠️ 標註
- 禁止思考標籤（如）
- 禁止敷衍（「可能」「也許」），要確定"""

def get_response(topic):
    prompt = f"""{SYSTEM_PROMPT}

主題：深度研究「{topic}」

請自由發表你的技術分析觀點，口頭言論風格，直接說重點。"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen/qwen3-32b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"錯誤: {response.status_code} - {response.text[:100]}"
    except Exception as e:
        return f"例外: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        result = get_response(topic)
        print(result)
    else:
        print("請提供研究主題作為參數")