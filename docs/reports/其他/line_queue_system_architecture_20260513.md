# LINE 餐廳候補位系統 - 系統架構設計書

**文件版本：** 1.0  
**日期：** 2026-05-13  
**作者：** 小咪技術研發助理  
**適用時區：** Asia/Taipei (GMT+8)

---

## 一、系統概述

### 1.1 系統定位

LINE 餐廳候補位系統是一個 **B2B2C 雙向平台**，連接餐廳與消費者：

- **面向餐廳（餐廳管理系統）：** 排隊管理、候位現場登記、通知發送、報表分析
- **面向消費者（LINE 應用）：** LINE 官方帳號內直接預約、候補、查看排隊進度

### 1.2 核心價值主張

- 消費者無需下載任何 APP，透過 LINE 即可完成所有操作
- 餐廳可有效管理現場排隊，提升座位周轉率
- 即時推播通知，減少消費者在現場久候的困擾

---

## 二、需求分析

### 2.1 B2B 餐廳需求

| 需求項目 | 說明 | 優先級 |
|----------|------|--------|
| 現場候補登記 | 消費者可現場掃 QR code 加入排隊 | Must have |
| 預約管理 | 接受未來時間的訂位預約 | Must have |
| 叫號通知 | 手動或自動叫號，並發送 LINE 通知 | Must have |
| 座位管理 | 標記座位空/滿/待清理狀態 | Must have |
| 客戶管理 | 查看消費者排隊/預約歷史 | Should have |
| 報表分析 | 來客數、等候時間、高峰時段統計 | Should have |
| 多店支援 | 支援連鎖餐廳多據點管理 | Nice to have |
| API 串接 | 對接餐廳現有 POS/ERP 系統 | Nice to have |

### 2.2 B2C 消費者需求

| 需求項目 | 說明 | 優先級 |
|----------|------|--------|
| 加入排隊 | 從 LINE 官方帳號加入排隊名單 | Must have |
| 查看排隊進度 | 即時查看前方等候組數 | Must have |
| 取消排隊 | 臨時有事可取消排隊 | Must have |
| 預約未來時段 | 可預約隔日或未來幾天的時段 | Must have |
| 接收通知 | 被叫號時收到 LINE 推播通知 | Must have |
| 過號處理 | 過號後可選擇重新排隊或繼續等候 | Should have |
| 我的預約 | 查詢/修改/取消已預約的時段 | Should have |

### 2.3 MVP 核心功能清單

```
MVP 功能（6-10週開發）

餐廳端：
✅ 餐廳設定（基本資料、座位數、等候人數上限）
✅ 現場候補登記（掃 QR code 加入排隊）
✅ 叫號功能（下一位、手動叫指定號碼）
✅ LINE 推播通知消費者
✅ 排隊名單管理（查看名單、移除、標記）

消費者端：
✅ 加入排隊（從 LINE 官方帳號）
✅ 查看排隊進度
✅ 接收被叫號通知
✅ 取消排隊
✅ 預約未來時段
✅ 取消預約

LINE 官方帳號：
✅ 自動回應（關鍵字觸發功能選單）
✅ 推播訊息（叫號通知、排隊進度）
✅ LIFF 頁面（排隊、預約、表單）
```

---

## 三、系統架構設計

### 3.1 整體架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                        使用者層                                  │
├─────────────────────────────────────────────────────────────────┤
│  [LINE App]  ◄──── LINE Official Account (機器人)               │
│     │              (LINE Messaging API + LINE Frontend Framework)│
│     │                                                             │
│  ┌──┴──────────────────────────────────────┐                    │
│  │         LIFF 頁面（嵌入在 LINE 內）         │                    │
│  │  • 排隊登記表單                           │                    │
│  │  • 我的排隊/預約查詢                      │                    │
│  │  • 排隊進度顯示                           │                    │
│  └──────────────────────────────────────────┘                    │
├─────────────────────────────────────────────────────────────────┤
│                       API 閘道層                                  │
│              (LINE Messaging API Webhook)                        │
│                    Nginx / Cloudflare                            │
├─────────────────────────────────────────────────────────────────┤
│                       服務層                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │  LINE API  │  │  Web App   │  │  Background │                │
│  │  Service   │  │  Service   │  │  Job Worker │                │
│  │            │  │            │  │ (叫號排程)  │                │
│  └────────────┘  └────────────┘  └────────────┘                │
├─────────────────────────────────────────────────────────────────┤
│                       資料層                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ PostgreSQL │  │  Redis     │  │ LINE API   │                │
│  │ (主資料庫)  │  │ (快取/佇列) │  │ (第三方)    │                │
│  └────────────┘  └────────────┘  └────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 技術棧建議

