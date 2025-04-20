import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from api.http_router import router

# Tạo FastAPI app và include router để test
app = FastAPI()
app.include_router(router)

client = TestClient(app)


@pytest.mark.asyncio
@patch("api.http_router.run_agent_http", new_callable=AsyncMock)
async def test_search_endpoint_success(mock_run_agent_http):
    mock_run_agent_http.return_value = "Mocked response from agent"

    session_id = "test-session"
    prompt = "What is the latest paper on AI?"

    response = client.get(f"/search/{session_id}", params={"prompt": prompt})

    assert response.status_code == 200
    assert response.json() == {"response": "Mocked response from agent"}
    mock_run_agent_http.assert_awaited_once_with(prompt=prompt, session_id=session_id, agent_name="search")


@pytest.mark.asyncio
@patch("api.http_router.run_agent_http", new_callable=AsyncMock)
async def test_search_endpoint_failure(mock_run_agent_http):
    mock_run_agent_http.return_value = None  # Giả lập lỗi

    session_id = "test-session"
    prompt = "This will fail"

    response = client.get(f"/search/{session_id}", params={"prompt": prompt})

    assert response.status_code == 500
    assert response.json()["detail"] == "Agent execution failed or produced no response."
    mock_run_agent_http.assert_awaited_once()

def test_search_endpoint_missing_prompt():
    session_id = "test-session"

    response = client.get(f"/search/{session_id}")  # Không truyền prompt

    assert response.status_code == 422  # Unprocessable Entity do thiếu prompt