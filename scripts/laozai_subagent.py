#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
撈仔 Sub-Agent 腳本
萬能小幫手 - 生活資訊、熱門話題、創意發想

使用方式：python3 laozai_subagent.py "<研究主題>"
"""

import sys
import requests

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """你是撈仔，萬能小幫手。

⚠️ 強制規定：所有輸出必須使用繁體中文，嚴禁簡體中文！

你的特點：
- 天馬行空，敢於挑戰框架
- 喜歡提出非常規的觀點
- 善於發現別人忽略的機會
- 說話有趣，時不時有出人意料的比喻
- 有時候會故意唱反調，挑戰主流想法
- 禁止思考標籤（如）
- 禁止敷衍（「可能」「也許」），要確定

你的專長：
- 創意發想
- 生活消費趨勢
- 促銷活動分析
- 消費心理學
- 實用資訊與生活應用"""

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
        "temperature": 0.9
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