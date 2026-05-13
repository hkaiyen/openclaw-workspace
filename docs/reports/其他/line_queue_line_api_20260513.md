# LINE 餐廳候補位系統 - Phase 3 LINE API 串接報告

**文件版本：** 1.0  
**日期：** 2026-05-13  
**作者：** 小咪技術研發助理  
**適用時區：** Asia/Taipei (GMT+8)

---

## 一、任務概述

Phase 3 完成了 LINE 餐廳候補位系統的 LINE API 串接工作，包含 LINE SDK 初始化、Webhook 接收與處理、訊息處理常式、Flex Message 訊息模板、LIFF 頁面 API、以及餐廳端叫號 API 等核心功能。

---

## 二、產出檔案清單

### 2.1 設定檔

| 檔案路徑 | 說明 |
|----------|------|
| `config/line.js` | LINE 設定集中管理（Channel、LIFF、Rich Menu、Webhook） |
| `.env.example` | 環境變數範例（已更新 LINE 相關設定） |

### 2.2 LINE SDK 核心

| 檔案路徑 | 說明 |
|----------|------|
| `src/line/client.js` | LINE SDK 初始化、Messaging API 操作函數 |
| `src/line/webhook.js` | Webhook 接收器、事件分派、簽章驗證 |

### 2.3 事件處理常式

| 檔案路徑 | 說明 |
|----------|------|
| `src/line/handlers/messageHandler.js` | 訊息事件處理（文字、圖片、位置、貼圖） |
| `src/line/handlers/followHandler.js` | 關注事件處理（加入/封鎖官方帳號） |
| `src/line/handlers/postbackHandler.js` | 按鈕點擊事件處理（排隊、預約、確認等） |
| `src/line/handlers/leaveHandler.js` | 離開群組事件處理 |

### 2.4 訊息模板

| 檔案路徑 | 說明 |
|----------|------|
| `src/line/messages/flexMessages.js` | Flex Message 訊息模板工廠函數 |

### 2.5 LIFF 頁面

| 檔案路徑 | 說明 |
|----------|------|
| `src/liff/routes.js` | LIFF API 端點（排隊、預約、餐廳查詢） |
| `src/liff/sdk.js` | LIFF SDK 前端 JavaScript 封裝 |

### 2.6 餐廳端 API

| 檔案路徑 | 說明 |
|----------|------|
| `src/api/index.js` | Express 應用程式主體 |
| `src/api/restaurantApi.js` | 餐廳端 API（叫號、排隊管理、預約管理） |

---

## 三、LINE SDK 串接架構

### 3.1 LINE Messaging API 功能對應

```
LINE Platform
     │
     │ POST /webhook
     ▼
┌─────────────────────────────┐
│      Webhook 接收器         │
│  - 簽章驗證（X-LINE-Signature）
│  - 事件解析
│  - 快速回應 200 OK
└─────────────┬───────────────┘
              │
     ┌────────┴────────┐
     │  事件分派        │
     ├─────────────────┤
     │ follow/unfollow │ → followHandler
     │ message         │ → messageHandler
     │ postback        │ → postbackHandler
     │ beacon          │ → webhook.js
     │ join/leave      │ → leaveHandler
     └─────────────────┘
              │
              ▼
     ┌─────────────────┐
     │  LINE Client    │
     │  replyMessage() │
     │  pushMessage() │
     └─────────────────┘
              │
              ▼
     LINE 用戶端
```

### 3.2 LINE SDK 操作函數

| 函數 | 用途 | 使用的 API |
|------|------|-----------|
| `replyMessage()` | 回覆使用者訊息 | Reply API |
| `pushMessage()` | 主動推播訊息 | Push API |
| `multicast()` | 多人推播 | Multicast API |
| `getProfile()` | 取得使用者資料 | Profile API |
| `createRichMenu()` | 建立 Rich Menu | Rich Menu API |
| `linkRichMenuToUser()` | 連結 Rich Menu 給使用者 | Rich Menu API |

---

## 四、Webhook 處理架構

### 4.1 支援的事件類型

