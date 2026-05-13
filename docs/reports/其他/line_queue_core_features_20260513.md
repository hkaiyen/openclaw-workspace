# LINE 餐廳候補位系統 - Phase 4 核心功能開發報告

**文件版本：** 1.0  
**日期：** 2026-05-13  
**作者：** 小咪技術研發助理  
**適用時區：** Asia/Taipei (GMT+8)

---

## 一、任務概述

Phase 4 完成了 LINE 餐廳候補位系統的核心功能開發，包含 LIFF 前端頁面、餐廳管理後台、以及核心商業邏輯服務。

---

## 二、產出檔案清單

### 2.1 LIFF 前端頁面（消費者端）

| 檔案路徑 | 說明 |
|----------|------|
| `public/liff/queue/join.html` | 加入排隊頁面 |
| `public/liff/queue/status.html` | 排隊進度查詢頁面 |
| `public/liff/reservation/book.html` | 線上預約頁面 |
| `public/liff/reservation/my.html` | 我的預約頁面 |

### 2.2 餐廳管理後台

| 檔案路徑 | 說明 |
|----------|------|
| `public/admin/index.html` | 餐廳管理後台主頁面（包含儀表板、排隊管理、預約管理、設定） |

### 2.3 核心服務層

| 檔案路徑 | 說明 |
|----------|------|
| `src/services/queueService.js` | 排隊服務（加入排隊、叫號、順位計算） |
| `src/services/reservationService.js` | 預約服務（建立預約、取消、時間衝突檢查） |
| `src/services/notificationService.js` | 通知服務（叫號通知、預約提醒、過號提醒） |
| `src/services/index.js` | 服務層匯出模組 |

### 2.4 路由整合

| 檔案路徑 | 說明 |
|----------|------|
| `src/routes/index.js` | 路由整合模組（LIFF 頁面路由 + API 路由） |

---

## 三、LIFF 前端頁面功能

### 3.1 加入排隊頁面（join.html）

**功能說明：**
- 顯示餐廳列表（包含等候人數）
- 選擇餐廳、填寫用餐人數、備註
- 提交後顯示排隊成功訊息（號碼、預估等候時間）
- 失敗時顯示錯誤訊息

**技術特點：**
- 使用原生 HTML + CSS + JavaScript（無框架依賴）
- LIFF SDK 初始化並取得使用者資料
- 示範模式：網路失敗時使用假資料展示功能
- 響應式設計，適合手機瀏覽

**UI 元件：**
- 餐廳選擇器（Radio button 清單）
- 人數下拉選單（1-10 人）
- 備註文字區塊
- 成功彈窗（顯示號碼與順位）

### 3.2 排隊進度頁面（status.html）

**功能說明：**
- 顯示目前排隊號碼與順位
- 即時更新排隊狀態（等待中/已叫號/已入座）
- 被叫號時顯示通知彈窗
- 可取消排隊
- 自動每 30 秒更新狀態

**技術特點：**
- Polling 機制定期更新狀態
- 叫號時自動彈出通知
- 支援 URL 參數傳入 restaurantId
- 歷史排隊記錄查詢

**UI 元件：**
- 排隊號碼大字顯示
- 順位與預估等候時間卡片
- 狀態標籤（等待中/已叫號/已入座）
- 叫號通知全屏彈窗

### 3.3 線上預約頁面（book.html）

**功能說明：**
- 選擇餐廳、日期、時間、人數
- 可填寫備註（過敏原、慶生等）
- 提交後顯示預約成功確認
- 日期選擇限制（今天起 30 天內）

**技術特點：**
- 日期選擇器（min/max 限制）
- 時間選擇（午/晚餐時段）
- 與 Phase 3 預約 API 整合

**UI 元件：**
- 餐廳選擇清單
- 日期選擇器
- 時間選擇下拉選單
- 人數選擇
- 預約成功確認彈窗

### 3.4 我的預約頁面（my.html）

