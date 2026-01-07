# Context-Aware Document Q&A System (RAG)

A lightweight, high-performance **Retrieval-Augmented Generation (RAG)** pipeline that enables users to "chat" with their enterprise documents (PDFs). 

Built using **LangChain**, **FastAPI**, **FAISS**, and **Llama-3.1 (via Groq)**, this system ensures factual responses by retrieving relevant context before answering questions.

---

## 🚀 Features

*   **⚡ Fast Inference:** Uses **Llama-3.1-8B** via Groq Cloud for near-instant answers.
*   **🧠 Context-Aware:** Implements recursive chunking with overlap to preserve semantic meaning across document splits.
*   **🔍 Efficient Search:** Uses **FAISS (Facebook AI Similarity Search)** for local, low-latency vector retrieval.
*   **🛠️ Production Ready:** Fully Dockerized with a **FastAPI** backend for easy deployment.
*   **📂 Easy Ingestion:** Automatically processes and indexes PDFs placed in the `data/` directory.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.9+
*   **Framework:** FastAPI
*   **Orchestration:** LangChain
*   **Vector Store:** FAISS (CPU)
*   **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
*   **LLM:** Llama-3.1-8B-Instant (via Groq)
*   **Containerization:** Docker

---

## 📂 Directory Structure

```text
rag-project/
│
├── data/                  # 📂 Place your PDF files here
├── vector_store/          # 💾 FAISS index is saved here (auto-generated)
├── src/
│   ├── ingestion.py       # ⚙️ Logic to load PDFs, chunk text, and embed
│   ├── rag_engine.py      # 🧠 LLM setup and RAG retrieval chain
│   └── utils.py           # 🔧 Helper functions (logging, etc.)
├── main.py                # 🚀 FastAPI application entry point
├── Dockerfile             # 🐳 Docker configuration
├── requirements.txt       # 📦 Python dependencies
├── .env                   # 🔑 API Keys
└── README.md              # 📄 Documentation
```

---

## ⚡ Quick Start (Local)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd rag-project
```

### 2. Set up Environment
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory:
```bash
touch .env
```
Add your Groq API Key (Get one for free at [console.groq.com](https://console.groq.com/keys)):
```properties
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Ingest Data
Place your PDF files (e.g., `resume.pdf`) inside the `data/` folder. Then run:
```bash
python -m src.ingestion
```
*You should see a message: "Vector Store created at ./vector_store"*

### 5. Run the Server
```bash
uvicorn main:app --reload
```
Access the API at: `http://127.0.0.1:8000/docs`

---

## 🐳 Running with Docker

### 1. Build the Image
```bash
docker build -t rag-app .
```

### 2. Run the Container
Pass your API key as an environment variable:
```bash
docker run -p 8000:8000 -e GROQ_API_KEY=gsk_xxxxxx rag-app
```

---

## 📡 API Endpoints

### 1. Train / Update Database
Refreshes the vector store with any new PDFs in the `data/` folder.
*   **URL:** `/train`
*   **Method:** `POST`
*   **Response:** `{"status": "success", "message": "Vector store updated..."}`

### 2. Query Documents
Ask a question based on the uploaded documents.
*   **URL:** `/query`
*   **Method:** `POST`
*   **Body:**
    ```json
    {
      "query": "What are the candidate's core skills?"
    }
    ```
*   **Response:**
    ```json
    {
      "answer": "The candidate is skilled in Python, LangChain, and Docker...",
      "sources": ["data/resume.pdf"]
    }
    ```

---

## 🔧 How It Works (Pipeline)

1.  **Ingestion:**
    *   PDFs are loaded using `PyPDFLoader`.
    *   Text is split into chunks of 500 characters with 50-character overlap (preserves context).
    *   Chunks are converted to vectors using `all-MiniLM-L6-v2`.
    *   Vectors are stored locally in FAISS.

2.  **Retrieval:**
    *   User asks a question.
    *   The question is embedded into a vector.
    *   FAISS finds the top 3 most similar text chunks.

3.  **Generation:**
    *   The **Llama-3.1** model receives a prompt containing:
        *   System Instruction ("You are a helpful HR assistant...")
        *   The Retrieved Context.
        *   The User's Question.
    *   The LLM generates an answer based *only* on the provided context.

---

## 🔮 Future Improvements

*   Add support for different file types (Docx, TXT).
*   Add "Chat History" memory for follow-up questions.
*   Deploy to AWS/GCP using Docker Compose.
*   Implement Hybrid Search (Keyword + Vector) for better accuracy.