| 事件類型 | 觸發時機 | 處理模組 |
|----------|----------|----------|
| `follow` | 使用者加入官方帳號為好友 | followHandler.js |
| `unfollow` | 使用者封鎖或刪除官方帳號 | followHandler.js |
| `join` | Bot 被加入 Group/Room | leaveHandler.js |
| `leave` | Bot 被從 Group/Room 移除 | leaveHandler.js |
| `message` | 收到訊息 | messageHandler.js |
| `postback` | 點擊按鈕 | postbackHandler.js |
| `beacon` | 進入/離開 Beacon 範圍 | webhook.js |

### 4.2 簽章驗證機制

```javascript
// 驗證演算法
const crypto = require('crypto');

function verifySignature(body, signature, channelSecret) {
    const hash = crypto
        .createHmac('SHA256', channelSecret)
        .update(body)
        .digest('base64');

    return hash === signature;
}
```

**驗證流程：**
1. 取得 `X-LINE-Signature` header
2. 將 request body（原始 JSON 字串）進行 HMAC-SHA256 加密
3. 比對加密結果是否與 signature 一致
4. 驗證失敗回應 403 Forbidden

---

## 五、訊息處理架構

### 5.1 關鍵字自動回應

```javascript
const keywordActions = {
    '加入排隊': { action: 'showJoinQueue' },
    '排隊': { action: 'showJoinQueue' },
    '排隊中': { action: 'showQueueStatus' },
    '我的排隊': { action: 'showQueueStatus' },
    '預約': { action: 'showReservation' },
    '我的預約': { action: 'showMyReservation' },
    '取消排隊': { action: 'cancelQueue' },
    '取消預約': { action: 'cancelReservation' },
    '幫助': { action: 'showHelp' },
    '測試': { action: 'test' },
};
```

### 5.2 Flex Message 訊息模板

| 模板函數 | 用途 |
|----------|------|
| `createWelcomeFlex()` | 歡迎訊息 + 功能按鈕 |
| `createJoinQueueFlex()` | 加入排隊說明 |
| `createConfirmJoinQueueFlex()` | 確認加入排隊 |
| `createQueueJoinedFlex()` | 排隊成功通知 |
| `createQueueStatusFlex()` | 排隊進度查詢 |
| `createCalledFlex()` | 叫號通知 |
| `createConfirmCancelQueueFlex()` | 取消排隊確認 |
| `createReservationFlex()` | 線上預約說明 |
| `createReservationListFlex()` | 預約列表 |
| `createConfirmCancelReservationFlex()` | 取消預約確認 |
| `createHelpFlex()` | 幫助訊息 |
| `createPartySizeSelectionFlex()` | 人數選擇 |

---

## 六、Postback 動作架構

### 6.1 動作類型

```javascript
const PostbackActions = {
    JOIN_QUEUE: 'join_queue',
    SHOW_QUEUE_STATUS: 'show_queue_status',
    CANCEL_QUEUE: 'cancel_queue',
    BOOK_RESERVATION: 'book_reservation',
    SHOW_RESERVATION: 'show_reservation',
    CANCEL_RESERVATION: 'cancel_reservation',
    SELECT_RESTAURANT: 'select_restaurant',
    SELECT_PARTY_SIZE: 'select_party_size',
    CONFIRM_ACTION: 'confirm_action',
    CANCEL_ACTION: 'cancel_action',
};
```

### 6.2 動作資料格式

postback data 使用 URL-encoded 格式：
```
action=join_queue&restaurantId=xxx&partySize=2
```

確認動作使用 `actionType`：
```
actionType=confirm_join_queue&restaurantId=xxx&partySize=2
```

---

## 七、LIFF 頁面 API

### 7.1 API 端點

| Method | 端點 | 說明 |
|--------|------|------|
| GET | `/liff/info` | 取得 LIFF 頁面基本資訊 |
| GET | `/liff/queue/status` | 取得排隊狀態 |
| POST | `/liff/queue/join` | 加入排隊 |
| POST | `/liff/queue/cancel` | 取消排隊 |
| GET | `/liff/reservation/my` | 取得我的預約 |
| POST | `/liff/reservation/book` | 建立預約 |
| POST | `/liff/reservation/cancel` | 取消預約 |
| GET | `/liff/restaurants` | 取得餐廳列表 |
| GET | `/liff/restaurants/:id` | 取得特定餐廳與排隊狀態 |

### 7.2 驗證機制

