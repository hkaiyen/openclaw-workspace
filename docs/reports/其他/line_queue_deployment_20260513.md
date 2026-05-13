# LINE 餐廳候補位系統 MVP 開發完成報告

## 版本資訊
- **系統版本：** 1.0.0
- **发布日期：** 2026-05-13
- **時區：** Asia/Taipei (GMT+8)
- **作者：** 小咪技術研發助理

---

## 📋 執行摘要

LINE 餐廳候補位系統 MVP 已完成所有開發階段。本系統幫助餐廳管理現場候位，消費者可透過 LINE 預約候補位，大幅提升餐廳排隊管理效率與消費者體驗。

### 完成階段

| 階段 | 內容 | 狀態 |
|------|------|------|
| 第一階段 | 系統架構設計與資料庫規劃 | ✅ 完成 |
| 第二階段 | LINE 機器人與 Webhook 處理 | ✅ 完成 |
| 第三階段 | LIFF 頁面開發 | ✅ 完成 |
| 第四階段 | 管理後台開發 | ✅ 完成 |
| 第五階段 | 系統測試與部署 | ✅ 完成 |

---

## 🏗️ 系統架構

### 系統架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                        LINE Platform                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   LIFF      │  │  Messaging  │  │   Rich      │         │
│  │   Pages     │  │     API     │  │   Menu      │         │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘         │
└─────────┼─────────────────┼──────────────────────────────────┘
          │                 │
          ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      Your Server                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Express   │  │   LINE     │  │  Database   │         │
│  │   App       │  │   Bot SDK   │  │  PostgreSQL │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 技術堆疊

| 層級 | 技術 | 版本 |
|------|------|------|
| 前端 | HTML5, CSS3, JavaScript | - |
| 後端 | Node.js, Express | 18.x |
| 資料庫 | PostgreSQL | 16.x |
| 快取 | Redis | 7.x（可選） |
| LINE 整合 | @line/bot-sdk | 最新版本 |
| 容器化 | Docker, Docker Compose | 20.x+ |

---

## 📁 專案結構

```
line_queue/
├── config/                 # 設定檔
│   └── line.js           # LINE 設定
├── docs/                  # 文件
│   ├── DEPLOYMENT.md     # 部署指南
│   └── LINE_SETUP.md     # LINE 申請教學
├── public/                # 靜態檔案
│   ├── admin/           # 管理後台
│   │   └── index.html   # 管理後台主頁面
│   └── liff/            # LIFF 頁面
│       ├── queue/       # 排隊相關頁面
│       │   ├── join.html    # 加入排隊
│       │   └── status.html  # 排隊狀態
│       └── reservation/ # 預約相關頁面
│           ├── book.html    # 預約
│           └── my.html     # 我的預約
├── scripts/               # 工具腳本
│   ├── init-db.sh       # 資料庫初始化
│   ├── test-api.sh      # API 測試腳本
│   └── test-line.sh     # LINE 整合測試腳本
├── sql/                   # SQL 資料庫脚本
│   ├── 001_initial_schema.sql  # 初始資料庫結構
│   ├── 002_seed_data.sql       # 範例資料
│   └── 001_initial_schema_down.sql  # Rollback 脚本
├── src/                   # 應用程式原始碼
│   ├── api/             # API 路由
│   │   └── restaurantApi.js
│   ├── db/              # 資料庫連線
│   │   └── connection.js
│   ├── liff/            # LIFF 路由
│   │   ├── routes.js
│   │   └── sdk.js
│   ├── line/            # LINE 機器人
│   │   ├── client.js     # LINE Client
│   │   ├── webhook.js    # Webhook 處理
│   │   ├── handlers/     # 事件處理器
│   │   │   ├── messageHandler.js   # 訊息處理
│   │   │   ├── followHandler.js     #  follow 處理
│   │   │   ├── leaveHandler.js     #  leave 處理
│   │   │   └── postbackHandler.js  #  postback 處理
│   │   └── messages/     # 訊息範本
│   │       └── flexMessages.js  # Flex Message 範本
│   ├── repositories/    # 資料存取層
│   │   ├── customerRepository.js
│   │   ├── notificationRepository.js
│   │   ├── queueRepository.js
│   │   ├── reservationRepository.js
│   │   └── restaurantRepository.js
│   ├── services/        # 商業邏輯層
│   │   ├── notificationService.js
│   │   ├── queueService.js
│   │   └── reservationService.js
│   └── routes/
│       └── index.js     # 主路由整合
├── docker-compose.yml    # Docker Compose 設定
├── .env.example          # 環境變數範例
└── README.md             # 專案說明文件
```

