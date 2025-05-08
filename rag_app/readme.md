# 🧠 RAG APP API — Documentation

## 📘 Overview

This FastAPI application allows users to:
1. Upload PDF files.
2. Convert their contents into vector embeddings using OpenAI Embeddings (`text-embedding-3-large`).
3. Store them in ChromaDB using the PDF filename (without extension) as the **collection name**.
4. Search specific documents using natural language queries, with results post-processed by a GPT-4o-mini model.

---

## 📁 Project Structure

```
pdf_search_app/
├── main.py                # FastAPI routes
├── vector_store.py        # Vector store logic (ChromaDB)
├── document_loader.py     # PDF loader (PyPDFLoader)
├── config.py              # Configuration (OpenAI model, paths)
├── requirements.txt       # Dependencies
├── uploads/               # Stores uploaded PDF files
├── chroma_langchain_db/   # ChromaDB persistence directory
```

---

## ⚙️ Configuration

### `config.py`

```python
EMBEDDING_MODEL = "text-embedding-3-large"
GPT_MODEL = "gpt-4o-mini"
CHROMA_DB_DIR = "chroma_langchain_db"
```

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your-key-here    # Linux/macOS
# or
set OPENAI_API_KEY=your-key-here       # Windows (Command Prompt)
```

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run FastAPI server

```bash
uvicorn main:app --reload
```



## 📌 Endpoints

### 1. **Upload PDF Document**

- **Method**: `POST`
- **Endpoint**: `/upload_document/`
- **Body Type**: `form-data`
- **Form Key**: `file` (type: File)
- **Response**:
  ```json
  {
    "message": "Document uploaded",
    "document_id": "filename_without_extension",
    "filename": "filename.pdf"
  }
  ```

---

### 2. **Get All Documents**

- **Method**: `GET`
- **Endpoint**: `/get_all_documents/`
- **Response**:
  ```json
  {
    "documents": ["mental_health", "data_policy"]
  }
  ```

---

### 3. **Search Document**

- **Method**: `POST`
- **Endpoint**: `/search_document/`
- **Body Type**: `form-data`
  - **document_id**: PDF name without `.pdf`
  - **query**: Search query
- **Response**:
  ```json
  {
    "query": "Mental health support",
    "result": [
      {
        "page_content": "Relevant text from PDF..."
      }
    ],
    "gpt_summary": "A GPT-generated answer or summary based on results."
  }
  ```

---

## 🤖 LLM Integration

- Uses `OpenAIEmbeddings` for vectorization (text-embedding-3-large).
- Uses `gpt-4o-mini` for summarizing search results.

---

## 🗃️ Data Handling

- PDF files are stored in `/uploads/`.
- ChromaDB stores vectorized documents in `/chroma_langchain_db/`, with the PDF name as the collection name.

---

## 📦 Dependencies (`requirements.txt`)

```txt
fastapi
uvicorn
openai
langchain
langchain-openai
langchain-community
langchain-chroma
PyPDF2
tqdm
```

---

## 🛠️ Future Improvements

- Store metadata in SQLite for robust tracking
- Add delete or update document endpoint
- Pagination support in search results
- File overwrite prevention or confirmation
- Supporting different file formats

## 📥 Postman Collection

A Postman collection is attached to this project for easy testing of the API endpoints.  
You can import it into Postman and test all endpoints including file upload, document retrieval, and search