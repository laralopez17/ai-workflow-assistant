from fastapi.testclient import TestClient

from ai_workflow_assistant.main import app

client = TestClient(app)


def test_health_returns_expected_payload() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ai-workflow-assistant",
        "version": "0.1.0",
    }
