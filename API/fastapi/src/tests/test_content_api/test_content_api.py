from starlette.testclient import TestClient
from app.main  import app

client = TestClient(app)

def test_content_api_list():
    response = client.get("/items?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

def test_content_api_Get_ById():
    response = client.get("/items/gun?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {'name': 'Portal Gun', 'item_id': 'gun'}


def test_content_api_Put_ById():
    response = client.put("/items/gun?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 403
    assert response.json() == {"detail":"You can only update the item: plumbus"}