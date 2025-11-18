#!/bin/bash

echo "🔍 診斷前端連接問題..."
echo "================================"
echo ""

# Check if .env.local exists
echo "1️⃣ 檢查 .env.local 檔案"
if [ -f .env.local ]; then
    echo "✅ .env.local 存在"
    echo "內容:"
    cat .env.local
    echo ""
else
    echo "❌ .env.local 不存在"
    echo ""
fi

# Check environment variable
echo "2️⃣ 檢查環境變數"
if [ -n "$NEXT_PUBLIC_API_BASE_URL" ]; then
    echo "✅ NEXT_PUBLIC_API_BASE_URL = $NEXT_PUBLIC_API_BASE_URL"
else
    echo "⚠️  NEXT_PUBLIC_API_BASE_URL 未設定"
    if [ -f .env.local ]; then
        source .env.local 2>/dev/null
        echo "從 .env.local 讀取: $NEXT_PUBLIC_API_BASE_URL"
    fi
fi
echo ""

# Check if in Codespaces
echo "3️⃣ 檢查是否在 Codespaces 中"
if [ -n "$CODESPACE_NAME" ]; then
    echo "✅ 在 Codespaces 中"
    echo "   CODESPACE_NAME = $CODESPACE_NAME"
    echo "   GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN = $GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN"
    
    # Construct expected backend URL
    EXPECTED_URL="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    echo ""
    echo "預期的後端 URL: $EXPECTED_URL"
    echo ""
else
    echo "ℹ️  本地環境（非 Codespaces）"
    echo "預期的後端 URL: http://localhost:8000"
    echo ""
fi

# Test backend connectivity
echo "4️⃣ 測試後端連接"
BACKEND_URL="${NEXT_PUBLIC_API_BASE_URL:-http://localhost:8000}"
echo "測試 URL: $BACKEND_URL/health"

# Try to connect
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ 後端連接成功 (HTTP $HTTP_CODE)"
    echo "回應:"
    curl -s "$BACKEND_URL/health" | jq . 2>/dev/null || curl -s "$BACKEND_URL/health"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "❌ 無法連接到後端（連接被拒絕或超時）"
    echo ""
    echo "可能原因:"
    echo "  1. 後端未啟動"
    echo "  2. 端口轉發未正確設定"
    echo "  3. URL 不正確"
else
    echo "⚠️  後端回應異常 (HTTP $HTTP_CODE)"
fi
echo ""

# Test API endpoint
echo "5️⃣ 測試 API 端點"
echo "測試 URL: $BACKEND_URL/api/watchlist"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/watchlist" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ API 端點正常 (HTTP $HTTP_CODE)"
    echo "回應:"
    curl -s "$BACKEND_URL/api/watchlist" | jq . 2>/dev/null || curl -s "$BACKEND_URL/api/watchlist"
else
    echo "❌ API 端點異常 (HTTP $HTTP_CODE)"
fi
echo ""

# Check if backend is running
echo "6️⃣ 檢查後端進程"
if pgrep -f "uvicorn" > /dev/null; then
    echo "✅ Uvicorn 正在運行"
    echo "進程資訊:"
    ps aux | grep uvicorn | grep -v grep
else
    echo "❌ Uvicorn 未運行"
    echo ""
    echo "請啟動後端:"
    echo "  cd backend"
    echo "  uvicorn app.main:app --host 0.0.0.0 --port 8000"
fi
echo ""

# Check ports
echo "7️⃣ 檢查端口使用情況"
if command -v lsof > /dev/null; then
    echo "Port 8000:"
    lsof -i :8000 2>/dev/null || echo "  未使用"
    echo "Port 3000:"
    lsof -i :3000 2>/dev/null || echo "  未使用"
elif command -v netstat > /dev/null; then
    echo "Port 8000:"
    netstat -tuln | grep 8000 || echo "  未使用"
    echo "Port 3000:"
    netstat -tuln | grep 3000 || echo "  未使用"
else
    echo "⚠️  無法檢查端口（lsof 和 netstat 都不可用）"
fi
echo ""

echo "================================"
echo "診斷完成！"
echo ""
echo "📝 下一步建議:"
echo ""
if [ -n "$CODESPACE_NAME" ]; then
    echo "Codespaces 環境:"
    echo "1. 確認後端正在運行"
    echo "2. 點擊 VS Code 底部的 'PORTS' 標籤"
    echo "3. 確認 port 8000 的「Visibility」是 'Public'"
    echo "4. 複製 port 8000 的「Forwarded Address」"
    echo "5. 執行: echo \"NEXT_PUBLIC_API_BASE_URL=<複製的URL>\" > .env.local"
    echo "6. 重新啟動前端: npm run dev"
else
    echo "本地環境:"
    echo "1. 確認後端在 http://localhost:8000 運行"
    echo "2. 執行: echo \"NEXT_PUBLIC_API_BASE_URL=http://localhost:8000\" > .env.local"
    echo "3. 重新啟動前端: npm run dev"
fi