---

## 📊 資料庫結構

### 資料表設計

#### 1. restaurants（餐廳資料表）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| name | VARCHAR(100) | 餐廳名稱 |
| line_channel_id | VARCHAR(100) | LINE Channel ID |
| line_channel_secret | VARCHAR(255) | LINE Channel Secret |
| line_access_token | TEXT | LINE Access Token |
| address | VARCHAR(200) | 地址 |
| phone | VARCHAR(20) | 電話 |
| total_seats | INT | 總座位數 |
| avg_meal_duration_minutes | INT | 平均用餐時長（分鐘） |
| queue_max_size | INT | 排隊人數上限 |
| auto_call_enabled | BOOLEAN | 是否啟用自動叫號 |
| created_at | TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | 更新時間 |

#### 2. customers（消費者資料表）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| line_user_id | VARCHAR(100) | LINE User ID |
| display_name | VARCHAR(100) | 顯示名稱 |
| phone | VARCHAR(20) | 電話 |
| created_at | TIMESTAMP | 建立時間 |

#### 3. queue_entries（排隊資料表）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| restaurant_id | UUID | 餐廳 ID |
| customer_id | UUID | 消費者 ID |
| queue_number | INT | 排隊號碼 |
| status | ENUM | 狀態（waiting/called/served/cancelled/no_show） |
| party_size | INT | 用餐人數 |
| joined_at | TIMESTAMP | 加入時間 |
| called_at | TIMESTAMP | 叫號時間 |
| served_at | TIMESTAMP | 入座時間 |
| notes | TEXT | 備註 |
| source | ENUM | 來源（walk_in/reservation/waitlist） |

#### 4. reservations（預約資料表）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| restaurant_id | UUID | 餐廳 ID |
| customer_id | UUID | 消費者 ID |
| reservation_date | DATE | 預約日期 |
| reservation_time | TIME | 預約時間 |
| party_size | INT | 用餐人數 |
| status | ENUM | 狀態（confirmed/seated/cancelled/no_show） |
| created_at | TIMESTAMP | 建立時間 |
| notes | TEXT | 備註 |

#### 5. notification_logs（通知記錄資料表）
| 欄位 | 類型 | 說明 |
|------|------|------|
| id | UUID | 主鍵 |
| restaurant_id | UUID | 餐廳 ID |
| customer_id | UUID | 消費者 ID |
| queue_entry_id | UUID | 排隊 ID |
| notification_type | ENUM | 類型 |
| line_message_id | VARCHAR(100) | LINE 訊息 ID |
| sent_at | TIMESTAMP | 發送時間 |
| status | ENUM | 狀態（sent/delivered/failed） |

---

## 🐳 Docker 部署

### Docker Compose 設定

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: line_queue_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: line_queue
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: line_queue_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: line_queue_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@linequeue.local
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    depends_on:
      - postgres

volumes:
  postgres_data:
  redis_data:
```

---

## 📡 API 端點

### 排隊 API

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/queue/list/:restaurantId` | 取得排隊名單 |
| GET | `/api/queue/stats/:restaurantId` | 取得排隊統計 |
| POST | `/api/queue/call-next` | 叫下一位 |
| POST | `/api/queue/call-specific` | 叫指定號碼 |
| POST | `/api/queue/mark-served` | 標記入座 |
| POST | `/api/queue/mark-no-show` | 標記過號 |

### 預約 API

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/reservations/:restaurantId` | 取得預約列表 |
| POST | `/api/reservations/mark-seated` | 標記已入座 |
| POST | `/api/reservations/mark-no-show` | 標記過號 |

### 通知 API

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/api/notifications/:restaurantId` | 取得通知歷史 |

