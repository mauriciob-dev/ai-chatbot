# ⚡ AI Chatbot — RAG-Powered Conversational Assistant

A full-stack AI chatbot application with PDF document intelligence, JWT authentication, and per-user conversation history. Built with FastAPI, Groq LLM, and FAISS vector search.

---

## 🚀 Features

- **RAG Pipeline** — Upload PDF documents and chat with their content using semantic search
- **JWT Authentication** — Per-user sessions with secure token-based auth
- **Conversation History** — Persistent chat history per user, stored locally
- **Dark Mode UI** — Clean, production-grade interface built with vanilla HTML/CSS/JS
- **Fast Inference** — Powered by Groq API running LLaMA 3.3 70B at high speed
- **Local Embeddings** — HuggingFace `all-MiniLM-L6-v2` for vector search, no extra API cost

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| LLM | Groq API — `llama-3.3-70b-versatile` |
| Vector Search | FAISS + HuggingFace Embeddings |
| PDF Processing | LangChain + PyPDF |
| Authentication | JWT (python-jose) |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Railway |

---

## 📁 Project Structure

```
chatbot/
├── main.py          # FastAPI routes, JWT auth, chat logic
├── rag.py           # PDF processing, FAISS vector store
├── history.py       # Per-user conversation persistence
├── Procfile         # Railway deployment config
├── requirements.txt # Python dependencies
├── .env             # Environment variables (not committed)
├── docs/            # Upload PDFs here for indexing
└── static/
    ├── index.html   # Chat interface
    └── login.html   # Login page
```

---

## ⚙️ Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/ai-chatbot.git
cd ai-chatbot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key_for_jwt
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

**4. Add PDF documents** *(optional)*
```bash
mkdir docs
# Copy any PDF files into the docs/ folder
```

**5. Run the server**
```bash
uvicorn main:app --reload
```

Open [http://localhost:8000/login](http://localhost:8000/login) in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Chat interface |
| `GET` | `/login` | Login page |
| `POST` | `/session` | Create JWT session |
| `POST` | `/chat` | Send message (requires Bearer token) |

---

## 🧠 How RAG Works

1. PDF files in `/docs` are loaded and split into chunks on startup
2. Each chunk is converted to a vector using HuggingFace embeddings
3. Vectors are indexed in FAISS for fast similarity search
4. When a user sends a message, the top 3 most relevant chunks are retrieved
5. Retrieved context is injected into the LLM system prompt
6. The model responds based on document content

---

## 🚀 Deployment

This project is configured for deployment on [Railway](https://railway.app).

Set the following environment variables in your Railway project:
```
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key_for_jwt
```

---

## 📄 License

MIT License — feel free to use this project as a base for your own applications.