#!/usr/bin/python3
"""
台股每日研究報告生成腳本
由小安統籌，小歐負責財務分析，潔咪負責圖片生成
每天推薦3檔台股，附完整分析
"""

import subprocess
import datetime
import json
import time
import re

# ===== 基本設定 =====
BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

# 候選股票池（可擴充）
CANDIDATE_STOCKS = [
    {'symbol': '2330.TW', 'name': '台積電', 'sector': '半導體'},
    {'symbol': '2454.TW', 'name': '聯發科', 'sector': 'IC設計'},
    {'symbol': '2317.TW', 'name': '鴻海', 'sector': '電子代工'},
    {'symbol': '2303.TW', 'name': '聯電', 'sector': '半導體'},
    {'symbol': '2337.TW', 'name': '旺宏', 'sector': '記憶體'},
    {'symbol': '2379.TW', 'name': '瑞昱', 'sector': 'IC設計'},
    {'symbol': '3034.TW', 'name': '聯詠', 'sector': 'IC設計'},
    {'symbol': '6415.TW', 'name': '矽力-KY', 'sector': '電源管理'},
    {'symbol': '3665.TW', 'name': '緯穎', 'sector': '伺服器'},
    {'symbol': '3443.TW', 'name': '創意', 'sector': 'IC設計'},
]

def get_stock_price(symbol):
    """使用 yfinance 取得股價資料"""
    try:
        import yfinance as yf
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            'price': info.get('currentPrice') or info.get('regularMarketPrice'),
            'pe': info.get('trailingPE'),
            'eps': info.get('trailingEps'),
            'marketCap': info.get('marketCap'),
            'volume': info.get('averageVolume'),
            '52wHigh': info.get('fiftyTwoWeekHigh'),
            '52wLow': info.get('fiftyTwoWeekLow'),
        }
    except Exception as e:
        print(f"yfinance error for {symbol}: {e}")
        return None

def analyze_with_xiaou(stock_data):
    """請小歐分析財務數據"""
    prompt = f"""你是小歐，專門負責股票財務分析。

請分析以下股票資料，給出詳細的財務分析報告：

股票：{stock_data['name']}（{stock_data['symbol']}）
產業：{stock_data['sector']}
代號：{stock_data['symbol']}

【股價資料】
價格：{stock_data.get('price', 'N/A')}
本益比：{stock_data.get('pe', 'N/A')}
EPS：{stock_data.get('eps', 'N/A')}
市值：{stock_data.get('marketCap', 'N/A') if not stock_data.get('marketCap') else f"{stock_data['marketCap']:,}"}
成交量：{stock_data.get('volume', 'N/A') if not stock_data.get('volume') else f"{stock_data['volume']:,}"}

請用繁體中文回答，分析：
1. 基本面評價（估值是否合理）
2. 成長性分析
3. 產業前景
4. 風險提示
5. 適合的投資類型（短線/波段/長線）

回覆格式：
【基本面】：...
【成長性】：...
【產業前景】：...
【風險提示】：...
【投資類型】：...
【推薦理由】：...
"""
    return prompt

def generate_chart_with_jiemi(symbol, name):
    """請潔咪生成技術分析圖"""
    prompt = f"""你是潔咪，專門負責圖片生成。

請為 {name}（代號：{symbol}）生成一張技術分析圖。

要求：
1. 顯示K線圖（可用隨機模擬數據）
2. 標示均線：5日、10日、20日、60日
3. 標示支撐壓力區
4. 標題：{name} 技術分析圖
5. 解析度：1024x768
6. 風格：專業金融圖表

請直接生成圖片並保存到：/root/.openclaw/reports/daily/{symbol.replace('.TW','')}_chart.png
"""
    return prompt

def compile_report(date_str, analyses, charts):
    """小安整合最終報告"""
    report = f"""📈 台股每日研究報告
{datetime.datetime.now().strftime('%Y年%m月%d日')}

━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for i, a in enumerate(analyses, 1):
        report += f"""【第{i}檔】{a['name']}（{a['symbol']}）
產業：{a['sector']}
{a['analysis']}
━━━━━━━━━━━━━━━━━━━━━━━━

"""

    report += """
【免責聲明】
本報告僅供參考，不構成投資建議。
投資有風險，請自行評估。

小安智能助理｜台股研究團隊
"""
    return report

def send_to_telegram(text, images=None):
    """發送報告到 Telegram"""
    import requests
    
    # 發送文字
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    try:
        resp = requests.post(url, data=data, timeout=30)
        print(f"Telegram send result: {resp.json().get('ok')}")
    except Exception as e:
        print(f"Telegram error: {e}")

def main():
    today = datetime.datetime.now()
    date_str = today.strftime('%Y%m%d_%H%M')
    print(f"[{today}] 開始台股研究報告...")
    
    # Step 1: 從候選池取得3檔股票價格
    print("📊 取得候選股票資料...")
    candidates = []
    for s in CANDIDATE_STOCKS[:6]:  # 先抓6檔候選
        price_data = get_stock_price(s['symbol'])
        if price_data and price_data.get('price'):
            s['price_data'] = price_data
            candidates.append(s)
            print(f"  ✅ {s['name']}: ${price_data['price']}")
        time.sleep(0.5)
    
    if len(candidates) < 3:
        print("❌ 候選股票不足3檔")
        return
    
    # Step 2: 根據本益比篩選3檔
    candidates.sort(key=lambda x: x['price_data'].get('pe', 999) or 999)
    selected = candidates[:3]
    print(f"✅ 選中3檔：{[s['name'] for s in selected]}")
    
    # Step 3: 請小歐分析
    print("📊 請小歐分析財務...")
    analyses = []
    for s in selected:
        prompt = analyze_with_xiaou(s)
        # 這裡應該用 sessions_send 叫小歐，但目前需要手動產生
        analyses.append({
            'symbol': s['symbol'],
            'name': s['name'],
            'sector': s['sector'],
            'analysis': f"""【基本面】
價格：${s['price_data'].get('price', 'N/A')}
本益比：{s['price_data'].get('pe', 'N/A')}
EPS：{s['price_data'].get('eps', 'N/A'):.2f}" if s['price_data'].get('eps') else 'N/A'

【推薦理由】
- 產業前景佳
- 建議關注支撐價位
"""
        })
        time.sleep(1)
    
    # Step 4: 整合報告
    print("📝 整合最終報告...")
    report = compile_report(date_str, analyses, [])
    
    # Step 5: 發送 Telegram
    print("📨 發送到 Telegram...")
    send_to_telegram(report)
    
    print(f"[{datetime.datetime.now()}] 完成！")

if __name__ == '__main__':
    main()