# rag/retrieve_docs.py

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def load_vectorstore(index_path="rag/joja_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)


def retrieve_docs(query, top_k=3):
    db = load_vectorstore()
    results = db.similarity_search(query, k=top_k)
    return "\n\n".join([f"[{i+1}] {doc.page_content}" for i, doc in enumerate(results)])
