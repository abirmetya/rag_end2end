# 🧠 Retrieval-Augmented Generation (RAG) Chatbot

This repository contains an **end-to-end RAG (Retrieval-Augmented Generation) workflow** integrated into a **Streamlit web app**.  
It allows users to **upload documents, manage them, and chat with an LLM** that can reference both uploaded knowledge and prior conversations for context.

---

## 🚀 Features

- **Document Management**  
  - Upload documents (PDF/TXT/MD/etc.)  
  - List available documents  
  - Delete documents  

- **Chat with Context**  
  - Supports **query contextualization** (rewrites ambiguous queries using history)  
  - Stores **previous chats in SQLite** with session IDs for persistence  
  - Retrieval of relevant chunks from uploaded docs for **RAG-powered responses**  

- **Model Flexibility**  
  - Choose from multiple **LLM backends** at runtime  
  - Custom embeddings for document storage and retrieval  

- **Backend APIs (FastAPI)**  
  - `upload_document` – Upload files  
  - `delete_document` – Remove stored docs  
  - `list_document` – Get document list  
  - `chat` – Query with contextual history  

- **Frontend (Streamlit)**  
  - Simple **UI to interact with the system**  
  - Select LLM model  
  - Upload/Delete documents  
  - Chat with memory-aware RAG  

---

## 🏗️ Architecture Overview

         ┌───────────────┐
         │   Streamlit   │  ⇦ User interacts here
         └───────┬───────┘
                 │
          (API Calls via HTTP)
                 │
     ┌───────────▼────────────┐
     │        FastAPI         │
     │ Endpoints:             │
     │  • upload_document     │
     │  • delete_document     │
     │  • list_document       │
     │  • chat                │
     └───────────┬────────────┘
                 │
    ┌────────────▼───────────────┐
    │      RAG Workflow           │
    │ ┌─────────┬──────────────┐ │
    │ │Embedder │ Retriever     │ │
    │ │ (Vector │ (DB Search)  │ │
    │ │ Store)  │               │ │
    │ └─────────┴──────────────┘ │
    │       │                     │
    │       ▼                     │
    │   Query Contextualizer      │
    │ (with SQLite Chat History)  │
    │       │                     │
    │       ▼                     │
    │         LLM                 │
    └─────────────────────────────┘


---

## 📦 Tech Stack

- **Frontend:** Streamlit  
- **Backend API:** FastAPI  
- **Database:** SQLite (for chat history + session IDs)  
- **Embeddings:** (OpenAI / HuggingFace / any chosen model)  
- **Vector Store:** (e.g., FAISS / Chroma / Pinecone — depending on config)  
- **LLMs:** (OpenAI GPT / Llama / etc. — user selectable)  

---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot

### 2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Set Environment Variables
OPENAI_API_KEY=your_key_here

▶️ Usage
1️⃣ Start Backend (FastAPI)
uvicorn main:app --reload --port 8000

2️⃣ Run Frontend (Streamlit)
streamlit run app.py

3️⃣ Interact with the App

Upload / delete documents

Choose LLM model

Ask questions and get RAG-powered answers

📂 API Endpoints
Method	Endpoint	Description
POST	/upload_document	Upload a new document
GET	/list_document	List all uploaded documents
DELETE	/delete_document	Delete a document
POST	/chat	Ask a question & get contextual ans
💾 Database (SQLite)

Table: chat_history

Columns:

id – Auto increment

session_id – Unique user session

user_query – Raw input from user

contextualized_query – Reformulated query

bot_response – LLM response

timestamp – Time of entry

This enables multi-session context retention.

🔮 Roadmap

 Add support for multi-user authentication

 Integrate advanced chunking strategies

 Add evaluation metrics for retrieval quality

 Deploy to cloud (AWS/GCP/Azure)

🤝 Contributing

Contributions are welcome!
Please open an issue or PR for any bug fixes, feature requests, or improvements.

📜 License

This project is licensed under the MIT License.