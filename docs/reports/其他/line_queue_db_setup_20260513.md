# LINE 餐廳候補位系統 - Phase 2 資料庫建置報告

**文件版本：** 1.0  
**日期：** 2026-05-13  
**作者：** 小咪技術研發助理  
**適用時區：** Asia/Taipei (GMT+8)

---

## 一、任務概述

Phase 2 完成了 LINE 餐廳候補位系統的資料庫建置工作，包含 Schema 設計、Migration 腳本、Seed Data、Repository 層以及 Docker 環境設定。

---

## 二、產出檔案清單

### 2.1 SQL 檔案

| 檔案路徑 | 說明 |
|----------|------|
| `sql/001_initial_schema.sql` | 初始 Schema Migration |
| `sql/001_initial_schema_down.sql` | Migration 復原腳本 |
| `sql/002_seed_data.sql` | 測試資料 Seed Data |

### 2.2 程式碼

| 檔案路徑 | 說明 |
|----------|------|
| `src/db/connection.js` | PostgreSQL 連線設定與連線池管理 |
| `src/repositories/index.js` | Repository 匯出索引 |
| `src/repositories/restaurantRepository.js` | 餐廳 CRUD Repository |
| `src/repositories/customerRepository.js` | 消費者 CRUD Repository |
| `src/repositories/queueRepository.js` | 排隊 CRUD + 叫號邏輯 Repository |
| `src/repositories/reservationRepository.js` | 預約 CRUD Repository |
| `src/repositories/notificationRepository.js` | 通知記錄 CRUD Repository |

### 2.3 Docker 與設定

| 檔案路徑 | 說明 |
|----------|------|
| `docker-compose.yml` | PostgreSQL + Redis 容器設定 |
| `scripts/init-db.sh` | 資料庫初始化腳本 |
| `.env.example` | 環境變數範例 |

---

## 三、資料庫 Schema 設計

### 3.1 資料表結構

| 資料表 | 主鍵 | 說明 |
|--------|------|------|
| `restaurants` | UUID | 餐廳基本資料 |
| `customers` | UUID | 消費者資料 |
| `queue_entries` | UUID | 排隊資料 |
| `reservations` | UUID | 預約資料 |
| `notification_logs` | UUID | 通知記錄 |
| `schema_migrations` | VARCHAR | 版本記錄 |

### 3.2 Index 設計

| Index 名稱 | 資料表 | 用途 |
|------------|--------|------|
| `idx_queue_entries_restaurant_status` | queue_entries | 依餐廳查詢排隊名單 |
| `idx_queue_entries_restaurant_queue_number` | queue_entries | 排隊號碼排序 |
| `idx_queue_entries_customer` | queue_entries | 消費者排隊歷史 |
| `idx_queue_entries_joined_at` | queue_entries | 時間排序 |
| `idx_reservations_restaurant_date` | reservations | 特定日期預約查詢 |
| `idx_reservations_customer` | reservations | 消費者預約歷史 |
| `idx_notification_logs_restaurant` | notification_logs | 餐廳通知歷史 |
| `idx_notification_logs_customer` | notification_logs | 消費者通知歷史 |
| `idx_notification_logs_sent_at` | notification_logs | 時間排序 |

### 3.3 特殊功能

- **自動更新觸發器**：`update_restaurants_updated_at` — 自動更新 `updated_at` 欄位
- **取得下一個排隊號碼函數**：`get_next_queue_number(p_restaurant_id UUID)` — 計算下一個可用排隊號碼
- **ENUM 型別**：`queue_status`、`queue_source`、`reservation_status`、`notification_type`、`notification_status`

---

## 四、Repository 層設計

### 4.1 RestaurantRepository

| 函數 | 說明 |
|------|------|
| `createRestaurant(data)` | 建立餐廳 |
| `getRestaurantById(id)` | 依 ID 取得餐廳 |
| `getRestaurantByLineChannelId(lineChannelId)` | 依 LINE Channel ID 取得餐廳 |
| `getAllRestaurants()` | 取得所有餐廳 |
| `updateRestaurant(id, data)` | 更新餐廳資料 |
| `deleteRestaurant(id)` | 刪除餐廳 |
| `getQueueCount(restaurantId)` | 取得目前排隊人數 |

