#!/usr/bin/env python3
"""
Google Sheets as a FREE Database!
No billing needed - unlimited storage for structured data
"""

import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

print("🗃️ GOOGLE SHEETS AS DATABASE - NO BILLING NEEDED!")
print("=" * 60)

# Initialize credentials
credentials = service_account.Credentials.from_service_account_file(
    os.getenv('SERVICE_ACCOUNT_KEY_PATH'),
    scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
)

# Build services
sheets_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

# Create a database spreadsheet
print("📊 Creating database spreadsheet...")

spreadsheet_body = {
    'properties': {
        'title': f'Automation Database - {datetime.now().strftime("%Y-%m-%d")}'
    },
    'sheets': [
        {
            'properties': {
                'sheetId': 0,
                'title': 'executions',
                'gridProperties': {
                    'rowCount': 10000,
                    'columnCount': 10
                }
            }
        },
        {
            'properties': {
                'sheetId': 1,
                'title': 'tenants',
                'gridProperties': {
                    'rowCount': 1000,
                    'columnCount': 8
                }
            }
        },
        {
            'properties': {
                'sheetId': 2,
                'title': 'logs',
                'gridProperties': {
                    'rowCount': 50000,
                    'columnCount': 6
                }
            }
        }
    ]
}

spreadsheet = sheets_service.spreadsheets().create(
    body=spreadsheet_body,
    fields='spreadsheetId,spreadsheetUrl,sheets'
).execute()

spreadsheet_id = spreadsheet['spreadsheetId']
print(f"✅ Database created!")
print(f"   ID: {spreadsheet_id}")
print(f"   URL: {spreadsheet['spreadsheetUrl']}")

# Set up database schema
print("\n🏗️ Setting up database schema...")

# Executions table headers
executions_headers = [
    ['ID', 'Tenant ID', 'Code', 'Status', 'Result', 'Error', 'Started At', 'Completed At', 'Duration (ms)', 'Metadata']
]

# Tenants table headers  
tenants_headers = [
    ['ID', 'Name', 'API Key', 'Created At', 'Status', 'Quota Used', 'Quota Limit', 'Settings']
]

# Logs table headers
logs_headers = [
    ['Timestamp', 'Level', 'Tenant ID', 'Message', 'Details', 'Source']
]

# Update headers
requests = [
    {
        'updateCells': {
            'range': {
                'sheetId': 0,
                'startRowIndex': 0,
                'endRowIndex': 1
            },
            'rows': [{'values': [{'userEnteredValue': {'stringValue': h}} for h in executions_headers[0]]}],
            'fields': 'userEnteredValue'
        }
    },
    {
        'updateCells': {
            'range': {
                'sheetId': 1,
                'startRowIndex': 0,
                'endRowIndex': 1
            },
            'rows': [{'values': [{'userEnteredValue': {'stringValue': h}} for h in tenants_headers[0]]}],
            'fields': 'userEnteredValue'
        }
    },
    {
        'updateCells': {
            'range': {
                'sheetId': 2,
                'startRowIndex': 0,
                'endRowIndex': 1
            },
            'rows': [{'values': [{'userEnteredValue': {'stringValue': h}} for h in logs_headers[0]]}],
            'fields': 'userEnteredValue'
        }
    }
]

# Format headers (bold, freeze)
for sheet_id in [0, 1, 2]:
    requests.extend([
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True},
                        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
                    }
                },
                'fields': 'userEnteredFormat'
            }
        },
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        }
    ])

sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={'requests': requests}
).execute()

print("✅ Schema created with 3 tables: executions, tenants, logs")

# Demo: Insert sample data
print("\n📝 Inserting sample data...")

# Add a tenant
tenant_data = [
    ['tenant-001', 'Claude AI', 'sk-demo-key-123', datetime.now().isoformat(), 
     'active', '0', '1000', '{"model": "claude-3", "features": ["colab", "storage"]}']
]

sheets_service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range='tenants!A2',
    valueInputOption='USER_ENTERED',
    body={'values': tenant_data}
).execute()

# Add execution records
execution_data = []
for i in range(5):
    execution_data.append([
        f'exec-{i+1:03d}',
        'tenant-001',
        f'print("Test {i+1}")',
        'completed',
        f'Test {i+1}',
        '',
        datetime.now().isoformat(),
        datetime.now().isoformat(),
        str(100 + i * 50),
        '{"engine": "colab", "gpu": false}'
    ])

sheets_service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range='executions!A2',
    valueInputOption='USER_ENTERED',
    body={'values': execution_data}
).execute()

print("✅ Sample data inserted!")

# Demo: Query data
print("\n🔍 Querying data...")

# Read all tenants
result = sheets_service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='tenants!A2:H'
).execute()

tenants = result.get('values', [])
print(f"\nActive Tenants: {len(tenants)}")
for tenant in tenants:
    print(f"  - {tenant[1]} (ID: {tenant[0]}, Status: {tenant[4]})")

# Read execution statistics
result = sheets_service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='executions!A2:J'
).execute()

executions = result.get('values', [])
print(f"\nTotal Executions: {len(executions)}")

# Calculate stats
if executions:
    durations = [int(e[8]) for e in executions if len(e) > 8 and e[8]]
    avg_duration = sum(durations) / len(durations) if durations else 0
    print(f"Average Duration: {avg_duration:.0f}ms")

print("\n" + "=" * 60)
print("💡 SHEETS DATABASE FEATURES:")
print("=" * 60)
print("✅ FREE - No billing needed!")
print("✅ 10 million cells per spreadsheet")
print("✅ Real-time collaboration")
print("✅ Built-in versioning")
print("✅ Query with formulas (VLOOKUP, FILTER, etc.)")
print("✅ Trigger functions on changes")
print("✅ Export to BigQuery later when you scale")

print("\n🔧 ADVANCED FEATURES:")
print("- Use named ranges for table references")
print("- Create pivot tables for analytics")
print("- Use Apps Script for triggers")
print("- Share specific sheets with users")
print("- Use formulas for computed columns")

# Create a helper class
print("\n📦 Here's a database helper class:")

database_helper = '''
class SheetsDatabase:
    """Google Sheets as a database"""
    
    def __init__(self, spreadsheet_id, credentials):
        self.spreadsheet_id = spreadsheet_id
        self.service = build('sheets', 'v4', credentials=credentials)
    
    def insert(self, table: str, data: list):
        """Insert rows into table"""
        return self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f'{table}!A:Z',
            valueInputOption='USER_ENTERED',
            body={'values': data}
        ).execute()
    
    def query(self, table: str, range: str = 'A:Z'):
        """Query data from table"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f'{table}!{range}'
        ).execute()
        return result.get('values', [])
    
    def update(self, table: str, range: str, data: list):
        """Update specific cells"""
        return self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f'{table}!{range}',
            valueInputOption='USER_ENTERED',
            body={'values': data}
        ).execute()
    
    def delete_rows(self, sheet_id: int, start_row: int, end_row: int):
        """Delete rows from table"""
        request = {
            'deleteDimension': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'ROWS',
                    'startIndex': start_row - 1,
                    'endIndex': end_row
                }
            }
        }
        return self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={'requests': [request]}
        ).execute()
'''

print(database_helper)

print(f"\n✅ Your database is ready at: {spreadsheet['spreadsheetUrl']}")
print("🚀 Start building with FREE unlimited database storage!")