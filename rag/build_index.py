# rag/build_index.py
from dotenv import load_dotenv
load_dotenv()

import os
from langchain.vectorstores import FAISS
from utils.embedding_loader import load_embedding_model
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter

def load_markdown_files(root_dir):
    all_chunks = []
    splitter = CharacterTextSplitter(separator="\n\n", chunk_size=500, chunk_overlap=50)

    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                filepath = os.path.join(foldername, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()

                # 加入元信息，方便之后回溯引用来源
                metadata = {
                    "source": os.path.relpath(filepath, root_dir)
                }
                chunks = splitter.split_text(text)
                for chunk in chunks:
                    all_chunks.append(Document(page_content=chunk, metadata=metadata))

    return all_chunks

def build_index(doc_dir="documents", index_dir="rag/joja_index"):
    print("🔍 正在加载并切分 Markdown 文档...")
    docs = load_markdown_files(doc_dir)

    if not docs:
        raise ValueError(f"❌ 未找到有效文档，请检查路径是否正确: {doc_dir}")

    print(f"📚 共切分出 {len(docs)} 个段落，开始生成向量...")
    embeddings = load_embedding_model("openai")  # 或 "gemini"
    vectordb = FAISS.from_documents(docs, embeddings)

    vectordb.save_local(index_dir)
    print(f"✅ 向量索引构建完成，保存在 {index_dir}")

if __name__ == "__main__":
    build_index()