| 層級 | 選擇 | 理由 |
|------|------|------|
| **後端框架** | Node.js + Express 或 Fastify | 處理非同步 IO 效率高，LINE SDK 生態完整 |
| **資料庫** | PostgreSQL | 結構化資料，支援 JSON 欄位適合 LINE Flex Message |
| **快取/佇列** | Redis | 排隊名單快取、Pub/Sub 通知 |
| **雲端平台** | GCP 或 AWS (台北 region) | 台北節點延遲最低， GCP Cloud Run 或 AWS ECS |
| **容器化** | Docker + Docker Compose | 方便本地開發與部署 |
| **前端（LIFF）** | Vue 3 或 React | 輕量、支援 LINE LIFF SDK |
| **LINE SDK** | `@line/bot-sdk` (Node.js) | 官方 Node.js SDK |

### 3.3 系統元件說明

#### LINE Messaging API Service
- 處理所有 LINE Webhook 事件（加入好友、收到訊息、點擊按鈕等）
- 推送 Flex Message 訊息格式（富媒體卡片）給消費者
- 管理 LINE Official Account 的回應模式

#### Web App Service（餐廳管理後台）
- React + Vite 前端，餐廳管理者操作介面
- 即時更新排隊名單
- 叫號操作觸發 LINE 推播

#### Background Job Worker
- 處理定時任務：自動叫號、通知催單
- 排隊順位自動往前遞進

---

## 四、資料庫設計

### 4.1 資料表 Schema

#### 餐廳資料表：`restaurants`

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| name | VARCHAR(100) | 餐廳名稱 |
| line_channel_id | VARCHAR(100) | LINE Channel ID |
| line_channel_secret | VARCHAR(100) | LINE Channel Secret (加密儲存) |
| line_access_token | TEXT | LINE Long-lived Access Token |
| address | VARCHAR(200) | 地址 |
| phone | VARCHAR(20) | 電話 |
| total_seats | INT | 總座位數 |
| avg_meal_duration_minutes | INT | 平均用餐時長（分鐘） |
| queue_max_size | INT | 排隊人數上限 |
| auto_call_enabled | BOOLEAN | 是否自動叫號 |
| created_at | TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | 更新時間 |

#### 消費者資料表：`customers`

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| line_user_id | VARCHAR(100) | LINE User ID（用於發送推播） |
| display_name | VARCHAR(100) | LINE 顯示名稱 |
| phone | VARCHAR(20) | 電話（可選） |
| created_at | TIMESTAMP | 建立時間 |

#### 排隊資料表：`queue_entries`

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| restaurant_id | UUID | 關聯餐廳 FK |
| customer_id | UUID | 關聯消費者 FK |
| queue_number | INT | 排隊號碼 |
| status | ENUM | 'waiting', 'called', 'served', 'cancelled', 'no_show' |
| party_size | INT | 用餐人數 |
| joined_at | TIMESTAMP | 加入排隊時間 |
| called_at | TIMESTAMP | 被叫號時間 |
| served_at | TIMESTAMP | 入座時間 |
| notes | TEXT | 備註（過敏原等） |
| source | ENUM | 'walk_in', 'reservation', 'waitlist' |

