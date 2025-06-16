# 🔐 Auto-Share: Never Get Locked Out Again!

## The Problem (SOLVED!)
Every time the service account creates a file, you can't access it without manually granting permissions. This is annoying!

## The Solution
We've created a smart wrapper that **automatically shares everything with you**!

## How to Use

### Method 1: Using GoogleServices (Recommended)

```python
from src.core.google_services import GoogleServices

# Initialize once
google = GoogleServices()  # Uses OWNER_EMAIL from .env

# Create spreadsheet - automatically shared with you!
spreadsheet = google.create_spreadsheet('My Data')

# Create folder - automatically shared with you!
folder = google.create_folder('My Project Files')

# Upload file - automatically shared with you!
file = google.upload_file('report.txt', 'Hello World!')

# Everything is auto-shared! No more access requests!
```

### Method 2: Quick Functions

```python
from src.core.google_services import create_spreadsheet, create_folder

# Even simpler - just import and use
sheet = create_spreadsheet('Quick Sheet')
folder = create_folder('Quick Folder')

# Auto-shared with your email from .env!
```

### Method 3: Using AutoShare Directly

```python
from src.utils.auto_share import AutoShare

# Create auto-sharer
auto_share = AutoShare('your-email@gmail.com')

# Use it for any creation
spreadsheet = auto_share.create_spreadsheet('My Sheet')
folder = auto_share.create_folder('My Folder')
```

## Configuration

Your `.env` file has:
```env
OWNER_EMAIL=sundeepg8@gmail.com
AUTO_SHARE_ENABLED=true
```

This means:
- ✅ Every file created is shared with sundeepg8@gmail.com
- ✅ No manual sharing needed
- ✅ No more "Request access" screens

## For Colab Integration

Update your colab-bridge to use this:

```python
# Old way (no auto-share)
sheets_service.spreadsheets().create(...)

# New way (with auto-share!)
from automation_engine.src.core.google_services import GoogleServices
google = GoogleServices()
spreadsheet = google.create_spreadsheet('Colab Results')
```

## Benefits

1. **No More Lockouts** - Everything is shared automatically
2. **Clean Code** - One import, simple methods
3. **Configurable** - Change owner email in .env
4. **Works Everywhere** - Use in any project

## Example: Complete Workflow

```python
from src.core.google_services import GoogleServices

# Initialize
google = GoogleServices()

# Create project structure
project_folder = google.create_folder('My Automation Project')
data_sheet = google.create_spreadsheet('Project Database')
config_doc = google.create_document('Project Config')

# Upload results
results = google.upload_file(
    'results.json',
    '{"status": "success"}',
    parent_id=project_folder['id']
)

# Everything is accessible immediately in your Drive!
print(f"Folder: {project_folder['webViewLink']}")
print(f"Sheet: {data_sheet['spreadsheetUrl']}")
```

## Never Forget!

**Always use GoogleServices or AutoShare for creating files!**

This ensures you always have access to everything your automation creates.