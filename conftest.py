import pytest
from pymongo import MongoClient

from data.const_and_func import SERVER_ADDRESS


@pytest.fixture
def get_users_from_mongo():
    client = MongoClient(f'mongodb://{SERVER_ADDRESS}', 27017)
    db = client.mestodb
    collection = db["users"]
    users= collection.find()
    print("\n")
    for user in users:
        print(user)


@pytest.fixture
def clear_users_from_mongo():
    client = MongoClient(f'mongodb://{SERVER_ADDRESS}', 27017)
    db = client.mestodb
    collection = db["users"]
    collection.delete_many({})
    print("\n")
    user = collection.find_one()
    if user is None:
        print("Setup: all users are deleted")
    else:
        print("Setup is not sucessful: not all users are deleted")



