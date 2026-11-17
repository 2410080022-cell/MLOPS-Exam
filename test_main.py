from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@patch("main.generate_llm_answer")
def test_ask_valid_question(mock_llm):
    mock_llm.return_value = "Photosynthesis is the process by which plants convert light energy into chemical energy."
    response = client.post("/ask", json={"question": "What is photosynthesis?"})
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "What is photosynthesis?"
    assert "Photosynthesis" in data["answer"]

def test_ask_invalid_input_empty():
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422

def test_ask_invalid_input_missing_field():
    response = client.post("/ask", json={"wrong_field": "Hello"})
    assert response.status_code == 422
