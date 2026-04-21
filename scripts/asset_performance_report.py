#!/usr/bin/python3
"""2026年各資產報酬率報告"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import subprocess, datetime, json, os, time

BOT_TOKEN = '8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw'
CHAT_ID = '8779713208'

GREEN = RGBColor(0x00, 0x80, 0x00)
RED = RGBColor(0xCC, 0x00, 0x00)

def set_color(cell, text, color):
    """在儲存格中設置帶顏色的文字"""
    p = cell.paragraphs[0]
    p.clear()
    run = p.add_run(text)
    run.font.color.rgb = color
    run.bold = True

def generate_report():
    today = datetime.datetime.now()
    date_str = today.strftime('%Y%m%d_%H%M')
    out_dir = '/root/.openclaw/reports/daily'
    os.makedirs(out_dir, exist_ok=True)
    output_path = out_dir + '/2026年資產報酬率報告_' + date_str + '.docx'

    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    title = doc.add_heading('📊 2026年各資產報酬率報告', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.size = Pt(26)
    title.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    date_p = doc.add_paragraph()
    date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dr = date_p.add_run('報告日期：' + today.strftime('%Y年%m月%d日'))
    dr.font.size = Pt(12)
    dr.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

    period_p = doc.add_paragraph()
    period_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pr = period_p.add_run('資料區間：2026年01月01日 ～ 2026年04月19日')
    pr.font.size = Pt(11)
    pr.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)

    doc.add_paragraph()

    # 股市與加密貨幣
    h1 = doc.add_heading('📈 股市與加密貨幣', level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    table = doc.add_table(rows=10, cols=4)
    table.style = 'Table Grid'
    hdr = table.rows[0].cells
    hdr[0].text = '資產'
    hdr[1].text = '期初價格'
    hdr[2].text = '期末價格'
    hdr[3].text = '報酬率'
    for c in hdr:
        c.paragraphs[0].runs[0].bold = True

    data = [
        ('🏆 韓股 (^KS11)', '4,309.63', '6,191.92', '+43.68%', True),
        ('🇹🇼 台股 (^TWII)', '29,349.81', '36,804.34', '+25.40%', True),
        ('📈 日經 (^N225)', '51,832.80', '58,475.90', '+12.82%', True),
        ('📈 Nasdaq (^IXIC)', '23,241.99', '24,468.48', '+5.28%', True),
        ('📈 S&P 500 (^GSPC)', '6,845.50', '7,126.06', '+4.10%', True),
        ('📈 Dow Jones (^DJI)', '48,063.29', '49,447.43', '+2.88%', True),
        ('➖ 美債 (TLT)', '87.16', '87.07', '-0.10%', False),
        ('📉 港股 (^HSI)', '26,338.47', '26,160.33', '-0.68%', False),
        ('💰 比特幣 (BTC-USD)', '87,508.83', '75,048.20', '-14.24%', False),
    ]

    for i, (asset, start, end, ret, is_positive) in enumerate(data):
        table.rows[i+1].cells[0].text = asset
        table.rows[i+1].cells[1].text = start
        table.rows[i+1].cells[2].text = end
        color = GREEN if is_positive else RED
        set_color(table.rows[i+1].cells[3], ret, color)

    doc.add_paragraph()

    # 貴金屬
    h2 = doc.add_heading('🥇 貴金屬', level=1)
    h2.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    table2 = doc.add_table(rows=2, cols=4)
    table2.style = 'Table Grid'
    hdr2 = table2.rows[0].cells
    hdr2[0].text = '資產'
    hdr2[1].text = '期初價格'
    hdr2[2].text = '期末價格'
    hdr2[3].text = '報酬率'
    for c in hdr2:
        c.paragraphs[0].runs[0].bold = True

    table2.rows[1].cells[0].text = '🥇 黃金 (GC=F)'
    table2.rows[1].cells[1].text = '4,325.60'
    table2.rows[1].cells[2].text = '4,879.60'
    set_color(table2.rows[1].cells[3], '+12.81%', GREEN)

    doc.add_paragraph()

    # 台灣房地產
    h3 = doc.add_heading('🏠 台灣房地產', level=1)
    h3.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    table3 = doc.add_table(rows=4, cols=3)
    table3.style = 'Table Grid'
    hdr3 = table3.rows[0].cells
    hdr3[0].text = '指標'
    hdr3[1].text = '數據'
    hdr3[2].text = '說明'
    for c in hdr3:
        c.paragraphs[0].runs[0].bold = True

    estate = [
        ('都市地價指數', '106.44', '114H2，年增 +1.03%', True),
        ('住宅買賣均價', '1,324萬/戶', '114Q2，年減 -5.55%', False),
        ('租金指數', '110.21', '115/03（2026年3月），年增 +2.01%', True),
    ]
    for i, (idx, val, desc, is_positive) in enumerate(estate):
        table3.rows[i+1].cells[0].text = idx
        table3.rows[i+1].cells[1].text = val
        # 說明欄位中的正負值
        p = table3.rows[i+1].cells[2].paragraphs[0]
        p.clear()
        if '+' in desc:
            run1 = p.add_run(desc.split('+')[0] + '+')
            run1.font.color.rgb = GREEN
            run2 = p.add_run(desc.split('+')[1])
            run2.font.color.rgb = GREEN
        else:
            run1 = p.add_run(desc.split('-')[0] + '-')
            run1.font.color.rgb = RED
            run2 = p.add_run(desc.split('-')[1])
            run2.font.color.rgb = RED

    doc.add_paragraph()

    note = doc.add_paragraph()
    note_run = note.add_run('※ 2026年以來台灣房地產價格指數帳面報酬率約 +1~2%（年化），落後股市表現。')
    note_run.font.size = Pt(10)
    note_run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    note_run.italic = True

    doc.add_paragraph()

    # 定存利率
    h4 = doc.add_heading('💵 定存利率', level=1)
    h4.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    table4 = doc.add_table(rows=4, cols=3)
    table4.style = 'Table Grid'
    hdr4 = table4.rows[0].cells
    hdr4[0].text = '項目'
    hdr4[1].text = '利率'
    hdr4[2].text = '說明'
    for c in hdr4:
        c.paragraphs[0].runs[0].bold = True

    deposit = [
        ('央行重貼現率', '2.00%', '維持不變（自2024年3月起）'),
        ('1年期定存利率', '1.50%', '銀行平均（無風險利率）'),
        ('今年以來利息收入', '約 0.375%', '4個月約當'),
    ]
    for i, (item, rate, desc) in enumerate(deposit):
        table4.rows[i+1].cells[0].text = item
        table4.rows[i+1].cells[1].text = rate
        table4.rows[i+1].cells[2].text = desc

    doc.add_paragraph()

    # 總結
    h5 = doc.add_heading('📋 投資績效總評', level=1)
    h5.runs[0].font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    summary = [
        ('🏆 今年以來表現最佳：韓股 (+43.68%)、台股 (+25.40%)，亞股漲幅驚人', True),
        ('📉 今年以來表現最差：比特幣 (-14.24%)，加密貨幣波動劇烈', False),
        ('🥇 黃金 (+12.81%) 表現亮眼，避險需求支撐價格', True),
        ('💵 定存報酬 (+1.50%)，無風險資產最穩健', True),
        ('🏠 台灣房地產 (+1~2%) 保守穩健，遠落後股市', True),
    ]
    for s, is_positive in summary:
        p = doc.add_paragraph()
        # 彩色顯示正負值
        if is_positive:
            # 找到 (+...) 部分並著色
            if '+' in s:
                idx = s.index('+')
                run1 = p.add_run(s[:idx])
                run2 = p.add_run(s[idx:])
                run2.font.color.rgb = GREEN
                run2.bold = True
            else:
                p.add_run(s)
        else:
            if '-' in s:
                idx = s.index('-')
                run1 = p.add_run(s[:idx])
                run2 = p.add_run(s[idx:])
                run2.font.color.rgb = RED
                run2.bold = True
            else:
                p.add_run(s)
        p.paragraph_format.space_after = Pt(6)

    footer = doc.sections[0].footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = fp.add_run('小安智能助理｜老闆的專屬理財幫手  ◎ 2026年資產報酬率報告')
    fr.font.size = Pt(9)
    fr.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)

    doc.save(output_path)
    return output_path

def send_telegram(file_path):
    today = datetime.datetime.now()
    caption = (
        '📊 2026年各資產報酬率報告\n'
        + today.strftime('%Y年%m月%d日') + '\n\n'
        '資料區間：2026/01/01 ～ 2026/04/19\n\n'
        '📈 股市、加密貨幣、貴金屬\n'
        '🏠 台灣房地產\n'
        '💵 定存利率\n\n'
        '✅ 報酬率：綠色(+) 紅色(-)\n\n'
        '看完記得分享給需要的人！'
    )
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': CHAT_ID, 'caption': caption}
            resp = requests.post(
                'https://api.telegram.org/bot' + BOT_TOKEN + '/sendDocument',
                data=data, files=files, timeout=30)
            return resp.json().get('ok', False)
    except:
        return False

if __name__ == '__main__':
    import requests
    print('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] 產生2026年資產報酬率報告...')
    report_path = generate_report()
    print('  📄 報告已生成: ' + report_path)
    print('  發送到Telegram...')
    if send_telegram(report_path):
        print('  ✅ 已發送到Telegram')
    else:
        print('  ❌ 發送失敗')
    print('[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] 任務完成！')
