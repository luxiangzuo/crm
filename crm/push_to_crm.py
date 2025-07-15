import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import config
from requests.auth import HTTPBasicAuth

import re
from datetime import date

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

valid_stages = ["New", "Qualified", "Customer", "Negotiation", "Closed Won", "Closed Lost"]

def sanitize_name(name: str) -> str:
    # 只保留字母、数字和常规字符
    return re.sub(r'[^a-zA-Z0-9_\- ]', '', name)[:50] or "Anonymous"


# 加载环境变量
load_dotenv()

# 路径配置
EMAIL_FILE = "emails_classified.jsonl"

# 读取分类后的邮件数据
def read_emails(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

# 生成认证头
def get_auth():
    # print("🚨用户名密码：", config.ESPOTCRM_USERNAME, config.ESPOTCRM_PASSWORD)
    # return HTTPBasicAuth(config.ESPOTCRM_USERNAME, config.ESPOTCRM_PASSWORD)# type: ignore
   
    username = config.ESPOTCRM_USERNAME
    password = config.ESPOTCRM_PASSWORD
    if not username or not password:
        raise ValueError("❌ 环境变量未正确加载：ESPOTCRM_USERNAME 或 ESPOTCRM_PASSWORD 缺失")
    return HTTPBasicAuth(username, password)

def push_to_lead(email):
    email_from = email.get("from", "")
    if not is_valid_email(email_from):
        print(f"⚠️ 忽略：无效邮箱地址 -> {email_from}")
        return

    stage = email.get("stage", "")
    if stage not in valid_stages:
        print(f"⚠️ 忽略：无效阶段 -> {stage}")
        return

    data = {
        "firstName": sanitize_name(email_from.split("@")[0]),
        "lastName": "(Imported)",
        "emailAddress": email_from,
        "description": email.get("body", "")[:512],
        "source": "Email",  # ✅ 改成合法值
        "stage": stage,
        "intent": email.get("intent")
    }
    return post_to_crm("Lead", data)


def push_to_opportunity(email):
    email_from = email.get("from", "")
    if not is_valid_email(email_from):
        print(f"⚠️ 忽略：无效邮箱地址 -> {email_from}")
        return

    stage = email.get("stage", "")
    if stage not in valid_stages:
        print(f"⚠️ 忽略：无效阶段 -> {stage}")
        return

    data = {
        "name": email.get("subject", "No Subject"),
        "accountName": sanitize_name(email_from.split("@")[0]),
        "description": email.get("body", "")[:512],
        "stage": stage,
        "source": "Email",  # ✅ 改成合法值
        "amount": 0,
        "closeDate": date.today().isoformat()  # ✅ 添加必填字段
    }
    return post_to_crm("Opportunity", data)


def push_to_contact(email):
    email_from = email.get("from", "")
    if not is_valid_email(email_from):
        print(f"⚠️ 忽略：无效邮箱地址 -> {email_from}")
        return

    data = {
        "firstName": sanitize_name(email_from.split("@")[0]),
        "lastName": "(Customer)",
        "emailAddress": email_from,
        "description": email.get("body", "")[:512]
    }
    return post_to_crm("Contact", data)


# 通用 POST 函数
def post_to_crm(entity, data):
    url = f"{config.ESPOTCRM_URL}/api/v1/{entity}"
    response = requests.post(url, json=data, auth=get_auth())
    if response.status_code in [200, 201]:
        print(f"✅ 导入成功: {entity} - {data.get('emailAddress') or data.get('name')}")
    else:
        print(f"❌ 导入失败: {entity} - {response.status_code}: {response.text}")




def update_opportunity_note(opportunity_id, reply_text):
    """
    将生成的 AI 回复内容更新到 CRM 中指定 Opportunity 的 description 字段。
    """
    from config import ESPOTCRM_URL
    import requests
    from .push_to_crm import get_auth  # 确保 get_auth 存在

    url = f"{ESPOTCRM_URL}/api/v1/Opportunity/{opportunity_id}"
    data = {
        "description": reply_text[:1000]  # 可根据字段限制截断
    }
    response = requests.patch(url, json=data, auth=get_auth())
    if response.status_code in [200, 204]:
        print(f"✅ 回信内容已更新至 CRM - Opportunity {opportunity_id}")
    else:
        print(f"❌ 更新失败: {response.status_code} - {response.text}")




# 主逻辑
def main():
    emails = read_emails(EMAIL_FILE)
    print(f"📦 共有 {len(emails)} 封邮件，准备分类导入 CRM...")

    for email in emails:
        stage = email.get("stage")
        if stage in ["Lead", "Qualified Lead"]:
            push_to_lead(email)
        elif stage in ["Opportunity", "Negotiation"]:
            push_to_opportunity(email)
        elif stage == "Customer":
            push_to_contact(email)
        else:
            print(f"⚠️ 忽略：无效或无关阶段 -> {email.get('subject')}")

if __name__ == "__main__":
    main()
