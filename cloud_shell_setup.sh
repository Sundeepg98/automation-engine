#!/bin/bash
# Cloud Shell setup script for automation-engine

echo "🚀 Setting up automation-engine in Cloud Shell"

# 1. Clone your repo
echo "📦 Cloning automation-engine..."
git clone https://github.com/sundeepg98/automation-engine.git
cd automation-engine

# 2. Create credentials directory
echo "🔐 Setting up credentials..."
mkdir -p credentials

# 3. Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install google-api-python-client google-auth

# 4. Set up environment
echo "🔧 Creating .env file..."
cat > .env << EOF
OWNER_EMAIL=sundeepg8@gmail.com
AUTO_SHARE_ENABLED=true
SERVICE_ACCOUNT_KEY_PATH=./credentials/automation-engine-463103-ee5a06e18248.json
EOF

echo "✅ Basic setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Upload your service account key to credentials/"
echo "2. Run: python3 test_setup.py"
echo "3. Start developing with VS Code (click 'Open Editor')"