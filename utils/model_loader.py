import os
from typing import Literal, Optional
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")

# ------- OpenAI -------
from openai import OpenAI
_openai_client: Optional[OpenAI] = None
def _get_openai_client() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        if not OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY 未设置")
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client

def call_openai(prompt: str) -> str:
    client = _get_openai_client()
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content or ""


# ------- Gemini -------
def call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY 未设置")
    try:
        import google.generativeai as genai          # lazy import
        genai.configure(api_key=GEMINI_API_KEY)      # type: ignore
        model = genai.GenerativeModel("models/gemini-1.5-pro")  # type: ignore
        resp  = model.generate_content(prompt)
        return resp.text
    except ImportError:
        raise ImportError("请先 pip install google-generativeai")

# ------- 工厂入口 -------
def call_model(prompt: str,
               model_name: Literal["openai", "gemini"] | None = None) -> str:
    """
    model_name=None ➜ 读取环境变量 LLM_PROVIDER，默认为 "openai"
    """
    model_name = (model_name or os.getenv("LLM_PROVIDER", "openai")).lower()# type: ignore
    if model_name == "openai":
        return call_openai(prompt)
    elif model_name == "gemini":
        return call_gemini(prompt)
    else:
        raise ValueError(f"Unsupported model: {model_name}")