**功能說明：**
- 顯示即將到來的預約與歷史記錄
- 切換標籤（ upcoming / past）
- 可取消未到來的預約
- 顯示預約狀態（已確認/已入座/已取消/未到場）

**技術特點：**
- Tab 切換即將到來/歷史記錄
- 取消二次確認機制
- 預約狀態即時更新

**UI 元件：**
- Tab 篩選器
- 預約卡片（餐廳名稱、日期、時間、人數、狀態）
- 取消確認彈窗

---

## 四、餐廳管理後台功能

### 4.1 儀表板（Dashboard）

**功能說明：**
- 即時統計（等待中/已叫號/已入座/今日預約）
- 叫號面板（叫下一位/叫指定號碼）
- 排隊名單即時顯示

**技術特點：**
- 即時更新統計數字
- 叫號後自動刷新名單
- 示範資料展示

**UI 元件：**
- 4 格統計卡片
- 叫號按鈕面板
- 排隊名單（可滑動）

### 4.2 排隊管理（Queue Management）

**功能說明：**
- 表格顯示所有排隊資料
- 可針對個別排隊執行：叫號、入座、過號、移除
- 狀態篩選

**技術特點：**
- 表格化排隊名單
- 狀態色彩標示
- 快速操作按鈕

### 4.3 預約管理（Reservations）

**功能說明：**
- 查看今日/明日/本週預約
- 標記預約入座
- 電話聯絡功能

**技術特點：**
- 日期篩選
- 預約狀態標示

### 4.4 基本設定（Settings）

**功能說明：**
- 餐廳名稱、電話、地址設定
- 座位數、平均用餐時長、排隊上限設定
- 儲存設定至資料庫

---

## 五、核心服務層設計

### 5.1 排隊服務（QueueService）

**主要函數：**

| 函數 | 說明 |
|------|------|
| `joinQueue()` | 加入排隊、檢查重複、檢查人數上限、發送通知 |
| `cancelQueue()` | 取消排隊（驗證所屬權限） |
| `callNext()` | 叫下一位、發送 LINE 通知 |
| `callSpecific()` | 叫指定號碼、發送 LINE 通知 |
| `markAsServed()` | 標記入座 |
| `markAsNoShow()` | 標記過號 |
| `calculateQueuePosition()` | 計算排隊順位 |
| `getQueueStatus()` | 取得排隊狀態 |
| `getQueueStats()` | 取得排隊統計 |

**商業邏輯：**
- 加入排隊前檢查：餐廳是否存在、是否重複排隊、排隊人數是否已滿
- 叫號時自動發送 LINE 推播通知消費者
- 順位計算：前方有多少組正在等待

### 5.2 預約服務（ReservationService）

**主要函數：**

| 函數 | 說明 |
|------|------|
| `createReservation()` | 建立預約、檢查時間衝突、發送確認通知 |
| `cancelReservation()` | 取消預約（驗證權限與狀態） |
| `checkTimeConflict()` | 檢查預約時間是否衝突（30 分鐘緩衝） |
| `getMyReservations()` | 取得消費者的預約列表 |
| `markAsSeated()` | 標記已入座 |
| `markAsNoShow()` | 標記過號 |
| `getReservationsByRestaurant()` | 取得餐廳的預約列表 |
| `sendReminder()` | 發送預約提醒 |

**商業邏輯：**
- 預約時間衝突檢查：同一餐廳同時間段（前後 30 分鐘）不得超過座位數
- 取消限制：已入座或已取消的預約無法再取消
- 預約提醒：可對已確認的預約發送提醒

### 5.3 通知服務（NotificationService）

**主要函數：**

