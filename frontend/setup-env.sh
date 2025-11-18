#!/bin/bash

# Helper script to set up frontend environment in Codespaces
# This script detects if running in Codespaces and configures the backend URL

echo "🔧 Setting up frontend environment..."
echo ""

if [ -n "$CODESPACE_NAME" ]; then
    echo "✅ Detected GitHub Codespaces environment"
    echo ""
    
    # In Codespaces, construct the backend URL
    BACKEND_URL="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    
    echo "📡 Backend URL: $BACKEND_URL"
    echo "NEXT_PUBLIC_API_BASE_URL=$BACKEND_URL" > .env.local
    
    echo "✅ Created .env.local with Codespaces backend URL"
    echo ""
    
    # Test backend connectivity
    echo "🔍 Testing backend connection..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" --connect-timeout 5 2>/dev/null)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Backend is reachable!"
    elif [ "$HTTP_CODE" = "000" ]; then
        echo "⚠️  WARNING: Cannot connect to backend"
        echo ""
        echo "Please check:"
        echo "  1. Backend is running: uvicorn app.main:app --host 0.0.0.0 --port 8000"
        echo "  2. Port 8000 visibility is set to 'Public' in the PORTS tab"
        echo ""
        echo "To set port visibility:"
        echo "  - Click 'PORTS' tab at the bottom of VS Code"
        echo "  - Right-click port 8000"
        echo "  - Select 'Port Visibility' → 'Public'"
        echo ""
    else
        echo "⚠️  WARNING: Backend returned HTTP $HTTP_CODE"
    fi
    echo ""
    
    echo "📋 Important next steps:"
    echo "  1. Make sure backend is running in another terminal"
    echo "  2. Set port 8000 to 'Public' in PORTS tab (very important!)"
    echo "  3. Set port 3000 to 'Public' in PORTS tab"
    echo "  4. Run: npm install && npm run dev"
    echo ""
    echo "For detailed troubleshooting, see: ../CODESPACES_SETUP.md"
    
else
    echo "💻 Local development environment detected"
    echo ""
    
    if [ ! -f .env.local ]; then
        echo "📝 Creating .env.local for local development"
        cp .env.local.example .env.local
        echo "✅ Created .env.local from example file"
        echo ""
        echo "⚠️  Please verify the backend URL in .env.local"
    else
        echo "ℹ️  .env.local already exists"
        echo "Current configuration:"
        cat .env.local
    fi
    echo ""
    
    # Test local backend
    echo "🔍 Testing local backend..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health" --connect-timeout 5 2>/dev/null)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Backend is running!"
    else
        echo "⚠️  Backend not responding"
        echo "Please start backend: cd backend && uvicorn app.main:app --port 8000"
    fi
fi

echo ""
echo "🎉 Setup complete! You can now run:"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "💡 TIP: Run 'bash diagnose.sh' to check all settings"
