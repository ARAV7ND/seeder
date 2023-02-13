import json
from models.cash_kick import CashKickModel
from tests.mock_data import cash_kick_payload, user_payload, contract_payload
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


def test_cash_kicks(client, app):
    """Test to insert cash_kicks in to the DB"""

    user_response = client.post(routes["USER"], json=user_payload)
    assert user_response.status_code == 200

    cash_kick_response = client.post(routes["CASH_KICK"],
                                     json=cash_kick_payload)

    with app.app_context():
        assert cash_kick_response.status_code == 201
        assert CashKickModel.query.first().name == cash_kick_payload["name"]
        assert CashKickModel.query.first(
        ).total_amount == cash_kick_payload["total_amount"]
        assert CashKickModel.query.first(
        ).status == cash_kick_payload["status"]


def test_creating_cash_kick(client, app):
    """Test to insert cash_kicks in to the DB using contract_id and cash_kick_id"""

    user_response = client.post(routes["USER"], json=user_payload)
    assert user_response.status_code == 200
    contract_response = client.post(routes["CONTRACTS"],
                                    json=contract_payload,
                                    headers=headers)
    assert contract_response.status_code == 200

    cash_kick_response = client.post(routes["CASH_KICK"],
                                     json=cash_kick_payload)
    with app.app_context():
        assert cash_kick_response.status_code == 201
        assert CashKickModel.query.first().name == cash_kick_payload["name"]
        assert CashKickModel.query.first(
        ).total_amount == cash_kick_payload["total_amount"]
        assert CashKickModel.query.first(
        ).status == cash_kick_payload["status"]

    cash_kick_contracts_response = client.post("cash_kicks/1/contracts/1")
    assert cash_kick_contracts_response.status_code == 201


def test_cash_kick_get_by_id(client, app):
    """Test to get cash_kicks by id from the DB"""

    user_response = client.post(routes["USER"], json=user_payload)
    assert user_response.status_code == 200

    login_response = client.post(routes["LOGIN"],
                                 json={
                                     "username": user_payload["username"],
                                     "password": user_payload["password"]
                                 })
    assert login_response.status_code == 200

    contract_response = client.post(routes["CONTRACTS"],
                                    json=contract_payload,
                                    headers=headers)
    assert contract_response.status_code == 200

    cash_kick_response = client.post(routes["CASH_KICK"],
                                     json=cash_kick_payload)
    assert cash_kick_response.status_code == 201

    new_response = client.get(f'{routes["CASH_KICK"]}/1', headers=headers)
    assert new_response.status_code == 200


def test_cash_kick_update(client, app):
    """Test to update cash kicks"""
    user_response = client.post(routes["USER"], json=user_payload)
    assert user_response.status_code == 200

    login_response = client.post(routes["LOGIN"],
                                 json={
                                     "username": user_payload["username"],
                                     "password": user_payload["password"]
                                 })
    assert login_response.status_code == 200
    contract_response = client.post(routes["CONTRACTS"],
                                    json=contract_payload,
                                    headers=headers)
    assert contract_response.status_code == 200

    cash_kick_response = client.post(routes["CASH_KICK"],
                                     json=cash_kick_payload)
    assert cash_kick_response.status_code == 201
    updated_payload = {
        "user_id": 1,
        "name": "loan for maintainence",
        "total_amount": 15000,
        "status": "pending"
    }
    updated_response = client.put(f"{routes['CASH_KICK']}/1",
                                  json=updated_payload,
                                  headers=headers)
    assert updated_response.status_code == 200
    with app.app_context():
        assert CashKickModel.query.first(
        ).user_id == updated_payload["user_id"]
        assert CashKickModel.query.first().name == updated_payload["name"]
        assert CashKickModel.query.first(
        ).total_amount == updated_payload["total_amount"]
        assert CashKickModel.query.first().status == updated_payload["status"]


def test_cash_kick_delete(client, app):
    """Test to update cash kicks"""
    user_response = client.post(routes["USER"], json=user_payload)
    assert user_response.status_code == 200

    login_response = client.post(routes["LOGIN"],
                                 json={
                                     "username": user_payload["username"],
                                     "password": user_payload["password"]
                                 })
    assert login_response.status_code == 200

    contract_response = client.post(routes["CONTRACTS"],
                                    json=contract_payload,
                                    headers=headers)
    assert contract_response.status_code == 200

    cash_kick_response = client.post(routes["CASH_KICK"],
                                     json=cash_kick_payload)
    assert cash_kick_response.status_code >= 200

    delete_response = client.delete(f"{routes['CASH_KICK']}/1",
                                    headers=headers)
    assert delete_response.status_code >= 200


def test_to_get_cash_kick_list(client, app):
    """Test to get list of available cash kicks"""

    user_response = client.post(routes["USER"], json=user_payload)
    assert user_response.status_code == 200

    cash_kick_response = client.post(routes["CASH_KICK"],
                                     json=cash_kick_payload)
    assert cash_kick_response.status_code == 201

    new_response = client.get(routes["CASH_KICK"], headers=headers)
    with app.app_context():
        assert new_response.status_code == 200
        assert CashKickModel.query.count() == 1