| 函數 | 說明 |
|------|------|
| `sendCallNotification()` | 發送叫號通知 |
| `sendQueueJoinedNotification()` | 發送排隊成功通知 |
| `sendReservationConfirmedNotification()` | 發送預約確認通知 |
| `sendReservationReminder()` | 發送預約提醒 |
| `sendQueueCancelledNotification()` | 發送排隊取消通知 |
| `sendNoShowReminder()` | 發送過號提醒 |
| `sendBatch()` | 批量發送通知 |
| `getNotificationStats()` | 取得通知統計 |
| `retryFailedNotifications()` | 重試失敗的通知 |

**商業邏輯：**
- 所有通知皆使用 Flex Message 格式
- 發送失敗時記錄至 notification_logs 資料表
- 支援批量發送（用於促銷、公告等）
- 失敗通知自動重試機制

---

## 六、路由整合

### 6.1 LIFF 頁面路由

| Method | 路徑 | 說明 |
|--------|------|------|
| GET | `/liff/queue/join` | 加入排隊頁面 |
| GET | `/liff/queue/status` | 排隊進度頁面 |
| GET | `/liff/reservation/book` | 預約頁面 |
| GET | `/liff/reservation/my` | 我的預約頁面 |

### 6.2 管理後台路由

| Method | 路徑 | 說明 |
|--------|------|------|
| GET | `/admin` | 餐廳管理後台首頁 |
| GET | `/admin/settings` | 餐廳設定頁面 |

### 6.3 API 路由

| Method | 路徑 | 說明 |
|--------|------|------|
| POST | `/api/queue/call-next` | 叫下一位 |
| POST | `/api/queue/call-specific` | 叫指定號碼 |
| POST | `/api/queue/mark-served` | 標記入座 |
| POST | `/api/queue/mark-no-show` | 標記過號 |
| GET | `/api/queue/list/:restaurantId` | 取得排隊名單 |
| GET | `/api/queue/stats/:restaurantId` | 取得排隊統計 |
| GET | `/api/reservations/:restaurantId` | 取得預約列表 |
| POST | `/api/reservations/mark-seated` | 標記已入座 |
| POST | `/api/reservations/mark-no-show` | 標記過號 |
| GET | `/api/notifications/:restaurantId` | 取得通知歷史 |

---

## 七、系統架構圖（Phase 4 完成後）

