#!/usr/bin/env python3
"""
Smart Google Services Wrapper
Always auto-shares with owner, no more access issues!
"""

import os
from typing import Optional, Dict, Any, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class GoogleServices:
    """
    Smart wrapper for all Google services with auto-sharing built in.
    Use this instead of direct API calls!
    """
    
    def __init__(self, owner_email: Optional[str] = None):
        # Get owner email from env or parameter
        self.owner_email = owner_email or os.getenv('OWNER_EMAIL', 'sundeepg8@gmail.com')
        
        # Load credentials
        self.credentials_path = os.getenv('SERVICE_ACCOUNT_KEY_PATH')
        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path,
            scopes=[
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/documents',
                'https://www.googleapis.com/auth/gmail.send'
            ]
        )
        
        # Initialize services lazily
        self._drive_service = None
        self._sheets_service = None
        self._docs_service = None
        
    @property
    def drive(self):
        """Get Drive service (lazy loading)"""
        if self._drive_service is None:
            self._drive_service = build('drive', 'v3', credentials=self.credentials)
        return self._drive_service
    
    @property
    def sheets(self):
        """Get Sheets service (lazy loading)"""
        if self._sheets_service is None:
            self._sheets_service = build('sheets', 'v4', credentials=self.credentials)
        return self._sheets_service
    
    @property
    def docs(self):
        """Get Docs service (lazy loading)"""
        if self._docs_service is None:
            self._docs_service = build('docs', 'v1', credentials=self.credentials)
        return self._docs_service
    
    def _auto_share(self, file_id: str, role: str = 'writer'):
        """Automatically share file with owner"""
        if os.getenv('AUTO_SHARE_ENABLED', 'true').lower() == 'true':
            try:
                permission = {
                    'type': 'user',
                    'role': role,
                    'emailAddress': self.owner_email
                }
                
                self.drive.permissions().create(
                    fileId=file_id,
                    body=permission,
                    sendNotificationEmail=False
                ).execute()
                
                print(f"✅ Auto-shared with {self.owner_email}")
                
            except Exception as e:
                print(f"⚠️  Auto-share failed: {e}")
    
    # ========== SPREADSHEET OPERATIONS ==========
    
    def create_spreadsheet(self, title: str, sheets: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Create a spreadsheet and auto-share it"""
        body = {'properties': {'title': title}}
        
        if sheets:
            body['sheets'] = sheets
            
        spreadsheet = self.sheets.spreadsheets().create(body=body).execute()
        
        # Auto-share
        self._auto_share(spreadsheet['spreadsheetId'])
        
        return spreadsheet
    
    def read_spreadsheet(self, spreadsheet_id: str, range: str) -> List[List[Any]]:
        """Read data from spreadsheet"""
        result = self.sheets.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range
        ).execute()
        
        return result.get('values', [])
    
    def write_spreadsheet(self, spreadsheet_id: str, range: str, values: List[List[Any]]):
        """Write data to spreadsheet"""
        return self.sheets.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()
    
    def append_spreadsheet(self, spreadsheet_id: str, range: str, values: List[List[Any]]):
        """Append data to spreadsheet"""
        return self.sheets.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()
    
    # ========== DRIVE OPERATIONS ==========
    
    def create_folder(self, name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a folder and auto-share it"""
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            metadata['parents'] = [parent_id]
            
        folder = self.drive.files().create(
            body=metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        # Auto-share
        self._auto_share(folder['id'])
        
        return folder
    
    def upload_file(self, name: str, content: str, parent_id: Optional[str] = None, 
                   mime_type: str = 'text/plain') -> Dict[str, Any]:
        """Upload a file and auto-share it"""
        from googleapiclient.http import MediaInMemoryUpload
        
        metadata = {'name': name}
        if parent_id:
            metadata['parents'] = [parent_id]
            
        media = MediaInMemoryUpload(content.encode(), mimetype=mime_type)
        
        file = self.drive.files().create(
            body=metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        # Auto-share
        self._auto_share(file['id'])
        
        return file
    
    def list_files(self, query: Optional[str] = None, page_size: int = 100) -> List[Dict[str, Any]]:
        """List files in Drive"""
        params = {
            'pageSize': page_size,
            'fields': 'files(id,name,mimeType,modifiedTime,webViewLink)'
        }
        
        if query:
            params['q'] = query
            
        result = self.drive.files().list(**params).execute()
        return result.get('files', [])
    
    # ========== DOCUMENT OPERATIONS ==========
    
    def create_document(self, title: str) -> Dict[str, Any]:
        """Create a Google Doc and auto-share it"""
        doc = self.docs.documents().create(body={'title': title}).execute()
        
        # Auto-share
        self._auto_share(doc['documentId'])
        
        return doc
    
    # ========== UTILITY FUNCTIONS ==========
    
    def share_existing_file(self, file_id: str, email: str = None, role: str = 'writer'):
        """Share an existing file with someone"""
        email = email or self.owner_email
        
        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        
        return self.drive.permissions().create(
            fileId=file_id,
            body=permission,
            sendNotificationEmail=True
        ).execute()

# Global instance (singleton pattern)
_google_services = None

def get_google_services() -> GoogleServices:
    """Get or create the global GoogleServices instance"""
    global _google_services
    if _google_services is None:
        _google_services = GoogleServices()
    return _google_services

# Convenience functions
def create_spreadsheet(title: str, **kwargs) -> Dict[str, Any]:
    """Quick function to create a spreadsheet"""
    return get_google_services().create_spreadsheet(title, **kwargs)

def create_folder(name: str, **kwargs) -> Dict[str, Any]:
    """Quick function to create a folder"""
    return get_google_services().create_folder(name, **kwargs)

def upload_file(name: str, content: str, **kwargs) -> Dict[str, Any]:
    """Quick function to upload a file"""
    return get_google_services().upload_file(name, content, **kwargs)