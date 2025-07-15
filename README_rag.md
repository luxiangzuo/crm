# 🧠 Joja MedTech - RAG 模块说明

本模块为 Joja 智能销售邮件生成系统提供检索增强能力（RAG），用于根据客户问题自动引用公司知识文档，生成个性化销售邮件。

---

## 📁 文件结构说明

```
rag/
├── documents/              # Joja 产品与政策文档（Markdown格式）
│   ├── products/...
│   ├── pricing/...
│   └── ...
│
├── joja_index/             # FAISS 向量索引目录（build_index.py 生成）
│
├── build_index.py          # ✅ 将 documents 文档向量化并构建索引
├── retrieve_docs.py        # ✅ 根据客户问题检索文档段落
```

---

## 🛠 运行流程

### ✦ 第 1 步：构建知识向量索引（仅需一次）

```bash
python rag/build_index.py
```

- 输入：rag/documents/ 中所有 .md 文件
- 输出：rag/joja_index/ 中的向量数据库

---

### ✦ 第 2 步：从知识库中检索相关段落

```python
from rag.retrieve_docs import retrieve_docs

query = "客户咨询 ECG S3 的 CE 认证与安装方式"
docs = retrieve_docs(query, top_k=3)

print(docs)
```

- 输出：匹配 query 的 3 条文档内容段落，可拼接进 prompt

---

## 💡 使用建议

- 向量库构建一次后即可重复使用
- 文档更新后需重新运行 build_index.py
- retrieve_docs 可用于邮件生成、客服问答、FAQ 展示等多种用途

---

## ✅ 依赖环境

推荐环境：Python 3.10  
依赖库（建议写入 requirements.txt）:

```
openai
langchain
faiss-cpu
tiktoken
python-dotenv
```

---

🦊 若有任何问题，请联系鸮鸮或妎妎技术部小狐狸