#### 預約資料表：`reservations`

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| restaurant_id | UUID | 關聯餐廳 FK |
| customer_id | UUID | 關聯消費者 FK |
| reservation_date | DATE | 預約日期 |
| reservation_time | TIME | 預約時間 |
| party_size | INT | 用餐人數 |
| status | ENUM | 'confirmed', 'seated', 'cancelled', 'no_show' |
| created_at | TIMESTAMP | 建立時間 |
| notes | TEXT | 備註 |

#### 通知記錄資料表：`notification_logs`

| 欄位 | 型別 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| restaurant_id | UUID | 關聯餐廳 FK |
| customer_id | UUID | 關聯消費者 FK |
| queue_entry_id | UUID | 關聯排隊 FK（可選） |
| notification_type | ENUM | 'queue_called', 'queue_cancelled', 'reminder', 'reservation_confirmed' |
| line_message_id | VARCHAR(100) | LINE 訊息 ID |
| sent_at | TIMESTAMP | 發送時間 |
| status | ENUM | 'sent', 'delivered', 'failed' |

### 4.2 ER 關聯圖

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  restaurants │       │   customers  │       │ queue_entries│
│──────────────│       │──────────────│       │──────────────│
│ id (PK)      │       │ id (PK)     │       │ id (PK)     │
│ name         │       │ line_user_id │       │ restaurant_id│
│ line_channel │       │ display_name │       │ customer_id  │
│ ...          │       │ phone        │       │ queue_number │
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       │                      │                      │
       │              ┌───────┴───────┐              │
       │              │               │              │
       └──────────────┴──┐         ┌──┴──────────────┘
                         │         │
                  ┌──────┴───────┐ │  ┌──────────────┐
                  │ reservations │ │  │notification_logs
                  │──────────────│ │  │──────────────│
                  │ id (PK)      │ │  │ id (PK)     │
                  │ restaurant_id│─┘  │ customer_id │
                  │ customer_id  │────│ queue_entry │
                  │ date/time    │    │ type/status │
                  └──────────────┘    └──────────────┘
```

---

## 五、LINE API 串接規劃

### 5.1 需要的 LINE API 權限

| 權限 | 用途 | 申請位置 |
|------|------|----------|
| Messaging API | 發送推播、接收 Webhook 事件 | LINE Developers Console |
| LINE Frontend Framework (LIFF) | 在 LINE 內嵌入 Web 頁面 | LINE Developers Console |
| Rich Menu | 自訂選單（排隊/預約/查詢） | LINE Developers Console |
| QR Code Login (LINE Login) | 消費者身份驗證 | LINE Developers Console |

### 5.2 LINE Messaging API 功能對應

| 功能 | 使用的 LINE API | 說明 |
|------|----------------|------|
| 加入排隊 | Reply API / Push API | 回應按鈕訊息，發送 Flex Message 確認 |
| 排隊進度查詢 | Push API | 主動推播排隊順位變化 |
| 叫號通知 | Push API | 叫號時主動推播消費者 |
| 關鍵字回應 | Reply API | 消費者傳送關鍵字時自動回覆 |
| 選單按鈕 | Flex Message / Quick Reply | 取代鍵盤輸入，直覺操作 |

### 5.3 LIFF 頁面設計

| LIFF 頁面 | 用途 | 路徑 |
|----------|------|------|
| 加入排隊 | 填寫姓名、人數、備註 | `/liff/queue/join` |
| 我的排隊 | 查看目前排隊狀態、順位 | `/liff/queue/status` |
| 預約時段 | 選擇日期/時間/人数 | `/liff/reservation/book` |
| 我的預約 | 查看/修改/取消預約 | `/liff/reservation/my` |

### 5.4 Webhook 架構設計

```
LINE Platform
     │
     │ POST /webhook (HTTPS)
     ▼
┌─────────────────────────┐
│   LINE Messaging API    │
│   Webhook Receiver      │
│   (Nginx → Express)     │
└───────────┬─────────────┘
            │
     ┌──────┴──────────┐
     │  Event Type     │
     ├─────────────────┤
     │ follow/unfollow │ → 更新顧客名單
     │ message         │ → 關鍵字回應 / 表單輸入
     │ postback        │ → 按鈕點擊（主要操作入口）
     │ beacon          │ → 進店偵測（進階功能）
     └─────────────────┘
