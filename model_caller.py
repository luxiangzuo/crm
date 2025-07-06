# model_caller.py


from typing import Literal, Optional
import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI

# === 加载 .env 中的环境变量 ===
load_dotenv()

# === 获取 API KEY ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === 初始化客户端 ===
genai.configure(api_key=GEMINI_API_KEY) # type: ignore


openai_client = OpenAI(api_key=OPENAI_API_KEY)

# === 通用调用函数 ===
def call_model(prompt: str, model_name: Literal["gemini", "openai"] = "gemini") -> Optional[str]:
    if model_name == "gemini":
        model = genai.GenerativeModel("models/gemini-1.5-pro")# type: ignore

        response = model.generate_content(prompt)
        return response.text if response else None

    elif model_name == "openai":
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content if response else None

    else:
        raise ValueError(f"Unsupported model name: {model_name}")


# from model_caller import call_model

# output = call_model("请将以下英文邮件归类", model_name="gemini")
# 或
# output = call_model("请将以下英文邮件归类", model_name="openai")
