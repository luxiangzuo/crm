# generate_sales_prompt.py

import json
from rag.retrieve_docs import retrieve_docs

def build_prompt(customer_info, email_summary, style="professional", max_docs=3):
    """
    构造用于销售邮件生成的 prompt。
    - customer_info: 客户信息 dict
    - email_summary: 客户意图/上封邮件摘要 dict
    - style: 语气控制（professional / friendly / concise）
    - max_docs: RAG 检索的文档数量
    """
    query = email_summary.get("主题", "")
    rag_context = retrieve_docs(query, top_k=max_docs)

    prompt = f"""你是 Joja MedTech Inc. 的销售代表，请根据以下信息撰写一封销售跟进邮件：

【客户信息】
{json.dumps(customer_info, indent=2, ensure_ascii=False)}

【客户邮件摘要】
{email_summary.get("主题", "无")}

【公司知识参考】
{rag_context}

【语气要求】
请使用「{style}」的语气，确保语句自然、专业、有鼓励性。可邀请客户进一步沟通或安排会议。
"""
    return prompt.strip()


# ✅ 测试示例
if __name__ == "__main__":
    dummy_customer = {
        "姓名": "Dr. Schneider",
        "公司": "MediHealth GmbH",
        "国家": "德国",
        "阶段": "Qualified Lead",
        "角色": "医疗采购负责人"
    }

    dummy_summary = {
        "主题": "客户对 ECG S3 的 CE 认证与远程部署方式感兴趣"
    }

    prompt = build_prompt(dummy_customer, dummy_summary)
    print("📝 拼好的 Prompt：\n")
    print(prompt)
