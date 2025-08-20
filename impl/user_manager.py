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
            "creation_time": datetime.datetime.now().isoformat()
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
                "creation_time": user["creation_time"]
            } for user in users.values()
        ]
        return json.dumps(results)


    # TODO: Check this param name mismatch
    def describe_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("id")
        if not user_id:
            raise ValueError("<user_id> is required")

        users = self.db.read()
        if user_id not in users:
            raise ValueError(f"User with id:[{user_id}] not found")

        user = users[user_id]
        return json.dumps({
            "name": user['name'],
            "description": user['description'],
            "creation_time": user['creation_time']
        })

    def update_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("id")
        updated_data = data.get("user", {})
        if not user_id:
            raise ValueError("<user_id> is required")

        users = self.db.read()
        if user_id not in users:
            raise ValueError(f"User with id:[{user_id}] not found")

        # Constraints check
        if "name" in updated_data and updated_data["name"] != users[user_id]["name"]:
            raise ValueError("username cannot be updated")
        if "display_name" in updated_data:
            self._validate_name(updated_data["display_name"], 128)
            users[user_id]["display_name"] = updated_data["display_name"]

        self.db.write(users)
        return json.dumps({"status": "success"})

    def get_user_teams(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("id")
        if not user_id:
            raise ValueError("<user_id> is required")

        users = self.db.read()
        if user_id not in users:
            raise ValueError(f"User with id:[{user_id}] not found")

        # TODO: neet to make Team Manager before returning here
        return json.dumps([])
