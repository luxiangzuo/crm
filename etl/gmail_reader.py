from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import json
import os
from pathlib import Path
# 设置作用域
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def init_gmail_service():
    

    BASE_DIR = Path(__file__).resolve().parent          # crm_clean/
    CLIENT_SECRET = BASE_DIR / 'data' / 'credentials.json'

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)

    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def save_email_to_jsonl(email_data, file_path='emails.jsonl'):
    with open(file_path, 'a', encoding='utf-8') as f:
        json.dump(email_data, f, ensure_ascii=False)
        f.write('\n')

def get_latest_emails(service, max_results=5, save_file='emails.jsonl'):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    print(f"\n📬 共获取到 {len(messages)} 封邮件\n")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload'].get('headers', [])

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(无主题)')
        from_addr = next((h['value'] for h in headers if h['name'] == 'From'), '(未知发件人)')

        body = ''
        parts = msg_data['payload'].get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break

        print(f"🔹 来自: {from_addr}")
        print(f"🔹 主题: {subject}")
        print(f"🔹 正文预览:\n{body[:300]}...\n")

        # 保存到 JSONL
        email_data = {
            'from': from_addr,
            'subject': subject,
            'body': body.strip()
        }
        save_email_to_jsonl(email_data, file_path=save_file)

if __name__ == '__main__':
    service = init_gmail_service()
    get_latest_emails(service, max_results=10)  # 默认读取10封邮件
