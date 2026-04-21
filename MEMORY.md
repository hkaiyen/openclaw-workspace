# MEMORY.md - 小安的長期記憶

## 重要設定

- **老闆名稱**: Hsueh Kaiyen
- **助理名稱**: 小安
- **所有報告語言**: 繁體中文（無例外）

## Agent 系統架構

### 四助理分工

| 助理 | 腳本/對話 | 執行方式 | 模型 |
|------|-----------|---------|------|
| 🐰 小安 | 全部（腳本+對話）| **OpenClaw直接執行** | MiniMax |
| 🐰 拉瑪 | 研究報告 | Groq API | Llama 3.3 |
| 🐰 千問 | 研究報告 | Groq API | **qwen/qwen3-32b** |
| 🐰 小歐 | 創意發散、另類觀點 | OpenRouter API | openrouter/free |

### 說明

- **小安**：所有工作由 OpenClaw 直接處理（排程任務、對話、腳本）
- **拉瑪/千問**：作為研究報告的備援，透過 Groq API 執行

## 老闆偏好

- 繁體中文為主
- 幽默風趣的互動
- 反覆確認後再提供重要資訊
- 報告自動發送到 Telegram

## 任務排程（OpenClaw 執行）

| 時間 | 任務 | 腳本 |
|------|------|------|
| 01:00 | 🏪 591店面出租報告 | 591_shop_report.py |
| 02:00 | ☀️ 晨間摘要 | morning_briefing.py |
| 04:45 | 📈 股市早盤 | daily_market_report.py |
| 06:00 | 📰 全方位新聞快報 | daily_news_report.py |
| 11:00/23:00 | 💾 備份OpenClaw | backup_openclaw.sh |
| 14:00 | 📈 股市午盤 | daily_market_report.py |
| 每6小時 | 🌍 中東局勢追蹤 | middle_east_report.py |
| 週一 09:00 | 🧠 記憶維護 | memory_maintenance.sh |
| 週五 14:00 | 🏷️ 促銷活動報告 | promotion_summary_report.py |
| 週五 16:00 | 🌴 週末行程規劃 | weekend_plan_report.py |
| 週六 02:00 | 📊 股票績效分析 | market_performance_2026.py |
| 每月1日 00:00 | 📊 資產報酬率報告 | asset_performance_report.py |
| 每季15日 00:00 | 📊 台積電TSM財報分析 | tsmc_analysis_report.py |
| 每季15日 00:00 | 📊 輝達NVDA財報分析 | nvda_analysis_report.py |
| 每季15日 00:00 | 📊 美股科技七雄完整彙整 | magnificent_seven_summary_full.py |

## API Keys

- **Groq API**: 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
- **FINNHUB_API_KEY**: d7btfs1r01quh9fbn7m0d7btfs1r01quh9fbn7mg
- **Notion Token**: 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

## 資料庫

- 周記資料庫: 2d66a4ae-1760-8120-aeaa-e6a05deb4f90
- 日記資料庫: 1716a4ae-1760-81cb-aada-dac840549da5（2026年內容空白）

## 小歐助理設定

| 項目 | 內容 |
|------|------|
| 名稱 | 小歐 |
| 模型 | OpenRouter (openrouter/free) |
| API Key | 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 |
| Base URL | https://openrouter.ai/api/v1 |

---

_最後更新: 2026-04-21_

## iCloud CalDAV 設定

| 項目 | 內容 |
|------|------|
| 帳號 | Hkaiyen@icloud.com |
| 應用專用密碼 | lpve-dfwe-spxv-pcdh |
| CalDAV 主機 | p116-caldav.icloud.com:443 |
| User ID | 1056470819 |
| 行事曆首頁 | https://p116-caldav.icloud.com:443/1056470819/calendars/ |

### 行事曆清單

| UUID | 名稱 |
|------|------|
| 5B62C2B1-1709-4A2B-9036-AD2021FD4DF5 | 行事曆（主要）|
| 1E8BE61F-92D9-4D01-9716-1D8AC2FA751B | T-EX行事曆 |
| 33C297E9-D9DA-4C60-9E99-AC81AFFD2044 | Work |
| 5725E222-1287-4AFF-8428-A1440DA2CA82 | Financial |
| 6CADDA48-509D-4675-8A4E-087D978D8FDB | Routine |
| C7C84572-8C29-40C4-97BE-216356344150 | 台灣節日 |

