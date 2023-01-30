# testing module for article app

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_articles_by_creator_id():

    response = client.post("/token",data={
        "username":"chandler@bing.com",
        "password":"pass123"
    })

    access_token = response.json().get("access_token")

    assert access_token

    response = client.get("/articles/1",headers={
        "Authorization":"bearer " + access_token
    })
    assert response.status_code == 200

