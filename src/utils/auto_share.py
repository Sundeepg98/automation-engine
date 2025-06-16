#!/usr/bin/env python3
"""
Auto-share utility - Automatically shares all created files with owner
"""

import os
from functools import wraps
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Optional, Dict, Any

class AutoShare:
    """Automatically share files created by service account"""
    
    def __init__(self, owner_email: str, credentials_path: Optional[str] = None):
        self.owner_email = owner_email
        
        # Load credentials
        if credentials_path is None:
            credentials_path = os.getenv('SERVICE_ACCOUNT_KEY_PATH')
            
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
    
    def share_file(self, file_id: str, role: str = 'writer') -> Dict[str, Any]:
        """Share a file with the owner"""
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': self.owner_email
            }
            
            result = self.drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=False  # Don't spam with emails
            ).execute()
            
            print(f"✅ Auto-shared with {self.owner_email}")
            return result
            
        except Exception as e:
            print(f"⚠️  Could not auto-share: {e}")
            return {}
    
    def create_spreadsheet(self, title: str, **kwargs) -> Dict[str, Any]:
        """Create a spreadsheet and auto-share it"""
        # Create the spreadsheet
        spreadsheet = self.sheets_service.spreadsheets().create(
            body={'properties': {'title': title}, **kwargs}
        ).execute()
        
        # Auto-share it
        self.share_file(spreadsheet['spreadsheetId'])
        
        return spreadsheet
    
    def create_document(self, name: str, mime_type: str = 'application/vnd.google-apps.document', 
                       parents: Optional[list] = None) -> Dict[str, Any]:
        """Create any Drive file and auto-share it"""
        file_metadata = {
            'name': name,
            'mimeType': mime_type
        }
        
        if parents:
            file_metadata['parents'] = parents
            
        # Create the file
        file = self.drive_service.files().create(
            body=file_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        # Auto-share it
        self.share_file(file['id'])
        
        return file
    
    def create_folder(self, name: str, parents: Optional[list] = None) -> Dict[str, Any]:
        """Create a folder and auto-share it"""
        return self.create_document(
            name=name,
            mime_type='application/vnd.google-apps.folder',
            parents=parents
        )

# Decorator for auto-sharing
def with_auto_share(owner_email: str):
    """Decorator to auto-share any created files"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Run the original function
            result = func(*args, **kwargs)
            
            # Check if it returned a file/folder ID
            if isinstance(result, dict):
                if 'spreadsheetId' in result:
                    auto_sharer = AutoShare(owner_email)
                    auto_sharer.share_file(result['spreadsheetId'])
                elif 'id' in result and 'kind' in result and 'drive' in result['kind']:
                    auto_sharer = AutoShare(owner_email)
                    auto_sharer.share_file(result['id'])
                    
            return result
        return wrapper
    return decorator

# Global auto-share instance
_auto_share_instance = None

def init_auto_share(owner_email: str):
    """Initialize global auto-share"""
    global _auto_share_instance
    _auto_share_instance = AutoShare(owner_email)
    return _auto_share_instance

def get_auto_share():
    """Get the global auto-share instance"""
    if _auto_share_instance is None:
        # Try to get from environment
        owner_email = os.getenv('OWNER_EMAIL', 'sundeepg8@gmail.com')
        return init_auto_share(owner_email)
    return _auto_share_instance