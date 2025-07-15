# classify_emails.py
"""
主业务逻辑：读取邮件 → 生成 Prompt → 调用模型 → 提取结果 → 写入文件
使用封装模块：generate_prompt.py + model_caller.py + project_utils.py
"""
import json
import time
import re

from utils.model_loader import call_model
from ai.generate_prompt import generate_prompt
from project_utils import print_model_status, log_result, get_current_model

INPUT_FILE = "emails.jsonl"
OUTPUT_FILE = "emails_classified.jsonl"

def extract_json(text):
    try:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None

def classify_email(email):
    prompt = generate_prompt(email)
    try:
        content = call_model(prompt)
        return extract_json(content)
    except Exception as e:
        print(f"❌ Model call failed: {e}")
        return None

def classify_email_with_retry(email, retries=3, delay=3):
    for attempt in range(retries):
        try:
            label = classify_email(email)
            if label:
                result = {
                    "from": email["from"],
                    "subject": email["subject"],
                    "body": email["body"],
                    "intent": label.get("intent", "unknown"),
                    "stage": label.get("stage", "unknown"),
                    "model_used": get_current_model()
                }
                return result
        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    return None

def main():
    print_model_status()

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        emails = [json.loads(line.strip()) for line in f if line.strip()]

    output = []
    for i, email in enumerate(emails):
        print(f"\n⏳ Processing email {i+1}/{len(emails)}...")
        result = classify_email_with_retry(email)
        if result:
            output.append(result)
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as out_f:
                json.dump(result, out_f, ensure_ascii=False)
                out_f.write('\n')
            log_result(i + 1, "✔ success", result["model_used"])
        else:
            print(f"⚠️ Email {i+1} failed after retries.")
        time.sleep(2)

    print(f"\n✅ Done! {len(output)} emails classified. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
