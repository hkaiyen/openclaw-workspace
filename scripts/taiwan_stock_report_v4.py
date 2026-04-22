#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
台股每日研究報告 v4（川寶投顧專用）
恢复原始版本：聯詠、鴻海、瑞昱
"""

import requests
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime

# ========== 設定 ==========
BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

# ========== 股票資料（根據 Word 檔案還原）==========
STOCKS = [
    {
        'symbol': '3034.TW',
        'name': '聯詠',
        'price': 260,
        'pe': 16.1,
        'eps': 26.84,
        'roe': '24.1',
        'profit_margin': '24.4',
        'operating_margin': '19.1',
        'dividend_yield': '6.74',
        'debt_ratio': '32.5',
        'current_ratio': '2.1',
        'roa': '15以上',
        '目標價': '$483 ~ $590（價值修復空間12-36%）',
        '推薦理由': 'P/E 16.1為IC設計族群最低，殖利率6.74%提供下檔保護，基本面無明顯瑕疵，適合價值型投資人與追求配息的防禦性配置。',
        '持有期間': '波段至長線（3-6個月以上）',
        '基本面評價': '體質穩健，評價偏低，具價值重估空間。',
        '財務品質': '毛利率24.4%、營益率19.1%在IC設計中屬中上水準，顯示產品組合具議價能力。ROE 24.1%優於平均，ROA約15%以上，負債比32.5%健康，流動比2.1顯示短期償債無虞。唯一需注意為存貨周轉，因面板景氣循環天然具波動性。',
        '成長動能': '聯詠為面板驅動IC全球龍頭，受惠AMOLED滲透率持續提升。三星、LG、京東方為主要客戶，營收貢獻穩定。2024年OLED DDI需求年增約20%，聯詠技術領先對手至少1-2年。新品車用顯示IC已進入認證階段，2025年有望放量。',
        '產業前景': '大尺寸TV面板報價已落底，監視器與筆電需求溫和復甦。Mini LED背光滲透為長期驅動。車用面板成新增長點，估計車用面板市場年複合成長達8%以上，聯詠擁有認證優勢。',
        '風險評估': '面板景氣循環最直接影響；中國廠商積極布局OLED DDI；終端消費電子需求放緩可能影響備貨意願；新台幣升值侵蝕毛利率。',
    },
    {
        'symbol': '2317.TW',
        'name': '鴻海',
        'price': 221,
        'pe': 16.5,
        'eps': 13.40,
        'roe': '11.3',
        'profit_margin': '6.8',
        'operating_margin': '3.2',
        'dividend_yield': '4.2',
        'debt_ratio': '45.2',
        'current_ratio': '1.5',
        'roa': '約8%',
        '目標價': '$188 ~ $241（向上空間約9%）',
        '推薦理由': 'AI伺服器題材實質發酵，營收規模亞洲頂尖，股息4.2%提供支撐，適合尋求穩健配息且參與AI行情的投資人。',
        '持有期間': '波段至長線（6-12個月）',
        '基本面評價': 'EPS 13.40對應P/E 16.5評價合理，ROE 11.3%普通但穩定。',
        '財務品質': '毛利率6.8%、營益率3.2%屬電子代工正常水準，規模經濟掩蓋低毛利弱點。負債比45.2%屬健康水位，流動比1.5略低但尚在安全範圍。應收帳款天數約75天，現金轉換循環穩定。',
        '成長動能': 'AI伺服器需求爆發，鴻海為輝達H系列主力代工廠，GB200供應鏈中地位關鍵。蘋果iPhone 17組裝訂單預計2025年下半年放量。電動車代工業務逐步貢獻營收。雲端服務商需求掩蓋消費電子放緩。',
        '產業前景': '全球AI基礎建設投資爆發，資料中心資本支出2024-2026年複合成長率預估15-20%。鴻海作為全球最大EMS廠，技術、產能、供應鏈管理均無可取代。AI伺服器ASP為傳統伺服器3-5倍，產品組合優化有助毛利率改善。',
        '風險評估': '毛利率過低易受原物料與人頭成本波動衝擊；中國產能集中，地緣政治風險加劇；客戶集中度過高（蘋果約50%）；電動車投資短期貢獻有限稀釋資源。',
    },
    {
        'symbol': '2379.TW',
        'name': '瑞昱',
        'price': 568,
        'pe': 20.2,
        'eps': 28.05,
        'roe': '28.1',
        'profit_margin': '47.2',
        'operating_margin': '18.5',
        'dividend_yield': '4.63',
        'debt_ratio': '28.1',
        'current_ratio': '2.8',
        'roa': '超過20%',
        '目標價': '$617 ~ $701（價值修復空間9-24%）',
        '推薦理由': '財務品質頂尖，成長藍籌明確，殖利率4.63%兼顧收益，適合追求穩健成長與合理價位的投資人。',
        '持有期間': '長線（6個月以上）',
        '基本面評價': 'ROE 28.1%、毛利率47.2%為IC設計翹楚，財務體質頂級。',
        '財務品質': '毛利率47.2%傲視同業，營益率18.5%顯示高附加價值產品組合。ROE 28.1%在IC設計中僅次龍頭，ROA估計超過20%，體現高效經營。負債比28.1%為三檔最低，流動比2.8顯示現金部位充裕。瑞昱歷年配息率達70%以上，股利政策穩定。',
        '成長動能': 'Wi-Fi 6/7升級為長期驅動力，全球路由器、筆電、智慧家居持續滲透。瑞昱為Wi-Fi晶片主要供應商，2024年Wi-Fi 6出貨滲透率已過50%，2025年Wi-Fi 6E/7升級潮到來。車用乙太網已通過多家Tier 1認證，2025年量產有望。藍芽音訊晶片切入品牌客戶，供應鏈地位穩固。',
        '產業前景': '全球網通基礎建設持續擴張，邊緣運算與AIoT應用爆發，所有聯網設備均需要Wi-Fi/藍芽晶片。瑞昱在亞太網通IC市場佔有率領先，技術與性價比兼具。邊緣AI導入終端裝置，新規格需求將帶動產品升級。',
        '風險評估': '中國競爭對手積極布局低價Wi-Fi市場；美中貿易摩擦可能影響中國客戶；半導體庫存調整影響營收波動；技術迭代要求持續研發投資。',
    },
]

# ========== 生成 Word 報告 ==========
def generate_report():
    doc = Document()
    
    # 頁面設定
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)
    
    # ========== 封面 ==========
    title = doc.add_heading('📈 台股每日研究報告', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.size = Pt(28)
    title.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = subtitle.add_run('川寶投顧每天研究三檔股票')
    sr.font.size = Pt(14)
    sr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    sr.font.italic = True
    
    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dr = date_para.add_run(datetime.datetime.now().strftime('%Y年%m月%d日'))
    dr.font.size = Pt(16)
    
    doc.add_paragraph()
    
    # ========== 研究摘要 ==========
    doc.add_heading('📋 研究摘要', level=1).runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    
    summary = """川寶投顧研究3檔台股：

