# 小安每日任務清單 (DAILY_TASKS)

> 最後更新：2026-04-21

---

## 📋 任務排程總覽

### 每日任務

| 時間 | 任務 | 腳本 | 狀態 |
|------|------|------|------|
| 01:00 | 🏪 591店面出租報告 | `591_shop_report.py` | ✅ |
| 02:00 | 📊 台股每日研究報告 | `taiwan_stock_report_v4.py` | ✅ |
| 02:00 | ☀️ 晨間摘要 | `morning_briefing.py` | ✅ |
| 04:45 | 📈 股市早盤 | `daily_market_report.py` | ✅ |
| 06:00 | 📰 全方位新聞快報 | `daily_news_report.py` | ✅ |
| 每6小時 | 🌍 中東局勢追蹤 | `middle_east_report.py` | ✅ |
| 14:00 | 📈 股市午盤 | `daily_market_report.py` | ✅ |
| 23:00 | 💾 OpenClaw 備份 | `backup_openclaw.sh` | ✅ |

---

### 每週任務

| 時間 | 任務 | 腳本 | 狀態 |
|------|------|------|------|
| 週一 09:00 | 🧠 記憶維護 | `memory_maintenance.sh` | ✅ |
| 週一 09:30 | 📋 Notion 每週報告 | `weekly_notion_report.py` | ✅ |
| 週五 14:30 | 🏷️ 促銷活動報告 | `promotion_summary_report.py` | ✅ |
| 週五 16:00 | 🌴 週末行程規劃 | `weekend_plan_report.py` | ✅ |
| 週六 03:00 | 📔 每週日記報告 | `weekly_notion_diary_report.py` | ✅ |
| 週六 09:00 | 📊 股票績效分析 | `market_performance_2026.py` | ✅ |

---

### 每月/每季任務

| 時間 | 任務 | 腳本 | 狀態 |
|------|------|------|------|
| 每月 1日 00:00 | 📊 資產報酬率報告 | `asset_performance_report.py` | ✅ |
| 每季 15日 00:00 | 📊 台積電財報分析 | `tsmc_analysis_report.py` | ✅ |
| 每季 15日 00:00 | 📊 輝達財報分析 | `nvda_analysis_report.py` | ✅ |
| 每季 15日 00:00 | 📊 美股七雄彙整 | `magnificent_seven_summary_full.py` | ✅ |

---

## 📊 任務執行狀態

### ✅ 已設定（自動化）

- [x] Crontab 已完整設定
- [x] 所有腳本 shebang 已更新為 Python 3.14
- [x] Bot Token 已統一為小安的新Bot

### ⚠️ 需要確認

- [ ] 591 店面的搜尋條件是否仍適用
- [ ] 晨間摘要是否包含老闆需要的所有資訊

---

## 🔧 手動執行指令

### 立即執行備份
```bash
bash ~/.openclaw/workspace/scripts/backup_openclaw.sh
```

### 立即執行新聞快報
```bash
/usr/local/bin/python3.14 ~/.openclaw/workspace/scripts/daily_news_report.py
```

### 立即執行股市報告
```bash
/usr/local/bin/python3.14 ~/.openclaw/workspace/scripts/daily_market_report.py
```

### 立即執行中東局勢追蹤
```bash
/usr/local/bin/python3.14 ~/.openclaw/workspace/scripts/middle_east_report.py
```

---

## 📝 任務新增/修改記錄

| 日期 | 修改內容 |
|------|---------|
| 2026-04-19 | 新增美股七雄完整彙整報告 |
| 2026-04-20 | 修正 daily_news_report.py 的 RSS 解析問題 |
| 2026-04-20 | 統一所有腳本的 Bot Token 為新 Bot |
| 2026-04-22 | 新增台股每日研究報告（川寶投顧每天研究三檔股票） |

---

## ⚠️ 重要提醒

1. **Bot Token 已統一**：`8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw`
2. **Python 版本**：所有腳本使用 `#!/usr/local/bin/python3.14`
3. **備份位置**：`~/Desktop/📂 OpenClaw_下載/backup/`

---

*小安製作 ❤️*
