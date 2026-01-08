#!/bin/bash
# Complete Cloud Shell Setup for Business

echo "🚀 Setting up your business workspace..."

# 1. Clone both repositories
cd ~/projects
echo "📦 Cloning repositories..."
# git clone https://github.com/Sundeepg98/automation-engine.git
# git clone https://github.com/Sundeepg98/colab-bridge.git

# 2. Set up service account credentials
echo "🔐 Setting up credentials..."
mkdir -p ~/projects/automation-engine/credentials
mkdir -p ~/projects/colab-bridge/credentials
# Upload automation-engine-463103-ee5a06e18248.json and copy to both

# 3. Install development tools
echo "🛠️ Installing tools..."
npm install -g vsce  # VS Code extension tool
pip3 install --user google-api-python-client google-auth pytest black

# 4. Create workspace shortcuts
echo "📁 Creating shortcuts..."
cat > ~/scripts/work-on-colab.sh << 'EOF'
#!/bin/bash
cd ~/projects/colab-bridge
echo "📍 Working on Colab-Bridge"
code .
EOF

cat > ~/scripts/work-on-automation.sh << 'EOF'
#!/bin/bash
cd ~/projects/automation-engine
echo "📍 Working on Automation Engine"
code .
EOF

chmod +x ~/scripts/*.sh

# 5. Set up git
echo "📝 Configuring git..."
git config --global user.email "sundeepg8@gmail.com"
git config --global user.name "Sundeepg98"

# 6. Create business tracker
cat > ~/documents/work/business-tracker.md << 'EOF'
# Business Tracker

## Colab-Bridge
- [ ] Clean up code
- [ ] Test extension
- [ ] Create demo video
- [ ] Submit to marketplace

## Automation Engine
- [ ] Implement auth
- [ ] Add usage tracking
- [ ] Create landing page
- [ ] Find first customer

## Weekly Goals
Week 1: Launch Colab-Bridge
Week 2: Get 100 installs
Week 3: Launch Automation Engine
Week 4: First paying customer
EOF

echo "✅ Setup complete!"