LIFF API 使用 `liffAuth` 中介層驗證：
1. 從查詢參數或 body 取得 `userId`
2. 查詢消費者資料庫確認存在
3. 注入 `req.customer` 供後續處理

### 7.3 LIFF SDK 前端封裝

```javascript
// 初始化
const liff = await initLiff();

// 取得使用者資料
const profile = await liffApi.getProfile();

// 傳送訊息給 Bot
await liffApi.sendMessages([{ type: 'text', text: 'Hello!' }]);

// API 呼叫
const result = await queueApi.join(restaurantId, partySize);
```

---

## 八、餐廳端 API

### 8.1 叫號 API

| Method | 端點 | 說明 |
|--------|------|------|
| POST | `/api/queue/call-next` | 叫下一位 |
| POST | `/api/queue/call-specific` | 叫指定號碼 |
| POST | `/api/queue/mark-served` | 標記入座 |
| POST | `/api/queue/mark-no-show` | 標記過號 |
| POST | `/api/queue/cancel` | 取消排隊 |

### 8.2 排隊名單 API

| Method | 端點 | 說明 |
|--------|------|------|
| GET | `/api/queue/list/:restaurantId` | 取得排隊名單 |
| GET | `/api/queue/stats/:restaurantId` | 取得排隊統計 |

### 8.3 預約管理 API

| Method | 端點 | 說明 |
|--------|------|------|
| GET | `/api/reservations/:restaurantId` | 取得預約列表 |
| POST | `/api/reservations/mark-seated` | 標記已入座 |
| POST | `/api/reservations/mark-no-show` | 標記過號 |

### 8.4 通知 API

| Method | 端點 | 說明 |
|--------|------|------|
| GET | `/api/notifications/:restaurantId` | 取得通知歷史 |

---

## 九、環境變數設定

### 9.1 必要環境變數

```bash
# LINE Messaging API
LINE_CHANNEL_ID=your_line_channel_id
LINE_CHANNEL_SECRET=your_line_channel_secret
LINE_ACCESS_TOKEN=your_line_access_token

# LIFF App IDs
LIFF_JOIN_QUEUE_ID=your_liff_id_1
LIFF_MY_QUEUE_ID=your_liff_id_2
LIFF_BOOK_RESERVATION_ID=your_liff_id_3
LIFF_MY_RESERVATION_ID=your_liff_id_4

# LIFF 頁面基礎 URL
LIFF_BASE_URL=https://your-domain.com
```

### 9.2 LINE Developers Console 設定

1. **Webhook URL:** `https://your-domain.com/webhook`
2. **Auto-reply:** 關閉（由程式碼控制）
3. **LIFF:** 設定 4 個 LIFF App（加入排隊、排隊狀態、預約、我的預約）
4. **Rich Menu:** 設定對應按鈕連結至 LIFF 頁面

---

## 十、Express 應用程式架構

```
src/api/index.js (主入口)
├── webhookRouter (LINE Webhook)
├── liffRouter (LIFF API)
├── restaurantApiRouter (餐廳端 API)
└── health check
```

**路由對應：**
- `POST /webhook` → LINE Webhook 接收
- `GET /webhook` → Webhook 驗證
- `/liff/*` → LIFF API
- `/api/queue/*` → 餐廳端叫號 API
- `/api/reservations/*` → 餐廳端預約 API
- `/api/notifications/*` → 通知記錄 API
- `GET /health` → 健康檢查

---

## 十一、Phase 3 完成狀態

### LINE Messaging API 串接
- ✅ @line/bot-sdk Node.js SDK 設定
- ✅ Webhook 接收與處理
- ✅ Reply API / Push API 使用
- ✅ 簽章驗證機制

### LINE LIFF 串接
- ✅ LIFF SDK 初始化函數
- ✅ 登入驗證流程
- ✅ 傳訊息給 Bot（liff.sendMessages）
- ✅ 取得使用者 LINE ID

### 機器人功能實作
- ✅ 關鍵字自動回應（加入排隊、查看進度、預約）
- ✅ Flex Message 訊息模板（排隊確認、叫號通知）
- ✅ Postback 按鈕處理

### Webhook 處理常式
- ✅ follow/unfollow 事件
- ✅ message 事件（文字訊息）
- ✅ postback 事件（按鈕點擊）
- ✅ beacon 事件（框架預留）

