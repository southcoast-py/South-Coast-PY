from starlette.testclient import TestClient
from app.main  import app

client = TestClient(app)

def test_ping():
    response = client.post("/admin/?token=jessica",
        headers={"X-Token": "fake-super-secret-token"})
    print(f"response : {response}")
    assert response.status_code == 200
    assert response.json() == {"message": "Admin getting schwifty"}
