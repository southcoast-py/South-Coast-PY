from starlette.testclient import TestClient
from app.main  import app

client = TestClient(app)

def test_user_api():
    response = client.get("/users/me?token=jessica")
    assert response.status_code == 200
    assert response.json() == {"username": "SouthCoastPY"}

def test_user_api_list():
    response = client.get("/users?token=jessica")
    assert response.status_code == 200
    assert response.json() == [{"username": "SouthCoastPY"},{"username": "Rick"}, {"username": "Morty"}]

def test_user_api_ByName():
    response = client.get("/users/SouthCoastPY?token=jessica")
    assert response.status_code == 200
    assert response.json() == {"username": "SouthCoastPY"}