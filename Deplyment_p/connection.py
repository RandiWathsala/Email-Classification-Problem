from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def gmail_connect():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_latest_emails(service, max_results=10):
    results = service.users().messages().list(userId='me', maxResults=max_results, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    email_list = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = txt['payload']['headers']
        subject = sender = ""
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
        snippet = txt.get("snippet", "")
        labels = txt.get("labelIds", [])
        email_list.append({
            "id": msg['id'],
            "subject": subject,
            "from": sender,
            "snippet": snippet,
            "labels": labels
        })
    return email_list


def mark_as_read(service, msg_id):
    """Mark a Gmail message as read"""
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

def get_emails_by_label(service, label, max_results=10):
    """Fetch emails for a specific Gmail label (INBOX, SENT, SPAM, TRASH)"""
    results = service.users().messages().list(userId='me', maxResults=max_results, labelIds=[label]).execute()
    messages = results.get('messages', [])
    email_list = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = txt['payload']['headers']
        subject, sender = "", ""
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
        snippet = txt.get("snippet", "")
        labels = txt.get("labelIds", [])
        email_list.append({
            "id": msg['id'],
            "subject": subject,
            "from": sender,
            "snippet": snippet,
            "labels": labels
        })
    return email_list

def get_inbox_emails(service, max_results=10):
    return get_emails_by_label(service, "INBOX", max_results)

def get_sent_emails(service, max_results=10):
    return get_emails_by_label(service, "SENT", max_results)

def get_spam_emails(service, max_results=10):
    return get_emails_by_label(service, "SPAM", max_results)

def get_trash_emails(service, max_results=10):
    return get_emails_by_label(service, "TRASH", max_results)