### 4.2 CustomerRepository

| 函數 | 說明 |
|------|------|
| `createCustomer(data)` | 建立消費者 |
| `getCustomerById(id)` | 依 ID 取得消費者 |
| `getCustomerByLineUserId(lineUserId)` | 依 LINE User ID 取得消費者 |
| `getAllCustomers()` | 取得所有消費者 |
| `updateCustomer(id, data)` | 更新消費者資料 |
| `getCustomerQueueHistory(customerId, limit)` | 取得排隊歷史 |
| `getCustomerReservationHistory(customerId, limit)` | 取得預約歷史 |

### 4.3 QueueRepository

| 函數 | 說明 |
|------|------|
| `joinQueue(data)` | 加入排隊 |
| `getQueueEntryById(id)` | 依 ID 取得排隊資料 |
| `getQueueListByRestaurant(restaurantId, status)` | 依餐廳取得排隊名單 |
| `callNext(restaurantId)` | 叫下一位 |
| `callSpecific(restaurantId, queueNumber)` | 手動叫指定號碼 |
| `markAsServed(queueEntryId)` | 標記入座 |
| `cancelQueue(queueEntryId)` | 取消排隊 |
| `markAsNoShow(queueEntryId)` | 標記過號 |
| `getWaitingCount(restaurantId)` | 取得等候人數 |
| `getCustomerQueuePosition(customerId, restaurantId)` | 取得排隊順位 |

### 4.4 ReservationRepository

| 函數 | 說明 |
|------|------|
| `createReservation(data)` | 建立預約 |
| `getReservationById(id)` | 依 ID 取得預約 |
| `getReservationsByRestaurantAndDate(restaurantId, date)` | 依餐廳和日期取得預約 |
| `getReservationsByCustomer(customerId)` | 依消費者取得預約 |
| `getUpcomingReservations(customerId)` | 取得即將到來的預約 |
| `updateReservation(id, data)` | 更新預約 |
| `cancelReservation(id)` | 取消預約 |
| `markAsSeated(id)` | 標記已入座 |
| `markAsNoShow(id)` | 標記過號 |

### 4.5 NotificationRepository

| 函數 | 說明 |
|------|------|
| `createNotification(data)` | 建立通知記錄 |
| `getNotificationById(id)` | 依 ID 取得通知 |
| `getNotificationsByRestaurant(restaurantId, limit)` | 依餐廳取得通知歷史 |
| `getNotificationsByCustomer(customerId, limit)` | 依消費者取得通知歷史 |
| `updateNotificationStatus(lineMessageId, status)` | 更新通知狀態 |
| `getNotificationsByType(restaurantId, type, limit)` | 依類型取得通知 |
| `getFailedNotifications(restaurantId, limit)` | 取得發送失敗的通知 |
| `getNotificationStats(restaurantId, start, end)` | 通知統計 |

---

## 五、Docker Compose 設定

### 5.1 服務架構

```
postgres (PostgreSQL 16-alpine)
    ├── Port: 5432
    ├── Volume: postgres_data
    └── Init SQL: ./sql/*.sql

redis (Redis 7-alpine)
    ├── Port: 6379
    └── Volume: redis_data

pgadmin (pgAdmin4)
    ├── Port: 5050
    └── 選用開啟
```

### 5.2 啟動方式

```bash
cd /root/.openclaw/workspace/line_queue
docker-compose up -d
```

### 5.3 初始化選項

```bash
# 僅建立資料庫結構
docker-compose up -d

# 建立資料庫並載入測試資料
LOAD_SEED_DATA=true docker-compose up -d
```

---

## 六、Seed Data 內容

### 6.1 餐廳（3 家）