### 頁面路由

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/liff/queue/join` | 加入排隊頁面 |
| GET | `/liff/queue/status` | 排隊狀態頁面 |
| GET | `/liff/reservation/book` | 預約頁面 |
| GET | `/liff/reservation/my` | 我的預約頁面 |
| GET | `/admin` | 餐廳管理後台 |

---

## 📱 LINE 功能整合

### LINE Messaging API

- ✅ 接收 Webhook 事件（follow, message, postback, beacon）
- ✅ 發送 Push 訊息
- ✅ Flex Message 訊息範本
- ✅ 簽章驗證

### LINE LIFF

- ✅ 加入排隊 LIFF 頁面
- ✅ 排隊狀態 LIFF 頁面
- ✅ 預約 LIFF 頁面
- ✅ 我的預約 LIFF 頁面

### LINE Rich Menu（需另行設定）

- 建議設計：首頁、排隊、預約、幫助

---

## 🔧 開發階段回顧

### 第一階段：系統架構設計
- 定義系統需求與功能
- 設計資料庫結構
- 建立 SQL Migration 脚本

### 第二階段：LINE 機器人開發
- 設定 LINE Messaging API
- 實作 Webhook 處理
- 實作訊息處理器
- 實作 Flex Message 範本

### 第三階段：LIFF 頁面開發
- 實作加入排隊頁面
- 實作排隊狀態頁面
- 實作預約頁面
- 實作我的預約頁面

### 第四階段：管理後台開發
- 實作管理後台首頁
- 實作排隊名單管理
- 實作叫號功能
- 實作預約管理

### 第五階段：測試與部署
- 實作 API 測試腳本
- 實作 LINE 整合測試腳本
- 編寫部署指南
- 編寫 LINE 申請教學
- 建立 Docker 部署環境

---

## 🚀 部署檢查清單

### 部署前檢查
- [ ] Node.js 18.x 已安裝
- [ ] PostgreSQL 16.x 已安裝
- [ ] LINE Channel 已建立
- [ ] LIFF 應用已設定
- [ ] 環境變數已正確設定
- [ ] SSL 憑證已設定（生產環境）

### 部署步驟
1. 複製專案到伺服器
2. 安裝相依套件：`npm install`
3. 設定環境變數：複製 `.env.example` 為 `.env`
4. 初始化資料庫：`psql -U postgres -d line_queue -f sql/001_initial_schema.sql`
5. 啟動服務：`npm start` 或使用 PM2/Docker

### 部署後檢查
- [ ] 服務正常啟動（`curl http://localhost:3000/`）
- [ ] Webhook 端點正常（`curl http://localhost:3000/webhook`）
- [ ] LIFF 頁面可正常存取
- [ ] 資料庫連線正常
- [ ] LINE Webhook 驗證成功

---

## 📚 文件總覽

| 文件 | 說明 |
|------|------|
| README.md | 專案說明文件 |
| docs/DEPLOYMENT.md | 詳細部署指南 |
| docs/LINE_SETUP.md | LINE 官方帳號申請教學 |
| scripts/test-api.sh | API 測試腳本 |
| scripts/test-line.sh | LINE 整合測試腳本 |
| sql/001_initial_schema.sql | 資料庫結構 |
| sql/002_seed_data.sql | 範例資料 |

---

## 📝 測試腳本使用說明

### API 測試

```bash
# 進入專案目錄
cd /root/.openclaw/workspace/line_queue

# 賦予執行權限
chmod +x scripts/test-api.sh

# 執行所有測試
./scripts/test-api.sh --all

# 僅測試排隊 API
./scripts/test-api.sh --queue

# 僅測試預約 API
./scripts/test-api.sh --reservation

# 僅測試 LIFF 頁面
./scripts/test-api.sh --liff

# 僅測試資料庫
./scripts/test-api.sh --db
```

### LINE 整合測試

```bash
# 賦予執行權限
chmod +x scripts/test-line.sh

# 執行所有 LINE 測試
./scripts/test-line.sh --all

# 僅測試 Messaging API
./scripts/test-line.sh --messaging

# 僅測試 LIFF
./scripts/test-line.sh --liff

# 顯示 ngrok 設定說明
./scripts/test-line.sh --ngrok
```

---

