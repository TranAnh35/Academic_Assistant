import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from unittest.mock import AsyncMock, patch
from api.websocket_router import router
from fastapi import FastAPI
import asyncio
import json

# Setup test app
app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
@patch("api.websocket_router.get_agent")
@patch("api.websocket_router.start_agent_session")
async def test_websocket_endpoint_success(mock_start_session, mock_get_agent):
    # Mock dữ liệu session
    mock_events = AsyncMock()
    mock_events.__aiter__.return_value = [
        # Một sự kiện giả định từ agent
        type("Event", (), {
            "turn_complete": False,
            "interrupted": False,
            "error": None,
            "content": type("Content", (), {"parts": [type("Part", (), {"text": "Hello from agent"})]}),
            "is_partial_response": lambda self: True,
            "is_final_response": lambda self: False
        })()
    ]

    mock_queue = AsyncMock()

    mock_get_agent.return_value = "mock_agent"
    mock_start_session.return_value = (mock_events, mock_queue)

    client = TestClient(app)
    with client.websocket_connect("/search/session123") as websocket:
        # Gửi tin nhắn từ client đến agent
        websocket.send_text("Hi from client")
        
        # Nhận phản hồi từ agent
        response = websocket.receive_text()
        response_data = json.loads(response)
        assert "message" in response_data
        assert response_data["message"] == "Hello from agent"

@pytest.mark.asyncio
@patch("api.websocket_router.get_agent")
async def test_websocket_endpoint_invalid_agent(mock_get_agent):
    # Khi agent không tồn tại
    mock_get_agent.side_effect = ValueError("Unknown agent name")

    client = TestClient(app)
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/invalid_agent/session456") as websocket:
            pass  # Sẽ raise lỗi do đóng WebSocket