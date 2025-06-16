# 🚀 Cloud Shell Quick Start

## Step 1: Open Cloud Shell
Go to: https://shell.cloud.google.com

## Step 2: Upload Service Account Key
1. Click the **⋮** menu (3 dots) in Cloud Shell
2. Select **Upload file**
3. Upload your `automation-engine-463103-ee5a06e18248.json`

## Step 3: Run Setup
```bash
# Download and run setup script
curl -O https://raw.githubusercontent.com/sundeepg98/automation-engine/main/cloud_shell_setup.sh
chmod +x cloud_shell_setup.sh
./cloud_shell_setup.sh

# Move your uploaded key
mv ~/automation-engine-463103-ee5a06e18248.json automation-engine/credentials/
```

## Step 4: Test Everything
```bash
cd automation-engine
python3 test_setup.py
```

## Step 5: Use VS Code
Click **Open Editor** button (top right) to get VS Code!

## 💡 Tips
- Your home directory persists between sessions
- Cloud Shell has 5GB storage
- Pre-installed: Python, Node.js, Git, Docker
- Free 60 hours/week usage

## 🔧 Install Claude Coder (Optional)
```bash
npm install -g @anthropic/claude-code
```