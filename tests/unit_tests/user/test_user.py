import json
from models.user_data import UserDataModel
from tests.mock_data import user_payload
from tests.constants.routes_info import routes

headers = {}


def test_login(client, app):
    """Test to login into the system"""

    response = client.post(routes["USER"], json=user_payload)
    assert response.status_code == 200
    login_response = client.post(routes["LOGIN"],
                                 json={
                                     "username": user_payload["username"],
                                     "password": user_payload["password"]
                                 })
    assert login_response.status_code == 200

    access_token = json.loads(login_response.data)
    headers['Authorization'] = f'Bearer {access_token["access_token"]}'


def test_invalid_login(client):
    """Test to check login system with invalid creds"""

    response = client.post(routes["USER"], json=user_payload)
    assert response.status_code == 200

    login_response = client.post(routes["LOGIN"],
                                 json={
                                     "username": "user1",
                                     "password": "user1"
                                 })
    assert login_response.status_code == 401


def test_blank_creds(client):
    """Test to check empty creds"""

    payload = {"username": "", "password": ""}
    login_response = client.post(routes["LOGIN"], json=payload)
    assert login_response.status_code == 401


def test_user_data(client, app):
    """Test to check to existing users data in the DB"""

    response = client.get(routes["USER"])
    assert response.status_code == 200

    with app.app_context():
        assert UserDataModel.query.count() == 0


def test_adding_user_data(client, app):
    """Test to post/add user data into the DB"""

    response = client.post(routes["USER"], json=user_payload)

    with app.app_context():
        assert response.status_code == 200
        assert UserDataModel.query.first().name == user_payload["name"]
        assert UserDataModel.query.first().address == user_payload["address"]
        assert UserDataModel.query.first().phone == user_payload["phone"]
        assert UserDataModel.query.first().username == user_payload["username"]


def test_invalid_user_data(client, app):
    """Test to insert user data with missing fields/properties"""

    payload = {
        "address": "hyd",
        "phone": "121655454",
        "email": "abc@gmail.com"
    }

    response = client.post(routes["USER"], json=payload)
    with app.app_context():
        assert response.status_code == 422


def test_duplicate_user_data(client, app):
    """Test to insert duplicate user data"""

    response = client.post("/user", json=user_payload)
    assert response.status_code == 200

    new_response = client.post(routes["USER"], json=user_payload)
    assert new_response.status_code == 400


def test_update_user_data(client, app):
    """Test to update user data"""

    update_payload = {
        **user_payload,
        "name": "krishna",
    }
    response = client.post(routes["USER"], json=user_payload)

    with app.app_context():
        assert response.status_code == 200
        assert UserDataModel.query.first().name == user_payload["name"]
        assert UserDataModel.query.first().address == user_payload["address"]
        assert UserDataModel.query.first().phone == user_payload["phone"]
        assert UserDataModel.query.first().username == user_payload["username"]

    update_response = client.put(f'{routes["USER"]}/{1}', json=update_payload)
    with app.app_context():
        assert update_response.status_code == 200
        assert UserDataModel.query.first().name == update_payload["name"]
        assert UserDataModel.query.first().address == update_payload["address"]
        assert UserDataModel.query.first().phone == update_payload["phone"]
        assert UserDataModel.query.first(
        ).username == update_payload["username"]


def test_get_user_data_by_id(client, app):
    """Test to get user data by Id"""

    repsonse = client.post(routes["USER"], json=user_payload)
    assert repsonse.status_code == 200

    new_response = client.get(f"{routes['USER']}/1")

    with app.app_context():
        assert new_response.status_code == 200
        assert UserDataModel.query.first().name == user_payload["name"]


def test_user_logout(client, app):
    response = client.post(routes["USER"], json=user_payload)
    assert response.status_code == 200
    login_response = client.post(routes["LOGIN"],
                                 json={
                                     "username": user_payload["username"],
                                     "password": user_payload["password"]
                                 })
    assert login_response.status_code == 200
    logout_response = client.post('/logout', headers=headers)
    assert "Successfully logged out" in json.loads(
        logout_response.data)["message"]
