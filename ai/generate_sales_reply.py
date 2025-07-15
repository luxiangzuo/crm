# generate_sales_reply.py
from crm.push_to_crm import update_opportunity_note
from utils.project_utils import print_model_status
from crm.pull_from_crm import pull_from_crm
from ai.generate_sales_prompt import build_prompt

from utils.model_loader import call_model

from rag.retrieve_docs import retrieve_docs
from typing import cast, Literal

def generate_sales_reply_from_crm(opportunity_id: str, model: str = "openai"):
    # Step 1: 从 CRM 拉取机会详情
    opportunity = pull_from_crm(opportunity_id)
    if not opportunity:
        raise ValueError(f"❌ 未找到机会记录：{opportunity_id}")

    # Step 2: 提取客户信息 & 邮件内容摘要
    customer_info = {
        "name": opportunity.get("name", "Valued Customer"),
        "stage": opportunity.get("stage", "Lead"),
        "product": opportunity.get("product", "VitalSure Pro Series")
    }
    email_summary = {
        "主题": opportunity.get("description", "")
    }

    # Step 3: 检索知识段落（RAG）
    docs = retrieve_docs(email_summary["主题"])

    # Step 4: 构造 prompt 并调用模型生成邮件
    prompt = build_prompt(customer_info, email_summary, docs)
    reply = call_model(prompt, model_name=cast(Literal["openai", "gemini"], model))

    # Step 5: 将结果推送回 CRM
    update_opportunity_note(opportunity_id, reply)

    return reply