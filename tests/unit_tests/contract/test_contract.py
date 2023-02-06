import json
from tests.mock_data import user_payload, contract_payload
from models.contract import ContractModel
from tests.constants.routes_info import routes

headers = {}


def test_contracts(client, app):
    """Test to insert a contarct into the DB"""
    user_response = client.post(routes["USER"], json=user_payload)
    assert user_response.status_code == 200

    login_response = client.post(routes["LOGIN"],
                                 json={
                                     "username": user_payload["username"],
                                     "password": user_payload["password"]
                                 })
    assert login_response.status_code == 200

    access_token = json.loads(login_response.data)
    headers['Authorization'] = f'Bearer {access_token["access_token"]}'
    response = client.post(routes["CONTRACTS"],
                           json=contract_payload,
                           headers=headers)

    with app.app_context():
        assert response.status_code == 200
        assert ContractModel.query.first().name == contract_payload["name"]
        assert ContractModel.query.first(
        ).intrest == contract_payload["intrest"]


def test_invalid_contract(client, app):
    """Test to insert a invalid contarct into the DB"""
    invalid_payload = {"intrest": 15, "name": "", "total_amount": 15000.0}
    response = client.post(routes["CONTRACTS"],
                           json=invalid_payload,
                           headers=headers)
    assert response.status_code >= 400


def test_get_contracts(client, app):
    """Test to get all the avialable from the DB"""

    post_response = client.post(routes["CONTRACTS"],
                                json=contract_payload,
                                headers=headers)
    assert post_response.status_code == 200
    get_response = client.get(routes["CONTRACTS"], headers=headers)
    assert get_response.status_code == 200
    with app.app_context():
        assert ContractModel.query.count() == 1


def test_duplicate_contract_(client, app):
    """Test to check duplicate contract name while inserting into DB"""
    response = client.post(routes["CONTRACTS"],
                           json=contract_payload,
                           headers=headers)
    assert response.status_code == 200
    new_response = client.post(routes["CONTRACTS"],
                               json=contract_payload,
                               headers=headers)
    assert new_response.status_code == 400
    assert "A contract with that name already exists" in json.loads(
        new_response.data)["message"]


def test_get_contracts_by_id(client, app):
    """Test to get contract by Id"""
    response = client.post(routes["CONTRACTS"],
                           json=contract_payload,
                           headers=headers)
    assert response.status_code == 200
    contract_response = client.get(f'{routes["CONTRACTS"]}/1', headers=headers)
    assert contract_response.status_code == 200
    with app.app_context():
        assert ContractModel.query.count() == 1
        assert ContractModel.query.first().name == contract_payload["name"]
        assert ContractModel.query.first(
        ).intrest == contract_payload["intrest"]


def test_delete_contracts_by_id(client, app):
    """Test to delete a contract"""

    response = client.post(routes["CONTRACTS"],
                           json=contract_payload,
                           headers=headers)
    assert response.status_code == 200
    contract_response = client.delete(f'{routes["CONTRACTS"]}/1',
                                      headers=headers)
    assert contract_response.status_code == 202
    with app.app_context():
        assert ContractModel.query.count() == 0


def test_updating_contract(client, app):
    """Test to verify contract updation"""

    response = client.post(routes["CONTRACTS"],
                           json=contract_payload,
                           headers=headers)
    assert response.status_code == 200
    new_payload = {**contract_payload, "name": "new_contract", "intrest": 20}
    update_response = client.put(f'{routes["CONTRACTS"]}/1',
                                 json=new_payload,
                                 headers=headers)
    assert update_response.status_code >= 200
