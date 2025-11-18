# 股票營收觀察工具 (Stock Revenue Tracking Tool)

台股營收追蹤工具，支援追蹤 200–300 檔股票，使用 FastAPI 後端與 Next.js 前端。

## 功能特點

- 📊 追蹤上個月、上上個月、上一季營收及 YoY 成長率
- 💹 顯示當前股價與漲跌幅（實時緩存）
- 📱 響應式設計（桌面版表格 + 手機版卡片）
- 🗄️ SQLite 資料庫持久化
- ⚡ WAL 模式提升併發效能
- 🔄 SWR 前端資料快取與自動重整

## 技術架構

### 後端 (Backend)
- **框架**: FastAPI + Uvicorn
- **資料庫**: SQLite with WAL mode
- **ORM**: SQLAlchemy
- **語言**: Python 3.10+

### 前端 (Frontend)
- **框架**: Next.js 16 (App Router)
- **語言**: TypeScript
- **UI**: Tailwind CSS
- **資料獲取**: SWR + Axios

## 快速開始

### 後端設定

1. 安裝依賴：
```bash
cd backend
pip install -r requirements.txt
```

2. 設定環境變數（複製 .env.example）：
```bash
cp .env.example .env
```

3. 匯入初始資料：
```bash
python app/scripts/import_fixtures.py
```

4. 啟動服務器：
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API 文檔將在 http://localhost:8000/docs 提供

### 前端設定

1. 安裝依賴：
```bash
cd frontend
npm install
```

2. 設定環境變數：
```bash
# 複製範例檔案
cp .env.local.example .env.local

# 編輯 .env.local 設定後端 API URL
# 本地開發: NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
# Codespaces: 使用轉發的端口 URL（見下方說明）
```

3. 啟動開發服務器：
```bash
npm run dev
```

應用將在 http://localhost:3000 運行

### 🚀 在 GitHub Codespaces 中運行

如果您在 Codespaces 中運行，需要特別設定：

1. **啟動後端**（在終端機 1）：
```bash
cd backend
pip install -r requirements.txt
python app/scripts/import_fixtures.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **取得後端 URL**：
   - 當後端啟動後，Codespaces 會自動轉發 port 8000
   - 點擊 VS Code 底部的 "PORTS" 標籤
   - 找到 port 8000，複製其轉發的 URL（類似：`https://username-repo-abc123-8000.app.github.dev`）

3. **設定前端**（在終端機 2）：
```bash
cd frontend
npm install

# 建立 .env.local 並設定後端 URL
echo "NEXT_PUBLIC_API_BASE_URL=<貼上剛才複製的 URL>" > .env.local

npm run dev
```

4. **訪問應用**：
   - 前端會在 port 3000 啟動
   - 在 "PORTS" 標籤中找到 port 3000，點擊開啟瀏覽器

**重要提示**：每次 Codespace 重新啟動，轉發的 URL 可能會改變，需要更新 `.env.local`

## 資料庫架構

### 主要資料表

- **stocks**: 股票主檔（代碼與名稱）
- **watchlist**: 追蹤清單
- **monthly_revenue**: 月營收資料
- **price_cache**: 股價緩存
- **news_cache**: 新聞緩存
- **ai_analysis_cache**: AI 分析緩存（預留）

## API 端點

### Watchlist
- `GET /api/watchlist` - 取得追蹤清單
- `POST /api/watchlist` - 新增股票
- `DELETE /api/watchlist/{stock_id}` - 移除股票
- `PATCH /api/watchlist/{stock_id}` - 更新項目

### Stocks
- `GET /api/stocks/{stock_id}` - 取得股票詳細資訊
- `GET /api/stocks/{stock_id}/monthly_revenue` - 取得月營收序列

### Prices
- `GET /api/prices?stocks=2330,2317` - 批次查詢股價

## 資料格式

### 營收顯示
- 以「億元」為單位顯示
- 保留兩位小數
- 千分位分隔符號

### YoY 顯示
- 正值顯示紅色（+X.XX%）
- 負值顯示綠色（-X.XX%）
- 無資料顯示「—」

## Docker 部署

```bash
# 後端
cd backend
docker build -t stock-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data stock-backend

# 前端
cd frontend
docker build -t stock-frontend .
docker run -p 3000:3000 stock-frontend
```

## 專案結構

```
stock_test/
├── backend/
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置與業務邏輯
│   │   ├── crud/         # 資料庫操作
│   │   ├── db/           # 資料庫連接
│   │   ├── models/       # SQLAlchemy 模型
│   │   ├── schemas/      # Pydantic 模式
│   │   └── scripts/      # 工具腳本
│   ├── fixtures/         # 初始資料
│   └── data/             # SQLite 資料庫檔案
└── frontend/
    ├── app/              # Next.js App Router
    ├── components/       # React 元件
    └── lib/              # 工具函數與 API 客戶端
```

## 開發計劃

### 已完成 ✅
- [x] 後端 API 完整實作
- [x] SQLite 資料庫與模型
- [x] 前端響應式介面
- [x] 追蹤清單 CRUD 功能
- [x] 營收與 YoY 計算邏輯
- [x] 初始資料匯入

### 待實作 🚧
- [ ] 外部 API 整合（TWSE、FinMind）
- [ ] 背景排程器（自動更新股價）
- [ ] 新聞抓取與展示
- [ ] Excel 匯出功能
- [ ] 單元測試與整合測試
- [ ] 生產環境部署配置

## 授權

MIT License

## 貢獻

歡迎提交 Issue 或 Pull Request！