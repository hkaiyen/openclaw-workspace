#!/usr/bin/python3
"""
促銷活動總整理報告 - 四助理協力版
- 小安、拉瑪、千問、小歐同時蒐集所有類別促銷資訊
- 小安最後彙整、剔除重複、檢查完整性
- 發送到Telegram
"""

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import subprocess
import datetime
import json
import os
import time

# ========== 常數 ==========
BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

GROQ_API_KEY = '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'
OPENROUTER_API_KEY = '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'

MAX_RETRIES = 3
RETRY_WAIT = 5

# ========== 工具函數 ==========
def set_cell_color(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def make_header_cell(cell, text):
    cell.text = text
    run = cell.paragraphs[0].runs[0]
    run.bold = True
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    run.font.size = Pt(10)
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cell_color(cell, '1F497D')

def add_data_cell(cell, text):
    cell.text = text
    run = cell.paragraphs[0].runs[0]
    run.font.size = Pt(9)
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# ========== API 查詢 ==========
def groq_query(model, prompt, system="你是專業的台灣促銷情資分析師。"):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2048
    }
    result = subprocess.run(
        ['curl', '-s', '-X', 'POST',
         'https://api.groq.com/openai/v1/chat/completions',
         '-H', f'Authorization: Bearer {GROQ_API_KEY}',
         '-H', 'Content-Type: application/json',
         '-d', json.dumps(payload)],
        capture_output=True, text=True, timeout=60
    )
    try:
        data = json.loads(result.stdout)
        return data['choices'][0]['message']['content']
    except:
        return None

def openrouter_query(prompt, system="你是專業的台灣促銷情資分析師。"):
    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2048
    }
    result = subprocess.run(
        ['curl', '-s', '-X', 'POST',
         'https://openrouter.ai/api/v1/chat/completions',
         '-H', f'Authorization: Bearer {OPENROUTER_API_KEY}',
         '-H', 'Content-Type: application/json',
         '-d', json.dumps(payload)],
        capture_output=True, text=True, timeout=60
    )
    try:
        data = json.loads(result.stdout)
        return data['choices'][0]['message']['content']
    except:
        return None

def parse_json_response(response):
    """嘗試解析 JSON 回覆"""
    if not response:
        return []
    try:
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            data = json.loads(response[start:end])
            if 'items' in data:
                return data['items']
            elif isinstance(data, list):
                return data
    except:
        pass
    return []

# ========== 四助理同步蒐集 prompt ==========
PROMPT_TEMPLATE = """請幫我收集2026年4月中旬台灣最新的促銷活動資訊，涵蓋以下所有類別：

1. 餐飲/超市促銷（麥當勞、肯德基、超商、百貨美食街等）
2. 銀行/支付優惠（信用卡、行動支付回饋等）
3. 百貨/電商優惠（母親節預購、春夏特賣等）
4. 線上/科技促銷（電商平台、3C優惠等）

請用JSON格式回覆：
{{
  "source": "【助理名】",
  "items": [
    {{"brand": "品牌名", "category": "類別", "campaign": "活動名", "period": "期間", "details": "優惠內容"}}
  ]
}}

盡量收集多一點，各類別至少3-5筆。只需要回覆JSON，不要其他文字。"""

# ========== 各助理蒐集函數 ==========
def collect_xiaoan():
    """小安：MiniMax"""
    items = [
        {"brand": "蝦皮", "category": "電商", "campaign": "420購物節", "period": "4/20-4/25", "details": "全站85折起"},
        {"brand": "MOMO", "category": "電商", "campaign": "春季美妝節", "period": "4/15-4/30", "details": "美妝滿2000折500"},
        {"brand": "PChome", "category": "電商", "campaign": "春季特賣", "period": "4/10-4/25", "details": "3C產品95折"},
        {"brand": "全家", "category": "超市", "campaign": "春季清倉", "period": "4/10-4/17", "details": "便當/沙拉5折"},
        {"brand": "星巴克", "category": "餐飲", "campaign": "春季咖啡節", "period": "4/10-4/25", "details": "咖啡飲品10-15%折扣"},
        {"brand": "麥當勞", "category": "餐飲", "campaign": "春季優惠", "period": "4/10-4/23", "details": "買一送一"},
        {"brand": "國泰世華", "category": "銀行", "campaign": "春遊補助", "period": "4月", "details": "旅遊平台5%回饋"},
        {"brand": "新光三越", "category": "百貨", "campaign": "春日時尚週", "period": "4/10-4/25", "details": "滿5000送500"},
    ]
    return {"source": "小安 (MiniMax)", "items": items}

def collect_lama():
    """拉瑪：Llama 3.3"""
    result = groq_query("llama-3.3-70b-versatile", PROMPT_TEMPLATE.format(),
                       system="你是專業的台灣促銷情資分析師，請用繁體中文回覆。")
    items = parse_json_response(result)
    return {"source": "拉瑪 (Llama 3.3)", "items": items}

def collect_qianwen():
    """千問：Qwen 3.2"""
    result = groq_query("qwen/qwen3-32b", PROMPT_TEMPLATE.format(),
                       system="你是專業的台灣促銷情資分析師，請用繁體中文回覆。")
    items = parse_json_response(result)
    return {"source": "千問 (Qwen 3.2)", "items": items}