```

### 5.5 機器人功能流程圖

```
消費者視角流程：

LINE 官方帳號
     │
     ▼
[加入好友] ──► 發送歡迎訊息 + 功能選單
     │
     ▼
[點擊「加入排隊」] ──► LIFF 頁面 → 填寫表單 → 確認排隊成功
     │
     ▼
[查看排隊進度] ──► 回傳目前順位 + 預估等待時間
     │
     ▼
[收到叫號通知] ──► 前往餐廳櫃檯報到
     │
     ▼
[入座] ──► 更新狀態為 served

餐廳視角流程：

餐廳管理後台
     │
     ▼
[手動叫號] ──► 點擊「叫下一位」──► 發送 LINE 推播給下一位消費者
     │
     ▼
[收到消費者報到] ──► 更新為 seated
     │
     ▼
[下一位自動往前遞進]
```

---

## 六、LINE 官方帳號申請流程

### 步驟 1：建立 LINE 官方帳號

1. 前往 [LINE Official Account Manager](https://manager.line.biz/)
2. 選擇「建立官方帳號」
3. 填入帳號名稱（餐廳名稱）
4. 選擇帳號類型（官方帳號）
5. 類別選擇「餐飲」

### 步驟 2：申請 Messaging API

1. 進入 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇已建立的 Provider
3. 建立新 Channel → 選擇「Messaging API」
4. 填入必要的 Channel 資料
5. 等待審核（約 1-3 工作天）

### 步驟 3：設定 Webhook URL

1. 在 Messaging API 設定頁面
2. 開啟「Use Webhook」功能
3. 填入你的伺服器 Webhook URL：`https://your-domain.com/webhook`
4. 點擊「Verify」確認連線

### 步驟 4：申請 LIFF

1. 在同一個 Channel 頁面
2. 進入「LIFF」標籤
3. 新增 LIFF App（每個功能一個 LIFF ID）
4. 設定：
   - LIFF App 名稱（如「加入排隊」）
   - URL：你的 LIFF 頁面網址
   - Size：Full（佔滿整個畫面）或 Tall
   - Scopes：`openid`, `profile`

### 步驟 5：設定 RICH MENU（選單）

1. 在 LINE Official Account Manager
2. 建立 RICH MENU（最多 10 個）
3. 設定按鈕對應 LIFF URL 或 關鍵字
4. 建議選單：
   - 🔢 加入排隊（LIFF）
   - 📋 我的排隊（LIFF）
   - 📅 線上預約（LIFF）
   - ☎ 聯絡餐廳（電話）

### 步驟 6：設定自動回應訊息

1. 在 Messaging API 設定
2. 設定「Auto Reply」：針對關鍵字自動回覆
3. 設定「Greeting」：新朋友加入時的歡迎訊息

### 申請前置準備

| 項目 | 說明 |
|------|------|
| LINE 帳號 | 個人或公司 LINE 帳號 |
| 電子郵件 | 用於 LINE Developers 註冊 |
| 網站/伺服器 | 可設定 HTTPS 的公開網址（Webhook） |
| 隱私權政策頁面 | LINE 要求必須有公開的隱私權頁面 |
| 服務條款頁面 | 同上 |

---

## 七、預估 MVP 開發時程（8 週）

### 第一階段：基礎建設（第 1-2 週）

| 任務 | 說明 |
|------|------|
| 系統架構與技術選型確認 | 決定技術棧、雲端平台 |
| LINE 官方帳號申請 | 完成 Messaging API + LIFF 申請 |
| 資料庫設計與建立 | PostgreSQL Schema 建立 |
| 基礎 API 框架建立 | Node.js + Express 基礎架構 |
| LINE SDK 串接 | Webhook 接收基礎 |

