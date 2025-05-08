# search.py

from vector_store import get_vector_store
from document_loader import load_document
from openai import OpenAI
from config import OPENAI_API_KEY, GPT_MODEL  # Use GPT_MODEL from config

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def add_document(file_path: str, document_id: str):
    """
    Load the PDF file, embed it, and add to the vector store using the document ID.
    """
    vector_store = get_vector_store(document_id)
    docs = load_document(file_path)
    vector_store.add_documents(documents=docs)
    # results = vector_store.similarity_search("tell me about dental insurance")
    # print(results)
    return True

def search_document(document_id: str, query: str, k: int = 2):
    """
    Search vector DB for similar chunks, then pass them through GPT-4.0-mini to generate a final response.
    """
    vector_store = get_vector_store(document_id)
    # print(vector_store)
    results = vector_store.similarity_search(query, k=k)
    print(results)
    # Combine content from retrieved chunks
    context = "\n".join([doc.page_content for doc in results])
    print(context)

    # Call OpenAI GPT model (GPT-4.0-mini) to generate a response based on the context
    response = client.responses.create(
        model=GPT_MODEL,  # Use GPT-4.0-mini
        input=f"Context:\n{context}\n\nQuestion: {query}\nAnswer in a single paragraph:"
    )

    # Return both raw chunks and generated answer
    return {
        "chunks": [doc.page_content for doc in results],
        "generated_answer": response.output_text.strip()  # The answer from GPT-4.0-mini
    }
