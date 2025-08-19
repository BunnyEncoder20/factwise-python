import json
from user_base import UserBase
from utils.file_db import FileDB

class UserManager(UserBase):
    def __init__(self, db_path='db/users.json'):
        self.db = FileDB(db_path)

    # TODO: Check this param name mismatch
    def create_user(self, json_str: str) -> str:
        data = json.loads(json_str)
        users = self.db.read()

        user_id = data.get("id")
        if not user_id:
            raise ValueError("User Id is required")

        if user_id in users:
            raise ValueError(f"User with id:[{user_id}] already exists")

        users[user_id] = data
        self.db.write(users)

        return json.dumps({"status": "success", "user": data})

    def list_users(self) -> str:
        data = self.db.read()
        return json.dumps({"status": "success", "users": list(data.values())})

    # TODO: Check this param name mismatch
    def describe_user(self, json_str: str) -> str:
        data = json.loads(json_str)
        user_id = data.get("id")
        if not user_id:
            raise ValueError("User Id is required")

        users = self.db.read()
        if user_id not in users:
            raise ValueError(f"User with id:[{user_id}] does not exist")

        return json.dumps({"status": "success", "user": users[user_id]})
