# generate_sales_reply.py
from utils.model_loader import call_model
from prompt.generate_sales_prompt import build_prompt
from rag.retrieve_docs import retrieve_docs
from typing import Literal, cast

def generate_sales_reply_from_email(name: str, email_text: str, model: str = "openai") -> str:
    customer_info = {
        "name": name,
        "stage": "Unknown",
        "product": "Unknown"
    }

    email_summary = {
        "主题": "客户邮件自动分析",
        "正文": email_text
    }

    docs = retrieve_docs(email_summary["主题"])

    prompt = build_prompt(customer_info, email_summary, docs)
    reply = call_model(prompt, model_name=cast(Literal["openai", "gemini"], model))
    return reply



if __name__ == "__main__":
    import os
    import json

    # 加载 emails_classified.jsonl 文件
    data_path = os.path.join(os.path.dirname(__file__), "../data/emails_classified.jsonl")
    
    with open(data_path, "r", encoding="utf-8") as f:
        lines = [json.loads(line.strip()) for line in f]

    # 测试前3封邮件生成回信
    for i, email in enumerate(lines[:3]):
        sender = email.get("from", "Client")
        name = sender.split('"')[1] if '"' in sender else sender.split("<")[0].strip()
        body = email.get("body", "")

        print(f"\n📨 [邮件{i+1} - 来自 {name}]\n{body}\n")
        reply = generate_sales_reply_from_email(name=name, email_text=body)
        print(f"\n✉️ [AI 回复建议]\n{reply}\n{'='*60}")
