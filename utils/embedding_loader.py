# utils/embedding_loader.py

import os
from dotenv import load_dotenv
load_dotenv()

def load_embedding_model(provider="openai"):
    provider = provider.lower()

    if provider == "openai":
        from langchain.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings()

    elif provider == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    else:
        raise ValueError(f"❌ Unsupported embedding provider: {provider}")