| 名稱 | 座位數 | 平均用餐時長 | 排隊上限 |
|------|--------|--------------|----------|
| 巷口牛肉麵 | 40 | 45 分鐘 | 30 |
| 幸福小館 | 25 | 60 分鐘 | 20 |
| 川味麻辣鍋 | 60 | 90 分鐘 | 40 |

### 6.2 消費者（12 位）

LINE User ID 格式：`U00XAAAAAAAAAAAAAAAA`

### 6.3 排隊情境模擬

- **巷口牛肉麵**：7 組排隊（5 waiting + 1 called + 1 served）
- **幸福小館**：3 組排隊
- **川味麻辣鍋**：5 組排隊（高朋滿座）

### 6.4 預約情境模擬

- **巷口牛肉麵**：3 筆預約（未來 1-2 天）
- **幸福小館**：2 筆預約
- **川味麻辣鍋**：3 筆預約

### 6.5 通知記錄情境

- 4 筆叫號通知（已送達）
- 2 筆預約確認通知（已發送）

---

## 七、本地開發使用方式

### 7.1 啟動資料庫

```bash
cd /root/.openclaw/workspace/line_queue
docker-compose up -d

# 等待啟動完成後執行 Migration
docker exec -it line_queue_postgres psql -U postgres -d line_queue -f /docker-entrypoint-initdb.d/001_initial_schema.sql

# 選擇性：載入測試資料
docker exec -it line_queue_postgres psql -U postgres -d line_queue -f /docker-entrypoint-initdb.d/002_seed_data.sql
```

### 7.2 設定環境變數

```bash
cp .env.example .env
# 編輯 .env 填入實際值
```

### 7.3 測試連線

```javascript
// 在 Node.js 中
const { testConnection } = require('./src/db/connection');

async function main() {
    const connected = await testConnection();
    if (connected) {
        console.log('可以開始使用資料庫了！');
    }
}

main();
```

---

## 八、下一步（Phase 3 建議）

Phase 2 完成後，建議進入以下項目：

1. **LINE Messaging API Service 實作**
   - Webhook 接收器
   - 訊息處理邏輯
   - Push API 發送通知

2. **餐廳管理後台基本框架**
   - Express 基礎架構
   - 餐廳登入/驗證系統
   - 排隊名單管理 API

3. **LIFF 頁面基本框架**
   - Vue 3 或 React 設定
   - LINE LIFF SDK 串接
   - 加入排隊表單頁面

4. **Redis 串接**
   - 排隊名單快取
   - Pub/Sub 即時通知

---

## 九、已知限制與改進建議

| 項目 | 說明 | 改進建議 |
|------|------|----------|
| Seed Data 的 queue_entry ID 有錯誤 | 初期版本有 ID 欄位對應問題（已修正） | 建議增加資料驗證腳本 |
| 無法跨資料庫交易 | 目前設計為單一資料庫 | 未來如有需要可考慮分散式交易 |
| 無敏感資料加密 | line_channel_secret 等以明文儲存 | 生產環境應使用加密或 Secret Manager |
| 無備份機制 | 目前無備份腳本 | 建議加入 pg_dump 備份機制 |

---

## 十、檔案總覽

```
line_queue/
├── docker-compose.yml          # Docker Compose 設定
├── .env.example               # 環境變數範例
├── sql/
│   ├── 001_initial_schema.sql     # Migration
│   ├── 001_initial_schema_down.sql # Migration 復原
│   └── 002_seed_data.sql          # 測試資料
├── src/
│   ├── db/
│   │   └── connection.js          # 資料庫連線設定
│   └── repositories/
│       ├── index.js               # 匯出索引
│       ├── restaurantRepository.js
│       ├── customerRepository.js
│       ├── queueRepository.js
│       ├── reservationRepository.js
│       └── notificationRepository.js
└── scripts/
    └── init-db.sh                # 資料庫初始化腳本
```

---

**文件結尾**

Phase 2 資料庫建置工作已全部完成。所有 SQL 檔案、Repository 層程式碼、以及 Docker 環境設定均已就緒，可供後續 Phase 3（LINE API 串接與餐廳後台開發）使用。

---
*小咪技術研發助理｜2026-05-13*