# 🎥 AskTube – YouTube Tutorial Q&A Assistant

AskTube is an AI-powered assistant that allows users to **ask questions about any YouTube tutorial** and get contextually accurate answers based on the transcript. It uses a powerful **Retrieval-Augmented Generation (RAG)** pipeline built with **LangChain**, **OpenAI**, and **FAISS**, giving you grounded answers by combining retrieval and generation from the transcript.

---

## 📌 Key Features

- 🔍 Ask any question about a YouTube tutorial
- 🧠 Accurate answers based on the transcript using RAG
- 🧾 Full support for long, complex tutorials (up to 128k tokens with GPT-4 Turbo)
- 🧰 Streamlit-based UI or optional FastAPI backend
- ⚡ Efficient, fast, and cost-aware with fallback LLM options

---

## 🧠 How It Works

1. **Transcript Fetching**: Extracts YouTube transcript using `youtube-transcript-api`.
2. **Chunking**: Breaks long transcripts into small, context-rich chunks.
3. **Embedding**: Converts chunks and questions into vector space using `sentence-transformers`.
4. **Vector Search**: Stores and retrieves relevant chunks using FAISS + MMR search.
5. **Answer Generation**: Feeds retrieved context + question into LLM (e.g., GPT-4 Turbo).

---

## 🚀 Real-World Use Cases

- 📚 Students learning from programming or math tutorials
- 💼 Professionals upskilling with webinars
- 💻 Developers understanding API walkthroughs
- 🧏 Accessibility for users unable to listen/watch videos

---

## 🏗️ Tech Stack

| Layer         | Component                            |
|---------------|--------------------------------------|
| Transcript    | `youtube-transcript-api`             |
| Chunking      | `RecursiveCharacterTextSplitter`     |
| Embeddings    | `sentence-transformers` or OpenAI    |
| Vector Store  | `FAISS`                              |
| RAG Framework | `LangChain`                          |
| LLM           | `GPT-4 Turbo` (fallback: GPT-3.5)     |
| Frontend      | `Streamlit` or `FastAPI`             |

---

## 🧪 Project Structure

AskTube/
│
├── app/ # Streamlit or FastAPI App
│ ├── main.py # Entry point
│ └── ui.py # Streamlit interface
│
├── backend/ # Backend logic (optional)
│ ├── rag_pipeline.py # End-to-end RAG logic
│ └── transcript_utils.py # Transcript fetching & preprocessing
│
├── config/ # API keys & settings
│ └── .env # OPENAI_API_KEY=your_key_here
│
├── data/ # Temporary vector store or test files
│
├── requirements.txt # Core dependencies
├── requirements-dev.txt # Dev/testing tools (optional)
├── README.md
└── .gitignore


---

## ⚙️ Installation

```bash
git clone https://github.com/nikhilitz/AskTube.git
cd AskTube

# Create virtual env
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

Add your OpenAI key to .env:
OPENAI_API_KEY=your_openai_api_key_here

🚦 Running the App
🖥️ Option 1: Run with Streamlit (UI)
streamlit run app/main.py
⚙️ Option 2: Run Backend (API)
uvicorn app.main:app --reload
💬 Prompt Format Used (RAG)
You are a helpful AI assistant. Based only on the following video transcript, answer the user's question accurately.

Transcript:
<<<insert retrieved chunks>>>

Question:
<<<user question>>>

Answer:
📦 Requirements
See requirements.txt for dependencies.
📌 This version uses the latest compatible libraries. To lock versions:
pip freeze > requirements.txt
🛡 License
MIT License – use freely with attribution.
✨ Credits
Built with ❤️ by @nikhilitz
Powered by:
LangChain
OpenAI GPT
FAISS
Streamlit / FastAPI
YouTube Transcript API
