# main.py

from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
import uuid
from search import add_document, search_document
from vector_store import get_all_documents

app = FastAPI()


@app.post("/upload_document/")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF file, save it locally, and use its name (without extension) as collection ID.
    """
    # Get the base filename without extension
    filename_only = os.path.splitext(file.filename)[0]

    # Save file in uploads directory using the exact same name
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", f"{filename_only}.pdf")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Use filename_only as both the collection name and document ID
    add_document(file_path, filename_only)

    return {
        "message": "Document uploaded",
        "document_id": filename_only,
        "filename": file.filename
    }


@app.get("/get_all_documents/")
async def list_documents():
    """
    Return a list of all document IDs available in the vector DB.
    """
    documents = get_all_documents()
    return {"document_ids": documents}


@app.post("/search_document/")
async def search_in_document(document_id: str = Form(...), query: str = Form(...)):
    """
    Perform a search query against a selected document using its ID,
    then pass context through GPT to generate a final answer.
    """
    result = search_document(document_id, query)
    return {
        "results": result["chunks"],
        "generated_answer": result["generated_answer"]
    }

