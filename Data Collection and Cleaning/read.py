from __future__ import print_function
import os.path
import base64
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import email

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_emails(service, max_results=50):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    email_data = []

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = txt['payload']
        headers = payload['headers']

        subject = None
        sender = None
        date = None
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
            if d['name'] == 'Date':
                date = d['value']

        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode("utf-8")
                    break
        else:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode("utf-8")

        email_data.append({
            'subject': subject,
            'from': sender,
            'date': date,
            'body': body,
            'gmail_labels': txt.get('labelIds', [])
        })

    return email_data

if __name__ == '__main__':
    service = get_gmail_service()
    emails = get_emails(service, max_results=500)  

    df = pd.DataFrame(emails)
    df.to_csv("emails_dataset.csv", index=False)
    print("saved to emails_dataset.csv")