### LINE 通知功能
- ✅ 叫號推播
- ✅ 排隊進度通知
- ✅ 預約確認通知

---

## 十二、已知限制

| 項目 | 說明 | 建議改進 |
|------|------|----------|
| 無 LIFF 頁面前端 | 目前只有 API，無實際 HTML 頁面 | Phase 4 實作 Vue/React 前端 |
| 無 Rich Menu API 設定 | 只有設定檔，無實際建立 | 需手動在 LINE Console 設定 |
| 無 LINE Login 驗證 | 使用 userId 簡單驗證 | 可升級為 LINE Login OAuth |
| 無訊息派發（dispatch） | 目前使用 replyMessage | 叫號後需派發至正確餐廳的 webhook |

---

## 十三、下一步（Phase 4 建議）

Phase 3 完成後，建議進入以下項目：

1. **LIFF 前端頁面實作**
   - Vue 3 或 React 框架設定
   - 加入排隊表單頁面
   - 排隊進度查詢頁面
   - 線上預約表單頁面

2. **餐廳管理後台實作**
   - React + Vite 前端框架
   - 排隊名單即時顯示
   - 叫號操作介面
   - 預約管理介面

3. **Redis 串接**
   - 排隊名單快取
   - Pub/Sub 即時通知（叫號更新）
   - 工作階段管理

4. **通知系統優化**
   - 排隊進度主動推播
   - 過號提醒
   - 即將到時催單

5. **LINE 官方設定**
   - Rich Menu 設定與绑定
   - 歡迎訊息設定
   - 自動回應訊息設定

---

## 十四、檔案總覽

```
line_queue/
├── config/
│   └── line.js                  # LINE 設定集中管理
├── src/
│   ├── api/
│   │   ├── index.js             # Express 主體
│   │   └── restaurantApi.js     # 餐廳端 API
│   ├── db/
│   │   └── connection.js        # 資料庫連線
│   ├── line/
│   │   ├── client.js            # LINE SDK 客戶端
│   │   ├── webhook.js           # Webhook 接收器
│   │   ├── handlers/
│   │   │   ├── messageHandler.js
│   │   │   ├── followHandler.js
│   │   │   ├── postbackHandler.js
│   │   │   └── leaveHandler.js
│   │   └── messages/
│   │       └── flexMessages.js  # Flex Message 模板
│   ├── liff/
│   │   ├── routes.js            # LIFF API 端點
│   │   └── sdk.js              # LIFF SDK 前端封裝
│   └── repositories/           # （Phase 2 已完成）
│       ├── index.js
│       ├── restaurantRepository.js
│       ├── customerRepository.js
│       ├── queueRepository.js
│       ├── reservationRepository.js
│       └── notificationRepository.js
├── sql/                        # （Phase 2 已完成）
├── docker-compose.yml          # （Phase 2 已完成）
├── .env.example                # （已更新）
└── scripts/
    └── init-db.sh              # （Phase 2 已完成）
```

---

## 十五、安裝與啟動方式

### 前置需求
- Node.js 18+
- Docker & Docker Compose
- LINE Channel（已申請 Messaging API）

### 安裝步驟

```bash
# 1. 安裝 npm 依賴
cd /root/.openclaw/workspace/line_queue
npm install

# 2. 複製並設定環境變數
cp .env.example .env
# 編輯 .env 填入 LINE Channel 設定

# 3. 啟動資料庫
docker-compose up -d

# 4. 執行資料庫 Migration
docker exec -it line_queue_postgres psql -U postgres -d line_queue -f /docker-entrypoint-initdb.d/001_initial_schema.sql

# 5. 啟動伺服器
npm start
```

### 測試 LINE 功能

```bash
# 啟動開發伺服器
npm run dev

# 測試 Webhook 端點
curl -X POST http://localhost:3000/webhook \
  -H "Content-Type: application/json" \
  -d '{"events":[]}'

# 測試健康檢查
curl http://localhost:3000/health
```

---

**文件結尾**

Phase 3 LINE API 串接工作已全部完成。所有 LINE SDK、Webhook 處理、訊息模板、LIFF API、以及餐廳端 API 均已就緒，可供後續 Phase 4（LIFF 前端頁面與餐廳管理後台開發）使用。

---
*小咪技術研發助理｜2026-05-13*