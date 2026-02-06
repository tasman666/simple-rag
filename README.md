# 🤖 Simple RAG Chatbot

A local **Retrieval-Augmented Generation (RAG)** chatbot that processes PDF documents and audio files to create a searchable knowledge base. Ask questions about your documents and get AI-powered answers using a local LLM—**all running privately on your machine**.

## ✨ Features

- **📄 PDF Processing** — Extract text from PDF documents using pdfplumber
- **🎙️ Audio Transcription** — Convert MP3, WAV, and M4A files to text using OpenAI Whisper
- **🧠 Vector Search** — Semantic search using sentence-transformers and Qdrant
- **💬 Local AI** — Get answers from a locally-running LLM via Ollama (no data leaves your machine)
- **📝 Chat Logging** — All conversations saved to JSONL for review and analysis
- **🔒 Privacy-First** — All processing happens locally, your documents stay private

## 📋 Requirements

- **Python 3.13+**
- **Ollama** with the `qwen2.5:7b` model installed
- FFmpeg (required for audio transcription)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd simple-rag
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama and Download the Model

1. Install Ollama from [ollama.com](https://ollama.com)
2. Download the required model:

```bash
ollama pull qwen2.5:7b
```

### 5. Install FFmpeg (for audio transcription)

```bash
# macOS (using Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg
```

## 📁 Project Structure

```
simple-rag/
├── main.py              # Main application entry point
├── ingestion.py         # File processing (PDF & audio extraction)
├── processing.py        # Chunking, embedding, vector search & LLM calls
├── logger_config.py     # Chat logging configuration (JSONL output)
├── requirements.txt     # Python dependencies
├── chat_history.jsonl   # Conversation log (auto-generated)
├── sources/             # Place your documents here
│   ├── example.pdf
│   └── example.mp3
└── venv/                # Virtual environment
```

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `pdfplumber` | PDF text extraction |
| `openai-whisper` | Audio transcription (speech-to-text) |
| `langchain-text-splitters` | Chunking documents for vector storage |
| `sentence-transformers` | Generating embeddings (all-MiniLM-L6-v2) |
| `qdrant-client` | Vector database for semantic search |
| `ollama` | Python client for local LLM inference |

## 🎯 Usage

### 1. Add Your Documents

Place your PDF or audio files in the `sources/` directory:

```
sources/
├── document1.pdf
├── meeting-notes.mp3
└── lecture.m4a
```

**Supported formats:**
- PDF: `.pdf`
- Audio: `.mp3`, `.wav`, `.m4a`

### 2. Run the Chatbot

```bash
python main.py
```

### 3. Ask Questions

Once the chatbot loads your documents, you can start asking questions:

```
--- 🤖 RAG Chatbot Ready! ---

Ask a question (or type 'exit'): What are the main topics discussed?

AI ANSWER:
Based on the documents, the main topics discussed are...
```

Type `exit` to quit the application.

## ⚙️ How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Sources    │────▶│  Ingestion   │────▶│   Chunking   │
│ (PDF/Audio)  │     │ (Text/STT)   │     │  (800 chars) │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Ollama     │◀────│   Context    │◀────│   Qdrant     │
│  (qwen2.5)   │     │  Retrieval   │     │   (Vector)   │
└──────────────┘     └──────────────┘     └──────────────┘
       │
       ▼
  ┌─────────┐
  │ Answer  │
  └─────────┘
```

1. **Ingestion** — Documents are loaded and text is extracted (PDFs) or transcribed (audio)
2. **Chunking** — Text is split into 800-character chunks with 100-character overlap using smart separators
3. **Embedding** — Chunks are converted to vectors using `all-MiniLM-L6-v2`
4. **Storage** — Vectors are stored in an in-memory Qdrant database
5. **Query** — User questions are embedded and matched against stored chunks
6. **Generation** — Relevant chunks are sent to Ollama for answer synthesis
7. **Logging** — Each Q&A interaction is logged to `chat_history.jsonl`

## 🔧 Configuration

### Change the LLM Model

Edit `processing.py` line 86 to use a different Ollama model:

```python
response = ollama.chat(
    model='llama3.2:3b',  # Change model here
    messages=[{'role': 'user', 'content': prompt}],
)
```

### Adjust Chunk Size

Edit `processing.py` lines 21-26:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,      # Current default (larger = more context)
    chunk_overlap=100,   # Overlap for continuity
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]  # Smart split points
)
```

### Persist Vector Database

By default, the vector database is in-memory. To persist it, edit `processing.py` line 11:

```python
client = QdrantClient("./qdrant_db")  # Saves to disk
```

### Chat History

All conversations are automatically logged to `chat_history.jsonl` in JSON Lines format:

```json
{"timestamp": "2026-02-06T16:45:00", "level": "INFO", "question": "...", "answer": "...", "context_used": [...]}
```

This file is excluded from git by default.

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
