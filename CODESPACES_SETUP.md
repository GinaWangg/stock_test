# Codespaces 連接問題完整解決指南

## 問題症狀
前端顯示「載入資料時發生錯誤」，即使已經設定 `.env.local`

## 最常見原因：Port Visibility 設定錯誤

### ✅ 完整解決步驟

#### 第 1 步：確認後端正在運行

在終端機 1 執行：
```bash
cd backend
pip install -r requirements.txt
python app/scripts/import_fixtures.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

看到這個訊息表示成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 第 2 步：設定 Port Visibility 為 Public

**這是最關鍵的步驟！**

1. 點擊 VS Code 底部的 **「PORTS」** 標籤
2. 找到 port **8000** 那一列
3. 右鍵點擊 port 8000
4. 選擇 **「Port Visibility」** → **「Public」**

   **重要**：預設是 Private，前端無法訪問！必須改成 Public！

5. 同樣將 port **3000** 也設為 **Public**

#### 第 3 步：複製正確的後端 URL

1. 在 PORTS 標籤中，找到 port 8000
2. 將滑鼠移到「**Forwarded Address**」欄位
3. 複製完整的 URL（例如：`https://username-repo-abc123-8000.app.github.dev`）
4. **測試** 這個 URL：在瀏覽器中開啟 `<複製的URL>/docs`，應該能看到 API 文檔

#### 第 4 步：設定前端環境變數

在終端機 2 執行：

```bash
cd frontend

# 方法 A：使用診斷腳本（推薦）
bash diagnose.sh  # 會顯示目前設定並給建議

# 方法 B：手動設定
echo "NEXT_PUBLIC_API_BASE_URL=<貼上第3步複製的URL>" > .env.local

# 驗證設定
cat .env.local
```

#### 第 5 步：安裝依賴並啟動前端

```bash
npm install
npm run dev
```

#### 第 6 步：開啟前端

1. 在 PORTS 標籤找到 port 3000
2. 點擊「地球」圖示或複製 Forwarded Address
3. 在瀏覽器中開啟

---

## 🔍 診斷工具

執行診斷腳本來檢查所有設定：

```bash
cd frontend
bash diagnose.sh
```

這個腳本會檢查：
- ✅ .env.local 是否存在
- ✅ 環境變數是否正確
- ✅ 是否在 Codespaces 中
- ✅ 後端連接是否正常
- ✅ API 端點是否可訪問
- ✅ 進程是否運行
- ✅ 端口使用情況

---

## ❌ 常見錯誤

### 錯誤 1：Port Visibility 是 Private
**症狀**：瀏覽器無法連接到後端，顯示 ERR_CONNECTION_REFUSED

**解決**：將 port 8000 和 3000 都設為 Public

### 錯誤 2：使用錯誤的 URL 格式
**症狀**：URL 包含 `localhost` 或格式不對

**正確格式**：
```
https://username-repo-abc123-8000.app.github.dev
```

**錯誤格式**：
```
http://localhost:8000  ❌
https://8000-username-repo-abc123.githubpreview.dev  ❌（舊格式）
```

### 錯誤 3：.env.local 未生效
**症狀**：前端仍使用 localhost:8000

**原因**：
- Next.js 需要重新啟動才會讀取新的 .env.local
- 檔案名稱錯誤（應該是 `.env.local` 不是 `.env` 或 `env.local`）

**解決**：
```bash
# 停止前端 (Ctrl+C)
# 重新啟動
npm run dev
```

### 錯誤 4：後端未啟動或崩潰
**檢查**：
```bash
# 檢查後端進程
ps aux | grep uvicorn

# 查看後端日誌
# 在後端終端機查看是否有錯誤訊息
```

### 錯誤 5：CORS 錯誤
**症狀**：瀏覽器 Console 顯示 CORS policy 錯誤

**檢查**：
- 後端 CORS 設定（已設為 allow_origins=["*"]）
- Port visibility 必須是 Public

---

## 🧪 測試連接

### 測試 1：測試後端健康檢查
```bash
# 使用 .env.local 中的 URL
BACKEND_URL=$(grep NEXT_PUBLIC_API_BASE_URL .env.local | cut -d'=' -f2)
curl $BACKEND_URL/health

# 應該返回：
# {"status":"healthy"}
```

### 測試 2：測試 API 端點
```bash
curl $BACKEND_URL/api/watchlist

# 應該返回 JSON 陣列（可能為空 []）
```

### 測試 3：在瀏覽器測試
開啟：`<後端URL>/docs`

應該能看到 FastAPI 的 Swagger 文檔介面

---

## 🆘 仍然無法解決？

執行完整診斷並回報：

```bash
cd frontend
bash diagnose.sh > diagnostic-report.txt
cat diagnostic-report.txt
```

將診斷報告的輸出貼到 issue 中，包含：
1. 完整的診斷輸出
2. 瀏覽器 Console 的錯誤訊息（按 F12 開啟開發者工具）
3. 後端終端機的日誌
4. PORTS 標籤的截圖

---

## 📋 快速檢查清單

- [ ] 後端在終端機 1 正在運行
- [ ] Port 8000 visibility 設為 **Public**
- [ ] Port 3000 visibility 設為 **Public**
- [ ] 已複製正確的 port 8000 forwarded URL
- [ ] .env.local 檔案存在且內容正確
- [ ] 執行了 `npm run dev` 啟動前端
- [ ] 在瀏覽器中能開啟 `<後端URL>/docs`
- [ ] 在瀏覽器中能開啟 `<前端URL>`

全部打勾後，應該就能正常使用了！
