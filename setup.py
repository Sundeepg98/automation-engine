#!/usr/bin/env python3
"""
Automation Engine Setup Script
Configures your Google Cloud project for maximum power
"""

import os
import sys
import json
import shutil
from pathlib import Path

print("🚀 AUTOMATION ENGINE SETUP")
print("=" * 60)
print("Project: automation-engine-463103")
print("Service Account: automation-service@automation-engine-463103.iam.gserviceaccount.com")
print("=" * 60)

# Setup steps
setup_tasks = {
    "1. Place Service Account Key": {
        "action": "Copy your downloaded key to ./credentials/automation-service-key.json",
        "verify": lambda: Path("./credentials/automation-service-key.json").exists(),
        "help": "Download from: Google Cloud Console → IAM → Service Accounts → Keys"
    },
    
    "2. Enable Required APIs": {
        "action": "Enable these APIs in Google Cloud Console",
        "apis": [
            "Google Drive API - For file operations",
            "Cloud Storage API - For better file handling", 
            "Cloud Run API - For serverless compute",
            "Cloud Functions API - For event-driven automation",
            "Vertex AI API - For ML capabilities",
            "Cloud Build API - For container building",
            "Cloud Scheduler API - For cron jobs",
            "Pub/Sub API - For messaging"
        ],
        "verify": lambda: True,  # Manual verification
        "help": "Go to: APIs & Services → Library → Search and Enable each"
    },
    
    "3. Create Cloud Storage Bucket": {
        "action": "Create bucket 'automation-engine-data' (or similar)",
        "command": "gsutil mb -p automation-engine-463103 gs://automation-engine-data-463103",
        "verify": lambda: True,
        "help": "For storing large files and results"
    },
    
    "4. Set Up Authentication": {
        "action": "Configure local authentication",
        "command": "export GOOGLE_APPLICATION_CREDENTIALS=./credentials/automation-service-key.json",
        "verify": lambda: os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None,
        "help": "Add to your .bashrc or .zshrc for persistence"
    }
}

def check_setup():
    """Check what's already configured"""
    print("\n📋 Checking current setup...")
    
    # Check for service account key
    key_path = Path("./credentials/automation-service-key.json")
    if key_path.exists():
        print("✅ Service account key found")
        try:
            with open(key_path) as f:
                key_data = json.load(f)
                print(f"   Project: {key_data.get('project_id', 'Unknown')}")
                print(f"   Account: {key_data.get('client_email', 'Unknown')}")
        except:
            print("   ⚠️  Could not read key file")
    else:
        print("❌ Service account key not found")
        print("   → Download from Google Cloud Console")
    
    # Check for .env file
    if Path(".env").exists():
        print("✅ .env file configured")
    else:
        print("❌ .env file not found")
        print("   → Copy .env.example to .env")
    
    # Check Python environment
    print(f"\n🐍 Python: {sys.version.split()[0]}")
    
    return key_path.exists()

def setup_credentials():
    """Help set up credentials"""
    print("\n🔐 Setting up credentials...")
    
    # Create credentials directory
    Path("credentials").mkdir(exist_ok=True)
    
    # Create .gitignore for credentials
    gitignore_content = """# Never commit credentials
*.json
*.pem
*.key
.env
"""
    with open("credentials/.gitignore", "w") as f:
        f.write(gitignore_content)
    print("✅ Created credentials/.gitignore")
    
    # Copy .env.example to .env if not exists
    if not Path(".env").exists() and Path(".env.example").exists():
        shutil.copy(".env.example", ".env")
        print("✅ Created .env from template")

def display_next_steps():
    """Show what to do next"""
    print("\n🎯 NEXT STEPS")
    print("=" * 60)
    
    steps = [
        "1. Copy your service account key to ./credentials/automation-service-key.json",
        "2. Enable APIs in Google Cloud Console (see list above)",
        "3. Run: pip install -r requirements.txt",
        "4. Edit .env with your configuration",
        "5. Run: python examples/test_setup.py"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n💡 TIP: Start with the Cloud Storage API test")
    print("   It's the easiest way to verify everything works!")

if __name__ == "__main__":
    # Check current setup
    has_key = check_setup()
    
    # Setup credentials directory
    setup_credentials()
    
    # Display next steps
    display_next_steps()
    
    if has_key:
        print("\n✅ You're ready to start building!")
    else:
        print("\n⚠️  Complete the setup steps above first")