```
┌─────────────────────────────────────────────────────────────────┐
│                        使用者層                                  │
├─────────────────────────────────────────────────────────────────┤
│  [LINE App]  ◄──── LINE Official Account (機器人)               │
│     │              (LINE Messaging API + LINE Frontend Framework)│
│     │                                                             │
│  ┌──┴──────────────────────────────────────┐                    │
│  │         LIFF 頁面（嵌入在 LINE 內）         │                    │
│  │  • join.html - 加入排隊                   │                    │
│  │  • status.html - 排隊進度                  │                    │
│  │  • book.html - 線上預約                    │                    │
│  │  • my.html - 我的預約                      │                    │
│  └──────────────────────────────────────────┘                    │
│                                                              │
│  ┌──────────────────────────────────────┐                    │
│  │         Admin 後台（瀏覽器）              │                    │
│  │  • index.html - 儀表板/排隊/預約/設定    │                    │
│  └──────────────────────────────────────────┘                    │
├─────────────────────────────────────────────────────────────────┤
│                       服務層                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ queueService│  │reservService│  │notifService│               │
│  │            │  │            │  │            │                │
│  └────────────┘  └────────────┘  └────────────┘                │
├─────────────────────────────────────────────────────────────────┤
│                       路由層                                     │
│  src/routes/index.js                                           │
│  • LIFF 頁面路由                                                │
│  • Admin 頁面路由                                               │
│  • API 路由                                                     │
├─────────────────────────────────────────────────────────────────┤
│                       資料層                                     │
│  PostgreSQL ◄──── Repositories ◄──── Services                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 八、技術特點

### 8.1 前端技術

- **無框架依賴**：使用原生 HTML + CSS + JavaScript，降低學習曲線
- **響應式設計**：支援手機（LIFF）與桌面（Admin）瀏覽
- **LIFF SDK 整合**：標準 LINE LIFF 初始化流程
- **示範模式**：網路失敗時使用假資料展示功能，提升開發體驗

### 8.2 後端技術

- **服務導向架構**：商業邏輯封裝於 Service 層
- **Repository 模式**：資料存取封裝於 Repository 層
- **路由集中管理**：所有頁面與 API 路由於 `src/routes/index.js`
- **錯誤處理**：統一的錯誤回應格式與例外處理

### 8.3 LIFF 整合

- **無痛初始化**：嘗試 LIFF 登入，失敗時使用 URL 參數 fallback
- **訊息傳送**：使用 `liff.sendMessages()` 與 Bot 互動
- **外部開窗**：使用 `liff.openWindow()` 開啟連結

---

## 九、已知限制

| 項目 | 說明 | 建議改進 |
|------|------|----------|
| 無即時更新 | 目前使用 polling，未使用 WebSocket | 可加入 Socket.io 或 Redis Pub/Sub |
| 無使用者認證 | Admin 後台無登入機制 | 可加入 Basic Auth 或 JWT |
| 無操作日誌 | 餐廳操作（叫號、標記）無完整日誌 | 加入操作日誌資料表 |
| 無權限管理 | Admin 同一權限等級 | 可加入角色（Admin/Manager/Staff） |
| 無資料匯出 | 排隊/預約資料無匯出功能 | 加入 CSV/Excel 匯出 |

---

## 十、下一步（Phase 5 建議）

Phase 4 完成後，建議進入以下項目：

### 10.1 生產環境準備

1. **LINE 官方設定**
   - 申請正式 LIFF ID 並設定至程式碼
   - 設定 Rich Menu 綁定至 LIFF 頁面
   - 設定 Webhook URL 至 LINE Developers Console

2. **安全性強化**
   - Admin 後台加入登入驗證
   - Webhook 簽章驗證確保安全
   - LINE Channel Secret 安全儲存

3. **效能優化**
   - Redis 整合（排隊名單快取）
   - 資料庫索引優化
   - 連線池設定調優

### 10.2 功能擴展

1. **即時通知**
   - WebSocket 或 Server-Sent Events 即時更新
   - Redis Pub/Sub 實現跨實例通知

2. **報表功能**
   - 來客數統計
   - 等候時間分析
   - 高峰時段統計

3. **消費者端優化**
   - 排隊預估時間更精準
   - 過號處理邏輯優化
   - 預約修改功能

4. **多店支援**
   - 連鎖餐廳管理
   - 店鋪間排隊轉移

---

## 十一、檔案總覽（Phase 4 新增）

```
line_queue/
├── public/
│   ├── liff/
│   │   ├── queue/
│   │   │   ├── join.html           # 加入排隊頁面（新增）
│   │   │   └── status.html         # 排隊進度頁面（新增）
│   │   └── reservation/
│   │       ├── book.html           # 線上預約頁面（新增）
│   │       └── my.html             # 我的預約頁面（新增）
│   └── admin/
│       └── index.html              # 餐廳管理後台（新增）
├── src/
│   ├── services/                   # 核心商業邏輯（新增）
│   │   ├── index.js                # 服務層匯出
│   │   ├── queueService.js         # 排隊服務
│   │   ├── reservationService.js    # 預約服務
│   │   └── notificationService.js   # 通知服務
│   └── routes/
│       └── index.js                # 路由整合模組（新增）
├── sql/                            # （Phase 2 已完成）
├── docker-compose.yml              # （Phase 2 已完成）
└── .env.example                    # （Phase 3 已完成）
```

---

**文件結尾**

Phase 4 核心功能開發已全部完成。所有 LIFF 前端頁面、餐廳管理後台、以及核心商業邏輯服務均已就緒。系統已具備基本的候補位與預約功能，可進行整合測試與 LINE 官方設定。

---
*小咪技術研發助理｜2026-05-13*