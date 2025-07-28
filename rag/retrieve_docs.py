# rag/retrieve_docs.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings


def load_vectorstore(index_path="rag/joja_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)


def retrieve_docs(query, top_k=3):
    db = load_vectorstore()
    results = db.similarity_search(query, k=top_k)
    # 🧠 打印检索到的文档段
    print("🔍 召回文档段落如下：")
    for i, doc in enumerate(results):
        print(f"[段落{i+1}]\n{doc.page_content}\n---")
    return "\n\n".join([f"[{i+1}] {doc.page_content}" for i, doc in enumerate(results)])
