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
