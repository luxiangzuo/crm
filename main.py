# main.py
from ai.generate_sales_reply import generate_sales_reply_from_crm as generate_sales_reply

if __name__ == "__main__":
    # 模拟点击按钮 1：生成 AI 回信
    test_id = "68679e913fb847d5a"          # CRM 里的 Opportunity ID
    print(generate_sales_reply(test_id))   # 运行生成并回写
    