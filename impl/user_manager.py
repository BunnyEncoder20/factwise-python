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
        if not data:
            return json.dumps({"status": "success", "users": []})

        return json.dumps({"status": "success", "users": list(data.values())})