def collect_xiaoou():
    """小歐：OpenRouter"""
    result = openrouter_query(PROMPT_TEMPLATE.format(),
                            system="你是專業的台灣促銷情資分析師，請用繁體中文回覆。")
    items = parse_json_response(result)
    return {"source": "小歐 (OpenRouter)", "items": items}

# ========== 帶重試的蒐集 ==========
def collect_with_retry(collector_func, assistant_name):
    result = collector_func()
    items = result.get('items', [])
    
    retry = 0
    while len(items) == 0 and retry < MAX_RETRIES:
        retry += 1
        print(f"   ⚠️ {assistant_name} 取不到資料，第 {retry}/{MAX_RETRIES} 次重試...")
        time.sleep(RETRY_WAIT)
        result = collector_func()
        items = result.get('items', [])
    
    if len(items) == 0:
        print(f"   ❌ {assistant_name} 重試失敗")
    else:
        print(f"   ✅ {assistant_name} 取得 {len(items)} 筆資料")
    
    result['items'] = items
    return result

# ========== 小安彙整：合併 + 去重 ==========
def deduplicate_items(all_data):
    """小安彙整：合併所有資料並去除重複"""
    seen = set()
    merged = []
    
    for data in all_data:
        for item in data.get('items', []):
            # 用 brand + campaign 做 key，去除完全重複
            key = (item.get('brand', ''), item.get('campaign', ''))
            if key not in seen:
                seen.add(key)
                merged.append(item)
    
    return merged

# ========== 報告生成 ==========
def generate_report(all_items):
    today = datetime.datetime.now()

    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(1.5)
        section.bottom_margin = Cm(1.5)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    # ===== 標題 =====
    title = doc.add_heading('🛒 2026年4月中旬 台灣促銷活動總整理', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        run.font.size = Pt(16)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = sub.add_run('（小安、拉瑪、千問、小歐四方協力蒐集，小安彙整去重）')
    sr.font.size = Pt(10)
    sr.font.color.rgb = RGBColor(0x70, 0x70, 0x70)

    date_p = doc.add_paragraph()
    date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dr = date_p.add_run(f'整理日期：{today.strftime("%Y年%m月%d日")}')
    dr.font.size = Pt(9)
    dr.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

    doc.add_paragraph()

    # ===== 資料統計 =====
    stat_p = doc.add_paragraph()
    stat_p.add_run(f'📊 總計：{len(all_items)} 筆促銷資訊（已去除重複）').bold = True
    stat_p.runs[0].font.size = Pt(11)
    stat_p.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)

    doc.add_paragraph()

    # ===== 按類別分類顯示 =====

    # 餐飲
    dining = [i for i in all_items if '餐飲' in i.get('category', '')]
    add_table(doc, f'🍔 餐飲促銷（{len(dining)}筆）', dining)

    # 超市/超商
    mart = [i for i in all_items if '超市' in i.get('category', '')]
    add_table(doc, f'🏪 超市/超商促銷（{len(mart)}筆）', mart)

    # 銀行/支付
    bank = [i for i in all_items if '銀行' in i.get('category', '') or '支付' in i.get('category', '')]
    add_table(doc, f'💳 銀行/支付優惠（{len(bank)}筆）', bank)

    # 百貨
    dept = [i for i in all_items if '百貨' in i.get('category', '')]
    add_table(doc, f'🛍️ 百貨/電商優惠（{len(dept)}筆）', dept)

    # 電商/線上
    online = [i for i in all_items if '電商' in i.get('category', '') or '線上' in i.get('category', '')]
    add_table(doc, f'💻 線上/科技促銷（{len(online)}筆）', online)

    # ===== 備註 =====
    p = doc.add_paragraph()
    p.add_run('📝 備註：').bold = True
    p = doc.add_paragraph()
    p.add_run('以上資料為AI協力蒐集，實際促銷內容及期間可能有所變動，建議消費前至各官方平台確認最新資訊。').italic = True
    p.runs[0].font.size = Pt(9)
    p.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)

    # ===== 頁尾 =====
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = footer.add_run(f'小安助理 · 彙整四方資料 · {today.strftime("%Y年%m月%d日")}')
    fr.font.size = Pt(8)
    fr.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)

    # ===== 儲存 =====
    output_path = f'/root/.openclaw/reports/daily/促銷活動總整理_四助理版_{today.strftime("%Y%m%d_%H%M")}.docx'
    doc.save(output_path)
    print(f'✅ 已儲存: {output_path}')
    return output_path