1. 【聯詠（3034）】價值型首選
   - P/E 16.1為IC設計最低，殖利率6.74%
   - 目標價：$483 ~ $590（潛在上漲12-36%）
   - 適合：追求配息與價值投資

2. 【鴻海（2317）】AI概念穩健股
   - GB200供應鏈核心，股息4.2%
   - 目標價：$188 ~ $241（潛在上漲9%）
   - 適合：穩健型投資人

3. 【瑞昱（2379）】成長型藍籌
   - ROE 28.1%、毛利率47.2%，財務頂尖
   - 目標價：$617 ~ $701（潛在上漲9-24%）
   - 適合：追求成長的長線投資人
"""
    doc.add_paragraph(summary)
    
    doc.add_page_break()
    
    # ========== 各檔報告 ==========
    for stock in STOCKS:
        # 標題
        h1 = doc.add_heading(f"【{stock['name']}（{stock['symbol']}）】", level=1)
        h1.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        
        # 基本面資料
        doc.add_heading('📊 基本面資料', level=2).runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        
        table = doc.add_table(rows=7, cols=2)
        table.style = 'Table Grid'
        
        basic_data = [
            ('股價', f"${stock['price']}"),
            ('本益比（P/E）', f"{stock['pe']}"),
            ('每股盈餘（EPS）', f"${stock['eps']}"),
            ('ROE', f"{stock['roe']}%"),
            ('毛利率', f"{stock['profit_margin']}%"),
            ('營益率', f"{stock['operating_margin']}%"),
            ('殖利率', f"{stock['dividend_yield']}%"),
        ]
        
        for i, (label, value) in enumerate(basic_data):
            table.rows[i].cells[0].text = label
            table.rows[i].cells[1].text = str(value)
            for p in table.rows[i].cells[0].paragraphs:
                for r in p.runs:
                    r.bold = True
        
        doc.add_paragraph()
        
        # 深度分析
        doc.add_heading('📈 深度分析', level=2).runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        
        analysis_items = [
            ('基本面評價', stock['基本面評價']),
            ('財務品質', stock['財務品質']),
            ('成長動能', stock['成長動能']),
            ('產業前景', stock['產業前景']),
            ('風險評估', stock['風險評估']),
        ]
        
        for category, content in analysis_items:
            p = doc.add_paragraph()
            p.add_run(f'{category}：').bold = True
            p.add_run(content)
            p.paragraph_format.space_after = Pt(6)
        
        doc.add_paragraph()
        
        # 投資推薦
        doc.add_heading('🎯 投資推薦', level=2).runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        
        recommend_items = [
            ('目標價', stock['目標價']),
            ('推薦理由', stock['推薦理由']),
            ('持有期間', stock['持有期間']),
        ]
        
        for category, content in recommend_items:
            p = doc.add_paragraph()
            p.add_run(f'{category}：').bold = True
            p.add_run(content)
            p.paragraph_format.space_after = Pt(6)
        
        doc.add_page_break()
    
    # ========== 最後一頁：重要聲明 ==========
    disc_title = doc.add_heading('📋 重要聲明', level=1)
    disc_title.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    
    disc_text = doc.add_paragraph()
    dt = disc_text.add_run('本報告僅供參考，不構成投資建議。投資有風險，請自行評估。｜川寶投顧｜台股研究團隊')
    dt.font.size = Pt(11)
    dt.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    dt.font.italic = True
    
    doc.add_paragraph()
    
    model_info = doc.add_paragraph()
    mr = model_info.add_run('使用模型：MiniMax M2.7 · Groq GPT-OSS-120B · Gemini 3 Pro')
    mr.font.size = Pt(10)
    mr.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    mr.font.italic = True
    
    return doc

# ========== 發送 Telegram ==========
def send_telegram(doc):
    output_path = f"/root/.openclaw/reports/daily/台股研究報告_v4_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.docx"
    doc.save(output_path)
    print(f"✅ 已保存: {output_path}")
    
    with open(output_path, 'rb') as f:
        files = {'document': f}
        data = {
            'chat_id': CHAT_ID,
            'caption': f"📈 川寶投顧每日研究報告 {datetime.datetime.now().strftime('%Y.%m.%d')}"
        }
        r = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument', data=data, files=files, timeout=60)
        print(f"Telegram: {'✅' if r.json().get('ok') else '❌'}")
    
    return output_path

# ========== 主程式 ==========
def main():
    print("\n" + "=" * 60)
    print("🚀 台股每日研究報告 v4 - 川寶投顧")
    print("=" * 60)
    print(f"時間: {datetime.datetime.now()}")
    print("股票: 聯詠(3034) · 鴻海(2317) · 瑞昱(2379)")
    
    doc = generate_report()
    output = send_telegram(doc)
    
    print("\n✅ 完成！")
    print(f"報告: {output}")

if __name__ == '__main__':
    main()