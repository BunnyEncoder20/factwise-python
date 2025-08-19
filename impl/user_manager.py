import json
import uuid
import datetime

from user_base import UserBase
from utils.file_db import FileDB

class UserManager(UserBase):
    def __init__(self, db_path='db/users.json'):
        self.db = FileDB(db_path)

    def _validate_name(self, name: str, max_len: int):
        if not name or len(name) > max_len:
            raise ValueError(f"Name must be 1-{max_len} characters\nGiven name length: {len(name)}")

    def create_user(self, request: str) -> str:
        data = json.loads(request)
        name = data.get("name")
        display_name = data.get("display_name")

        # validate names
        self._validate_name(name, 64)
        self._validate_name(display_name, 64)

        users = self.db.read()

        # username must be unique
        if any(user["name"] == name for user in users.values()):
            raise ValueError(f"username: <{name}> already exists")

        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "name": name,
            "display_name": display_name,
            "description": f"User {display_name}",
            "created_at": datetime.datetime.now().isoformat()
        }
        users[user_id] = user
        self.db.write(users)

        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users = self.db.read()
        results = [
            {
                "name": user["name"],
                "display_name": user["display_name"],
                "created_at": user["created_at"]
            } for user in users.values()
        ]
        return json.dumps(results)


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

    def update_user(self, json_str: str) -> str:
        data = json.loads(json_str)
        users = self.db.read()

        user_id = data.get("id")
        if not user_id:
            raise ValueError("User Id is required")

        if user_id not in users:
            raise ValueError(f"User with id:[{user_id}] does not exist")

        users[user_id] = data.get("user")
        self.db.write(users)

        return json.dumps({"status": "success", "user": data})