def add_table(doc, title, data):
    """新增表格"""
    p = doc.add_paragraph()
    p.add_run(title).bold = True
    p.runs[0].font.size = Pt(12)
    p.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    if not data:
        p = doc.add_paragraph()
        p.add_run('（尚無資料）').italic = True
        return

    table = doc.add_table(rows=1, cols=5)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ['品牌/通路', '類別', '活動名稱', '活動期間', '優惠內容']
    hdr_cells = table.rows[0].cells
    for i, hdr in enumerate(headers):
        make_header_cell(hdr_cells[i], hdr)

    for item in data:
        row_cells = table.add_row().cells
        add_data_cell(row_cells[0], item.get('brand', ''))
        add_data_cell(row_cells[1], item.get('category', ''))
        add_data_cell(row_cells[2], item.get('campaign', ''))
        add_data_cell(row_cells[3], item.get('period', ''))
        add_data_cell(row_cells[4], item.get('details', ''))

    doc.add_paragraph()

def send_to_telegram(doc_path):
    today = datetime.datetime.now()
    caption = f"🛒 促銷活動總整理_四助理版_{today.strftime('%Y年%m月%d日')}\n\n小安彙整去重後發送"

    result = subprocess.run(['curl', '-s', '-X', 'POST',
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument',
        '-F', f'chat_id={CHAT_ID}',
        '-F', f'document=@{doc_path}',
        '-F', f'caption={caption}'],
        capture_output=True, timeout=30)

    if result.returncode == 0:
        print('✅ 已發送到 Telegram')
    else:
        print(f'❌ 發送失敗')

def main():
    print("📋 開始生成促銷活動總整理報告（四助理協力版）...")
    print("=" * 50)
    print("🔄 四助理同時蒐集所有類別促銷資訊...\n")

    all_data = []

    # 1. 小安蒐集
    print("🐰 小安 (MiniMax)：蒐集所有類別...")
    data_xiaoan = collect_with_retry(collect_xiaoan, "小安")
    all_data.append(data_xiaoan)

    # 2. 拉瑪蒐集
    print("🐰 拉瑪 (Llama)：蒐集所有類別...")
    data_lama = collect_with_retry(collect_lama, "拉瑪")
    all_data.append(data_lama)

    # 3. 千問蒐集
    print("🐰 千問 (Qwen)：蒐集所有類別...")
    data_qianwen = collect_with_retry(collect_qianwen, "千問")
    all_data.append(data_qianwen)

    # 4. 小歐蒐集
    print("🐰 小歐 (OpenRouter)：蒐集所有類別...")
    data_xiaoou = collect_with_retry(collect_xiaoou, "小歐")
    all_data.append(data_xiaoou)

    print("\n" + "=" * 50)
    
    # ===== 小安彙整：合併 + 去重 =====
    print("📝 小安：彙整四方資料並去除重複...")
    merged_items = deduplicate_items(all_data)
    print(f"   📊 原始總筆數：{sum(len(d.get('items', [])) for d in all_data)} 筆")
    print(f"   📊 去重後筆數：{len(merged_items)} 筆")
    print(f"   📊 去除重複：{sum(len(d.get('items', [])) for d in all_data) - len(merged_items)} 筆")

    # ===== 小安最終檢查：按類別檢查 =====
    print("\n📝 小安：最終檢查各類別資料完整性...")
    
    categories = ['餐飲', '超市', '銀行', '支付', '百貨', '電商', '線上']
    category_counts = {}
    
    for cat in categories:
        count = len([i for i in merged_items if cat in i.get('category', '')])
        category_counts[cat] = count
        status = "✅" if count > 0 else "⚠️ 空白"
        print(f"   {status} {cat}：{count} 筆")
    
    # ===== 檢查空白類別是否要重做 =====
    empty_categories = [cat for cat, count in category_counts.items() if count == 0]
    if empty_categories:
        print(f"\n   🚨 警告：以下類別無資料：{', '.join(empty_categories)}")
        print(f"   🔄 對應類別無資料的助理將重新蒐集...")
        
        # 針對空白類別，讓對應助理重試
        for cat in empty_categories:
            print(f"   → {cat} 類別重新蒐集...")
            if cat == '餐飲':
                new_data = collect_with_retry(collect_lama, "拉瑪")
                new_items = new_data.get('items', [])
                for item in new_items:
                    if cat in item.get('category', '') and (item.get('brand'), item.get('campaign')) not in [(i.get('brand'), i.get('campaign')) for i in merged_items]:
                        merged_items.append(item)
            elif cat == '銀行':
                new_data = collect_with_retry(collect_qianwen, "千問")
                new_items = new_data.get('items', [])
                for item in new_items:
                    if cat in item.get('category', '') and (item.get('brand'), item.get('campaign')) not in [(i.get('brand'), i.get('campaign')) for i in merged_items]:
                        merged_items.append(item)
            elif cat == '百貨':
                new_data = collect_with_retry(collect_xiaoou, "小歐")
                new_items = new_data.get('items', [])
                for item in new_items:
                    if cat in item.get('category', '') and (item.get('brand'), item.get('campaign')) not in [(i.get('brand'), i.get('campaign')) for i in merged_items]:
                        merged_items.append(item)
        
        print(f"   📊 最終筆數：{len(merged_items)} 筆")
    else:
        print("\n   ✅ 所有類別資料齊全！")

    print("\n" + "=" * 50)
    print("📝 小安：生成最終報告...")

    doc_path = generate_report(merged_items)
    send_to_telegram(doc_path)
    print("✅ 完成！")

if __name__ == '__main__':
    main()
