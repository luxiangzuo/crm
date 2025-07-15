import os
from dotenv import load_dotenv
from typing import Literal, Optional

load_dotenv()

# === 提取 API 密钥（提前放好，不强制依赖）===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# === Gemini 调用 ===
def call_gemini(prompt: str) -> Optional[str]:
    if not GEMINI_API_KEY:
        raise ValueError("❌ 未设置 GEMINI_API_KEY")

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)  # 配置 Gemini
        model = genai.GenerativeModel("models/gemini-1.5-pro")  # type: ignore
        response = model.generate_content(prompt)
        return response.text if response else None
    except ImportError:
        raise ImportError("请先安装 `google-generativeai`：pip install google-generativeai")


# === OpenAI 调用 ===
def call_openai(prompt: str) -> Optional[str]:
    if not OPENAI_API_KEY:
        raise ValueError("❌ 未设置 OPENAI_API_KEY")

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content if response else None
    except ImportError:
        raise ImportError("请先安装 `openai`：pip install openai")


# === 通用工厂封装 ===
def call_model(prompt: str, model_name: Literal["gemini", "openai"] = "gemini") -> Optional[str]:
    if model_name == "gemini":
        return call_gemini(prompt)
    elif model_name == "openai":
        return call_openai(prompt)
    else:
        raise ValueError(f"❌ Unsupported model name: {model_name}")
