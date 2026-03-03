# 📄 LangGraph PDF RAG Chatbot

An advanced **Multi-Threaded PDF Chatbot** built with **LangGraph, LangChain, HuggingFace, FAISS, and Streamlit**.

This chatbot allows you to:

- 💬 Chat with an LLM
- 📄 Upload and query PDFs (RAG)
- 🌐 Search the web
- 📈 Fetch real-time stock prices
- 🧮 Perform calculations
- 🧵 Maintain multiple chat threads with memory
- 💾 Persist conversation history using SQLite

---

# 🚀 Live Demo

👉 **Try it here:**  
https://zdqcde63ocfjgd6qdowhy4.streamlit.app/

---

## 🚀 Features

- Multi-threaded conversations (each chat has its own memory)
- PDF ingestion with FAISS vector store
- Retrieval-Augmented Generation (RAG)
- Tool calling support:
  - Web search (DuckDuckGo)
  - Calculator
  - Stock price fetcher (Alpha Vantage)
- Streaming responses
- SQLite checkpointing
- Streamlit UI

---

## 🧠 Architecture Overview

### 🔹 Backend – LangGraph + RAG

- Built using **LangGraph StateGraph**
- Tool calling enabled
- SQLite checkpoint memory
- Per-thread FAISS retrievers
- HuggingFace LLM endpoint (`openai/gpt-oss-20b`)
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`

### 🔹 Frontend – Streamlit

- Multiple chat threads
- Per-thread PDF upload
- Real-time streaming responses
- Sidebar thread manager

---

## 🏗️ Tech Stack

- LangChain
- LangGraph
- HuggingFace Inference API
- FAISS
- Streamlit
- SQLite
- Python

---
## 📄 How PDF RAG Works

1. Upload a PDF
2. PDF is:
   - Loaded via `PyPDFLoader`
   - Split into chunks
   - Embedded
   - Stored in FAISS
3. When user asks about document → `rag_tool` retrieves context
4. Context injected into LLM response

---

## 🧵 Multi-Thread System

- Unique `thread_id` per chat
- SQLite stores conversation state
- Each thread can have its own PDF
- Past conversations reloadable

---

## 🛠️ Project Structure

```
├── back_rag.py
├── front_chat.py
├── chatbot_db
├── .env
├── requirements.txt
└── README.md
```

---

## 📌 Future Improvements

- Docker deployment
- Authentication
- Environment-based API key handling
- Vector DB persistence
- Citation highlighting in responses

---

## 👨‍💻 Author

Suraj  

---

## 📜 License

MIT License
