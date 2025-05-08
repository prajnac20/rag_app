# document_loader.py

from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path: str):
    """
    Load a PDF document from the given path and return a list of pages as Document objects.
    """
    loader = PyPDFLoader(file_path)
    return loader.load()
