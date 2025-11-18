#!/bin/bash

# Helper script to set up frontend environment in Codespaces
# This script detects if running in Codespaces and configures the backend URL

echo "🔧 Setting up frontend environment..."

if [ -n "$CODESPACE_NAME" ]; then
    echo "✅ Detected GitHub Codespaces environment"
    
    # In Codespaces, construct the backend URL
    BACKEND_URL="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    
    echo "📡 Backend URL: $BACKEND_URL"
    echo "NEXT_PUBLIC_API_BASE_URL=$BACKEND_URL" > .env.local
    
    echo "✅ Created .env.local with Codespaces backend URL"
else
    echo "💻 Local development environment detected"
    
    if [ ! -f .env.local ]; then
        echo "📝 Creating .env.local for local development"
        cp .env.local.example .env.local
        echo "✅ Created .env.local from example file"
        echo "⚠️  Please verify the backend URL in .env.local"
    else
        echo "ℹ️  .env.local already exists"
    fi
fi

echo ""
echo "🎉 Setup complete! You can now run:"
echo "   npm install"
echo "   npm run dev"
