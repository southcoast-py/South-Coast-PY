from starlette.testclient import TestClient
from app.main  import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping?token=jessica")
    print(f"response : {response}")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