### 第二階段：餐廳端功能（第 3-4 週）

| 任務 | 說明 |
|------|------|
| 餐廳管理後台登入系統 | 驗證、餐廳設定 |
| 排隊名單管理 UI | 即時顯示排隊名單 |
| 叫號功能 | 手動叫號、下一位按鈕 |
| 基本資料設定 | 座位數、等候上限等 |

### 第三階段：消費者端功能（第 5-6 週）

| 任務 | 說明 |
|------|------|
| LIFF 頁面 - 加入排隊 | 表單填寫、確認 |
| LINE 推播通知 | 叫號時通知消費者 |
| LIFF 頁面 - 查看排隊進度 | 即時順位查詢 |
| 取消排隊功能 | 消費者可取消 |

### 第四階段：預約功能 + 優化（第 7-8 週）

| 任務 | 說明 |
|------|------|
| 線上預約系統 | 日期/時間/人數選擇 |
| 預約管理（餐廳端） | 查看/修改預約 |
| Flex Message 訊息模板設計 | 提升 UI/UX |
| 系統測試與除錯 | 整合測試、修正問題 |
| 部署上線 | 生產環境部署 |

### 階段時程圖

```
週  1    2    3    4    5    6    7    8
─┼───┼───┼───┼───┼───┼───┼───┼───┼──
基礎建設   ████████████
餐廳端功能      ████████████
消費者端功能            ████████████
預約+優化                      ████████████
                                              ████████ 上線
```

---

## 八、功能優先級分類

### Must Have（核心功能）

- [ ] LINE 官方帳號申請與基本設定
- [ ] Webhook 接收與回應
- [ ] LIFF 加入排隊頁面
- [ ] 餐廳端排隊名單管理
- [ ] 叫號功能 + LINE 推播
- [ ] 查看排隊進度（消費者）
- [ ] 取消排隊

### Should Have（重要功能）

- [ ] 線上預約功能
- [ ] 排隊進度推播（主動通知）
- [ ] Flex Message 美化訊息格式
- [ ] 報表分析（來客數、等候時間）
- [ ] 消費者歷史記錄

### Nice to Have（加分功能）

- [ ] 自動叫號排程
- [ ] 多店管理
- [ ] POS 系統串接
- [ ] 優惠券/集點功能
- [ ] 會員分級制度

---

## 九、系統安全考量

### 9.1 LINE Channel Secret 保護
- 儲存於環境變數或加密的 Secret Manager
- 不暴露在 client-side 程式碼

### 9.2 LIFF 安全性
- 使用 `liff.sendMessages()` 前需確認使用者已授權
- 不儲存敏感的 LINE Access Token

### 9.3 Webhook 驗證
- 啟用 LINE Webhook 簽章驗證（`X-LINE-Signature` header）
- 驗證每個請求是否來自 LINE Platform

### 9.4 消費者資料保護
- 遵循 LINE 隱私權規範
- 設定隱私權政策頁面（LINE 官方帳號要求）
- 最小化蒐集原則（僅蒐集必要資料）

---

## 十、下一步（Phase 2）

Phase 1 完成後，預計進入以下項目：

1. **LINE Login 整合**：強化消費者身份驗證
2. **自動叫號系統**：根據平均用餐時長自動往前遞進
3. **通知系統優化**：過號提醒、排隊即將到時催單
4. **餐廳管理後台強化**：報表、數據分析
5. **API 文件化**：供後續擴展或第三方串接

---

**文件結尾**

本文件為 LINE 餐廳候補位系統的**第一階段系統架構設計書**，基於 LINE Messaging API 官方文件與業界實務經驗所撰寫。詳細的LINE API 文件請參考：
- [LINE Messaging API 官方文件](https://developers.line.biz/zh-hant/docs/messaging-api/)
- [LINE LIFF 官方文件](https://developers.line.biz/zh-hant/docs/liff/)
- [LINE Developers Console](https://developers.line.biz/console/)

---
*小咪技術研發助理｜2026-05-13*