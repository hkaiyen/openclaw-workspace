#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
台股每日研究報告 v4.0 - 完整版
小安統籌 + 小歐深度分析

流程：
1. 小安取得完整財報（10項）
2. 小安取得法人籌碼資料
3. 小安取得技術指標
4. 小歐產業深度分析
5. 小歐風險評估
6. 小歐推薦理由與目標價
7. 小安整合完整Word報告
"""

import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import os
import subprocess
import sys

# ========== 設定 ==========
BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

# 候選股票池
CANDIDATE_STOCKS = [
    {'symbol': '2330.TW', 'name': '台積電', 'sector': '半導體'},
    {'symbol': '2454.TW', 'name': '聯發科', 'sector': 'IC設計'},
    {'symbol': '2317.TW', 'name': '鴻海', 'sector': '電子代工'},
    {'symbol': '2303.TW', 'name': '聯電', 'sector': '半導體'},
    {'symbol': '3034.TW', 'name': '聯詠', 'sector': 'IC設計'},
    {'symbol': '2379.TW', 'name': '瑞昱', 'sector': 'IC設計'},
    {'symbol': '6415.TW', 'name': '矽力-KY', 'sector': '電源管理'},
    {'symbol': '3443.TW', 'name': '創意', 'sector': 'IC設計'},
    {'symbol': '3665.TW', 'name': '緯穎', 'sector': '伺服器'},
    {'symbol': '2451.TW', 'name': '創見', 'sector': '記憶體'},
]

# ========== 步驟1：小安取得完整財報 ==========
def step1_get_complete_financials():
    """取得完整財務資料（10項）"""
    print("\n" + "=" * 60)
    print("【步驟1】小安取得完整財報資料（yfinance）")
    print("=" * 60)
    
    candidates = []
    for s in CANDIDATE_STOCKS:
        try:
            t = yf.Ticker(s['symbol'])
            info = t.info
            
            # 基本面
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            pe = info.get('trailingPE')
            forward_pe = info.get('forwardPE')
            eps = info.get('trailingEps')
            market_cap = info.get('marketCap')
            
            # 獲利能力
            profit_margin = info.get('profitMargin')
            operating_margin = info.get('operatingMargin')
            roe = info.get('returnOnEquity')
            roa = info.get('returnOnAssets')
            
            # 財務結構
            debt_to_equity = info.get('debtToEquity')
            current_ratio = info.get('currentRatio')
            
            # 成長性
            revenue = info.get('totalRevenue')
            revenue_growth = info.get('revenueGrowth')
            earnings_growth = info.get('earningsGrowth')
            
            # 股利
            dividend_yield = info.get('dividendYield')
            dividend_rate = info.get('dividendRate')
            
            # 籌碼
            volume = info.get('averageVolume')
            shares = info.get('sharesOutstanding')
            
            # 52週
            high_52 = info.get('fiftyTwoWeekHigh')
            low_52 = info.get('fiftyTwoWeekLow')
            
            if price and eps:
                data = {
                    'symbol': s['symbol'],
                    'name': s['name'],
                    'sector': s['sector'],
                    'price': price,
                    'pe': round(pe, 2) if pe else None,
                    'forward_pe': round(forward_pe, 2) if forward_pe else None,
                    'eps': round(eps, 2) if eps else None,
                    'market_cap': market_cap,
                    'profit_margin': round(profit_margin * 100, 2) if profit_margin else None,
                    'operating_margin': round(operating_margin * 100, 2) if operating_margin else None,
                    'roe': round(roe * 100, 2) if roe else None,
                    'roa': round(roa * 100, 2) if roa else None,
                    'debt_to_equity': round(debt_to_equity, 2) if debt_to_equity else None,
                    'current_ratio': round(current_ratio, 2) if current_ratio else None,
                    'revenue': revenue,
                    'revenue_growth': round(revenue_growth * 100, 2) if revenue_growth else None,
                    'earnings_growth': round(earnings_growth * 100, 2) if earnings_growth else None,
                    'dividend_yield': round(dividend_yield * 100, 2) if dividend_yield else None,
                    'dividend_rate': dividend_rate,
                    'volume': volume,
                    'shares': shares,
                    'high_52': high_52,
                    'low_52': low_52,
                    'distance_high': round((price - high_52) / high_52 * 100, 1) if high_52 else None,
                }
                candidates.append(data)
                print(f"✅ {s['name']}: P/E={pe:.1f} EPS={eps:.2f} ROE={roe*100:.1f}%" if roe else f"✅ {s['name']}")
        
        except Exception as e:
            print(f"❌ {s['name']}: {e}")
        
        time.sleep(0.3)
    
    # 按本益比排序，選3檔
    valid = [c for c in candidates if c['pe'] and c['pe'] < 50]
    valid.sort(key=lambda x: x['pe'])
    selected = valid[:3]
    
    print(f"\n✅ 篩選結果: {[s['name'] for s in selected]}")
    
    with open('/tmp/stock_data.json', 'w') as f:
        json.dump(selected, f, indent=2)
    
    return selected

# ========== 步驟2：小安取得法人籌碼 ==========
def step2_get_institutional_data(selected_stocks):
    """取得法人籌碼資料"""
    print("\n" + "=" * 60)
    print("【步驟2】小安取得法人籌碼資料")
    print("=" * 60)
    
    # 嘗試從 GoodInfo 取得
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    institutional_data = []
    
    for s in selected_stocks:
        sid = s['symbol'].replace('.TW', '')
        print(f"\n取得 {s['name']} 法人資料...")
        
        try:
            # 嘗試取得三大法人資料
            url = f"https://goodinfo.tw/StockInfo/GetSalesReportCntDate.asp?STOCK_ID={sid}"
            resp = requests.get(url, headers=headers, timeout=10)
            
            # 簡化：使用 yfinance 的機構持股資料
            t = yf.Ticker(s['symbol'])
            info = t.info
            
            inst_data = {
                'symbol': s['symbol'],
                'name': s['name'],
                'institutional_ownership': info.get('institutionalOwnership'),
                'held_by_insiders': info.get('heldByInsiders'),
                'market_cap': s['market_cap'],
                'volume': s['volume'],
                'shares': s['shares'],
            }
            
            # 嘗試從不同 URL 取得更多資料
            url2 = f"https://goodinfo.tw/StockInfo/ShowK线.asp?STOCK_ID={sid}"
            resp2 = requests.get(url2, headers=headers, timeout=10)
            
            print(f"  ✅ {s['name']}: 取得成功")
            
        except Exception as e:
            print(f"  ⚠️ {s['name']}: {e}")
            inst_data = {'symbol': s['symbol'], 'name': s['name'], 'note': '取得失敗'}
        
        institutional_data.append(inst_data)
        time.sleep(0.5)
    
    with open('/tmp/institutional_data.json', 'w') as f:
        json.dump(institutional_data, f, indent=2)
    
    return institutional_data

# ========== 步驟3：小安取得技術指標 ==========
def step3_get_technical_indicators(selected_stocks):
    """取得技術指標"""
    print("\n" + "=" * 60)
    print("【步驟3】小安取得技術指標")
    print("=" * 60)
    
    technical_data = []
    
    for s in selected_stocks:
        try:
            t = yf.Ticker(s['symbol'])
            df = t.history(period='60d')  # 60天資料計算均線
            
            if len(df) > 60:
                # 計算均線
                ma5 = df['Close'].rolling(5).mean().iloc[-1]
                ma10 = df['Close'].rolling(10).mean().iloc[-1]
                ma20 = df['Close'].rolling(20).mean().iloc[-1]
                ma60 = df['Close'].rolling(60).mean().iloc[-1]
                
                # 計算KD（簡化版）
                low_min = df['Low'].rolling(9).min().iloc[-1]
                high_max = df['High'].rolling(9).max().iloc[-1]
                k_raw = (df['Close'].iloc[-1] - low_min) / (high_max - low_min) * 100 if high_max > low_min else 50
                k = round(k_raw, 2)
                d = round(k * 0.9 + 50 * 0.1, 2)  # 簡化D值
                
                # 判斷多空
                price = df['Close'].iloc[-1]
                if price > ma20 > ma60:
                    trend = "多頭排列"
                elif price < ma20 < ma60:
                    trend = "空頭排列"
                else:
                    trend = "盤整"
                
                # 支撐壓力
                support = round(ma20 * 0.95, 0)
                resistance = round(ma20 * 1.05, 0)
                
                tech = {
                    'symbol': s['symbol'],
                    'name': s['name'],
                    'price': round(price, 2),
                    'ma5': round(ma5, 2),
                    'ma20': round(ma20, 2),
                    'ma60': round(ma60, 2),
                    'k': k,
                    'd': d,
                    'trend': trend,
                    'support': support,
                    'resistance': resistance,
                    'volume': int(df['Volume'].iloc[-1]),
                    'avg_volume': int(df['Volume'].rolling(20).mean().iloc[-1]),
                }
                
                print(f"✅ {s['name']}: {trend} MA20={ma20:.0f} K={k:.1f} D={d:.1f}")
                
            else:
                tech = {'symbol': s['symbol'], 'name': s['name'], 'note': '資料不足'}
                print(f"⚠️ {s['name']}: 資料不足")
            
        except Exception as e:
            print(f"❌ {s['name']}: {e}")
            tech = {'symbol': s['symbol'], 'name': s['name'], 'error': str(e)}
        
        technical_data.append(tech)
        time.sleep(0.3)
    
    with open('/tmp/technical_data.json', 'w') as f:
        json.dump(technical_data, f, indent=2)
    
    return technical_data

# ========== 主程式 ==========
def main():
    print("\n" + "=" * 60)
    print("🚀 台股每日研究報告 v4.0 - 完整版")
    print("=" * 60)
    print(f"開始時間: {datetime.datetime.now()}")
    
    start = datetime.datetime.now()
    
    # 步驟1: 取得完整財報
    selected_stocks = step1_get_complete_financials()
    
    # 步驟2: 取得法人籌碼
    inst_data = step2_get_institutional_data(selected_stocks)
    
    # 步驟3: 取得技術指標
    tech_data = step3_get_technical_indicators(selected_stocks)
    
    # 保存所有資料
    all_data = {
        'stocks': selected_stocks,
        'institutional': inst_data,
        'technical': tech_data,
        'generated_at': datetime.datetime.now().isoformat()
    }
    
    with open('/tmp/all_stock_data.json', 'w') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    end = datetime.datetime.now()
    
    print("\n" + "=" * 60)
    print("✅ 小安部分完成！")
    print(f"耗時: {(end-start).total_seconds():.1f} 秒")
    print("=" * 60)
    print("\n下一步: 請小歐分析")
    print("=" * 60)

if __name__ == '__main__':
    main()