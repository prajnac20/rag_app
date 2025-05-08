# vector_store.py

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import EMBEDDING_MODEL, CHROMA_DB_DIR

def get_vector_store(document_id: str):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        collection_name=document_id,  # Now this is the filename
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIR
    )

from fastapi import APIRouter
import os


def get_all_documents():
    """
    Lists all uploaded PDFs by returning their base filename (no extension).
    This will also be used as the Chroma collection name.
    """
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        return []

    document_ids = []
    for file in os.listdir(uploads_dir):
        if file.endswith(".pdf"):
            base_name = os.path.splitext(file)[0]
            document_ids.append(base_name)

    return {"documents": document_ids}

