import pytest
from httpx import AsyncClient
from fastapi import status
from main import app
import os

# Path to a sample PDF file to use for upload tests
TEST_FILE_PATH = "tests/sample_test.pdf"

@pytest.mark.asyncio
async def test_upload_document():
    # Ensure test file exists
    assert os.path.exists(TEST_FILE_PATH), "Test PDF file not found."

    with open(TEST_FILE_PATH, "rb") as f:
        files = {"file": ("sample_test.pdf", f, "application/pdf")}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/upload_document/", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert "filename" in data
    global document_id
    document_id = data["document_id"]

@pytest.mark.asyncio
async def test_get_all_documents():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/get_all_documents/")
    assert response.status_code == 200
    json_data = response.json()
    assert "document_ids" in json_data
 

@pytest.mark.asyncio
async def test_search_document():
    query = "What does the document say about mental health?"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/search_document/",
            data={"document_id": document_id, "query": query}
        )

    assert response.status_code == 200
    json_data = response.json()

    assert "results" in json_data
    assert "generated_answer" in json_data