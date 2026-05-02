# 📚 Study Buddy — AI Tutor

A RAG-powered app that lets you upload any PDF and chat with it.
Ask questions, get answers grounded in the actual document.

## 🧠 How it works
1. Upload a PDF
2. System splits it into chunks
3. Chunks are embedded and stored in a vector database
4. You ask a question → relevant chunks are retrieved
5. AI generates an answer based on those chunks

## 🛠️ Tech Stack
- Python
- Ollama (local AI, 100% private)
- Mistral 7b model
- ChromaDB (vector database)
- PyPDF2 (PDF reading)
- Streamlit (UI)

## 🚀 Progress
- [x] Day 1 — Local AI setup with Ollama
- [x] Day 2 — PDF reading and chunking
- [x] Day 3 — Embeddings and ChromaDB
- [x] Day 4 — RAG chain
- [x] Day 5 — Streamlit UI

## ⚙️ Setup
```bash
git clone https://github.com/Mariem1233/study-buddy
cd study-buddy
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
ollama pull mistral:7b
```

## 📌 Status
✅ Complete — Working local RAG app
