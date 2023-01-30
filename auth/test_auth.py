# testing module for auth app

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_empty_user_pass():

    response = client.post("/token",data={
        "username": "",
        "password": ""
    })

    token = response.json().get("access_token")
    message = response.json().get("detail")[0]
    assert token == None
    assert message.get("msg") == "field required"

def test_get_auth_token():

    response = client.post("/token",data={
        "username":"chandler@bing.com",
        "password":"pass123"
    })

    token = response.json().get("access_token")
    assert token