## 🎯 系統功能總覽

### 消費者功能
| 功能 | 說明 | 觸發方式 |
|------|------|----------|
| 加入排隊 | 選擇餐廳、填寫姓名人數 | LINE 訊息「排隊」或 LIFF |
| 取消排隊 | 取消尚未被叫到的排隊 | LINE 訊息「取消」 |
| 查詢排隊狀態 | 查看排隊號碼和等候人數 | LINE 訊息「狀態」或 LIFF |
| 線上預約 | 預約指定日期和時段 | LINE 訊息「預約」或 LIFF |
| 查看預約 | 查看已預約的資料 | LIFF 頁面 |

### 餐廳管理功能
| 功能 | 說明 | 觸發方式 |
|------|------|----------|
| 叫下一位 | 叫第一位消費者 | 管理後台按鈕 |
| 叫指定號碼 | 叫特定排隊號碼 | 管理後台輸入 |
| 標記入座 | 標記消費者已入座 | 管理後台按鈕 |
| 標記過號 | 標記消費者未到場 | 管理後台按鈕 |
| 查看排隊名單 | 查看所有排隊資料 | 管理後台頁面 |
| 查看預約列表 | 查看所有預約 | 管理後台頁面 |

### LINE 機器人自動回應
| 關鍵字 | 回應 |
|--------|------|
| 「排隊」、「join」 | 引導加入排隊 |
| 「預約」、「reservation」 | 引導進行預約 |
| 「取消」、「cancel」 | 引導取消排隊/預約 |
| 「狀態」、「status」 | 查詢排隊/預約狀態 |
| 「幫助」、「help」 | 顯示幫助資訊 |

---

## 🔒 安全考量

1. **LINE Channel Secret 保護**
   - 不要將 Secret  commit 到版控
   - 使用環境變數管理
   - 生產環境使用 secrets 管理工具

2. **Webhook 簽章驗證**
   - 生產環境啟用簽章驗證
   - 驗證每個 incoming 請求

3. **資料庫權限**
   - 遵循最小權限原則
   - 不要使用 root 帳號

4. **HTTPS 強制**
   - 生產環境必須使用 HTTPS
   - 使用 Let's Encrypt 或 Cloudflare

---

## 📈 未來擴展方向

### 短期擴展
- 整合更多 LINE 功能（LIFF QR Code）
- 支援多語言
- 強化統計報表功能

### 中期擴展
- 會員系統整合
- 優惠券/集點功能
- 評論/回饋功能

### 長期擴展
- 跨店連鎖管理
- AI 預測排隊時間
- 電子支付整合

---

## ❓ 疑難排解

### 常見問題

**Q: Webhook 驗證失敗**
- 確認使用 HTTPS
- 確認 SSL 憑證有效
- 確認 LINE Channel Secret 正確

**Q: LIFF 頁面無法載入**
- 確認 LIFF Endpoint URL 正確
- 確認 LINE LIFF SDK 已正確引入

**Q: 資料庫連線失敗**
- 確認 PostgreSQL 已啟動
- 確認環境變數正確
- 檢查連線帳號權限

**Q: 無法發送 LINE 訊息**
- 確認 Access Token 有效
- 確認 LINE User ID 格式正確

---

## 📄 部署文件

完整的部署說明請參考：
- [部署指南](./docs/DEPLOYMENT.md)
- [LINE 申請教學](./docs/LINE_SETUP.md)

---

## ✅ 結論

LINE 餐廳候補位系統 MVP 已完成所有開發工作。系統提供完整的排隊管理、預約管理、以及 LINE 機器人整合功能。管理人員可通過管理後台輕鬆管理排隊和預約，消費者可通過 LINE 享受流暢的排隊和預約體驗。

所有必要的文件和測試腳本都已準備完成，部署人員可根據 `docs/DEPLOYMENT.md` 的指引進行系統部署。

---

## 📞 技術支援

- **負責人：** 小咪技術研發助理
- **系統版本：** 1.0.0
- **发布日期：** 2026-05-13
- **時區：** Asia/Taipei (GMT+8)

---

**（本報告已儲存於 `/root/.openclaw/reports/daily/line_queue_deployment_20260513.md`）**