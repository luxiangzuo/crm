import os
from dotenv import load_dotenv
from pydantic import SecretStr


load_dotenv()

def load_embedding_model(provider: str | None = None):
    """
    provider 可选:
      - "openai"   ➜ 使用 text-embedding-ada-002
      - "gemini"   ➜ 使用 models/embedding-001
    若 provider=None 则自动读取环境变量 EMBEDDING_PROVIDER，默认为 "openai"
    """
    provider = (provider or os.getenv("EMBEDDING_PROVIDER", "openai")).lower()

    if provider == "openai":
        from langchain.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings()

    elif provider == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ 未设置 GEMINI_API_KEY")
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=SecretStr(api_key)
        )

    else:
        raise ValueError(f"❌ Unsupported embedding provider: {provider}")
