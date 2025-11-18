# Troubleshooting Guide / 問題排解指南

## ⚠️ 最常見問題：Port Visibility 設定

### 問題：在 Codespaces 中前端顯示「載入資料時發生錯誤」

**症狀**: 
- 後端正在運行
- 已設定 .env.local
- 但前端仍然無法連接

**最可能的原因**: Port 8000 的 Visibility 設為 Private（預設值）

**解決方法**（必做）:
1. 點擊 VS Code 底部的 **「PORTS」** 標籤
2. 找到 port **8000** 那一列
3. 右鍵點擊該列
4. 選擇 **「Port Visibility」** → **「Public」**
5. 同樣將 port **3000** 也設為 **「Public」**

**為什麼重要**: 
- 預設情況下，Codespaces 的端口是 Private（只有你能訪問）
- 前端在瀏覽器中運行，需要 Public 權限才能訪問後端
- 即使設定了正確的 URL，Private 端口仍會被阻擋

---

## 前端顯示「載入資料時發生錯誤」

### 問題描述
前端啟動後顯示紅色錯誤訊息：「載入資料時發生錯誤」

### 常見原因與解決方法

#### 1. 後端未啟動
**症狀**: 前端無法連接到後端 API

**解決方法**:
```bash
# 確認後端正在運行
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 測試後端是否正常
curl http://localhost:8000/health
# 應該返回: {"status":"healthy"}
```

#### 2. 環境變數未設定或設定錯誤（Codespaces）
**症狀**: 在 GitHub Codespaces 中運行時出現錯誤

**檢查步驟**:
```bash
cd frontend

# 檢查 .env.local 是否存在
ls -la .env.local

# 檢查內容
cat .env.local

# 應該顯示類似:
# NEXT_PUBLIC_API_BASE_URL=https://xxx-8000.app.github.dev
```

**解決方法 A - 使用診斷腳本**:
```bash
cd frontend
bash diagnose.sh  # 會顯示詳細診斷資訊
```

**解決方法 B - 手動設定**:
1. 確認後端正在運行
2. 取得後端的轉發 URL：
   - 點擊 VS Code 底部的 "PORTS" 標籤
   - 找到 port 8000
   - **確認 Visibility 是 'Public'（非常重要！）**
   - 複製「Forwarded Address」欄位的 URL
   - 範例：`https://username-repo-abc123-8000.app.github.dev`

3. 設定前端環境變數：
```bash
cd frontend

# 手動建立 .env.local（替換為你複製的 URL）
echo "NEXT_PUBLIC_API_BASE_URL=https://your-forwarded-url-8000.app.github.dev" > .env.local

# 驗證設定
cat .env.local

# 測試連接
curl $(cat .env.local | cut -d'=' -f2)/health
# 應該返回: {"status":"healthy"}
```

4. 重新啟動前端：
```bash
# 停止前端 (Ctrl+C)
npm run dev
```

**解決方法 C - 使用自動設定腳本**:
```bash
cd frontend
bash setup-env.sh  # 自動偵測並設定
npm run dev
```

#### 3. CORS 問題
**症狀**: 瀏覽器控制台顯示 CORS 錯誤

**解決方法**:
- 檢查後端 CORS 設定（已在 `app/main.py` 中配置）
- 確認前端 URL 在允許的來源清單中

#### 4. 資料庫未初始化
**症狀**: 後端運行但 API 返回錯誤

**解決方法**:
```bash
cd backend
python app/scripts/import_fixtures.py
```

#### 5. 端口衝突
**症狀**: 無法啟動服務

**解決方法**:
```bash
# 檢查端口使用情況
lsof -i :8000  # 後端
lsof -i :3000  # 前端

# 終止佔用端口的進程
kill -9 <PID>
```

## 快速診斷步驟

### 步驟 1: 檢查後端
```bash
cd backend
curl http://localhost:8000/health
```
預期輸出: `{"status":"healthy"}`

### 步驟 2: 檢查 API 資料
```bash
curl http://localhost:8000/api/watchlist
```
預期輸出: JSON 陣列（可能為空 `[]` 或包含股票資料）

### 步驟 3: 檢查前端環境變數
```bash
cd frontend
cat .env.local
```
應該顯示: `NEXT_PUBLIC_API_BASE_URL=<後端 URL>`

### 步驟 4: 在 Codespaces 中驗證 URL
```bash
# 從前端測試後端連接
cd frontend
node -e "console.log('Backend URL:', process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000')"
```

### 步驟 5: 檢查瀏覽器控制台
1. 開啟瀏覽器開發者工具（F12）
2. 查看 Console 標籤是否有錯誤訊息
3. 查看 Network 標籤，確認 API 請求狀態

## Codespaces 專用設定

### 自動化設定（推薦）
```bash
cd frontend
bash setup-env.sh
npm install
npm run dev
```

### 手動設定
```bash
# 1. 取得 Codespace 名稱
echo $CODESPACE_NAME

# 2. 取得轉發域名
echo $GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN

# 3. 建立完整的後端 URL
echo "NEXT_PUBLIC_API_BASE_URL=https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}" > .env.local

# 4. 驗證設定
cat .env.local
```

## 常見錯誤訊息

### "載入資料時發生錯誤"
- **原因**: 前端無法連接到後端
- **解決**: 檢查 `.env.local` 設定是否正確

### "Stock not found"
- **原因**: 嘗試新增不存在的股票
- **解決**: 確認股票代碼正確，或使用測試資料（2330, 2357, 2317, 2454）

### "Network Error"
- **原因**: 網路連接問題或後端未啟動
- **解決**: 確認後端正在運行，檢查防火牆設定

## 需要更多幫助？

如果問題仍未解決：
1. 檢查後端日誌是否有錯誤訊息
2. 確認 Python 依賴已正確安裝
3. 確認 Node.js 依賴已正確安裝
4. 重新啟動 Codespace 或本地環境

## 完整重置步驟

如果需要完全重新開始：

```bash
# 1. 清理前端
cd frontend
rm -rf node_modules .next .env.local
npm install

# 2. 清理後端
cd ../backend
rm -rf data/stock_revenue.db*
python app/scripts/import_fixtures.py

# 3. 重新設定
cd ../frontend
bash setup-env.sh

# 4. 啟動服務
# Terminal 1:
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2:
cd frontend && npm run dev
```
