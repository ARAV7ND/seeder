from dotenv import load_dotenv
import os
load_dotenv()
user_payload = {
    "name": "yashwanth",
    "address": "hyderabad",
    "phone": 121655454,
    "username": "user",
    "password": os.getenv("DEFAULT_KEY")
}
contract_payload = {
    "duration": "13 months",
    "intrest": 15,
    "name": "contract4",
    "total_amount": 15000.0
}

cash_kick_payload = {
    "user_id": 1,
    "name": "loan for inventory",
    "total_amount": 10000,
    "status": "pending"
}