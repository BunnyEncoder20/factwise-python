import json
import uuid
import datetime

from team_base import TeamBase
from utils.file_db import FileDB

class TeamManager(TeamBase):
    def __init__(self, team_db_path="db/teams.json", user_db_path="db/users.json"):
        self.team_db = FileDB(team_db_path)
        self.user_db = FileDB(user_db_path)

    def _validate_name(self, name: str, max_len: int):
        if not name or len(name) > max_len:
            raise ValueError(f"Invalid team name. Name must be between 1 - {max_len} characters.")

    def _validate_description(self, desc: str, max_len: int):
        if desc and len(desc) > max_len:
            raise ValueError(f"Description must be less than {max_len} characters.")




    def create_team(self, request: str) -> str:
        data = json.loads(request)
        name = data.get("name")
        description = data.get("description", "")
        admin_id = data.get("admin")    # user id

        teams = self.team_db.read()
        users = self.user_db.read()

        # enforce constraints
        self._validate_name(name, 64)
        self._validate_description(description, 128)

        # Team name must be unique
        if any(team["name"] == name for team in teams.values()):
            raise ValueError(f"Team with name '{name}' already exists")

        # Team Admin must be a existing user
        if admin_id not in users:
            raise ValueError(f"Admin user with id: [{admin_id}] does not exist")

        team_id = str(uuid.uuid4())
        team = {
            "id": team_id,
            "name": name,
            "description": description,
            "admin": admin_id,
            "users": [admin_id],    # admin always first member of team
            "creation_time": datetime.datetime.now().isoformat()
        }

        teams[team_id] = team
        self.team_db.write(teams)

        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams = self.team_db.read()
        result = [{
            "name": team["name"],
            "description": team["description"],
            "admin": team["admin"],
            "creation_time": team["creation_time"]
        } for team in teams.values()]
        return json.dumps(result)

    def describe_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")
        if not team_id:
            raise ValueError("Team id is required")

        teams = self.team_db.read()
        if team_id not in teams:
            raise ValueError(f"Team with id:[{team_id}] does not exist")

        team = teams[team_id]
        return json.dumps({
            "name": team["name"],
            "description": team["description"],
            "admin": team["admin"],
            "creation_time": team["creation_time"]
        })

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("id")
        updated_data = data.get("team", {})
        teams = self.team_db.read()

        if not team_id:
            raise ValueError("Team id is required")
        if team_id not in teams:
            raise ValueError(f"Team with id:[{team_id}] not found")

        # enforce constraints
        if "name" in updated_data:
            self._validate_name(updated_data["name"], 64)
            if any(team["name"] == updated_data["name"] and tid != team_id for tid, team in teams.items()):
                raise ValueError("Team name must be unique")
            teams[team_id]["name"] = updated_data["name"]

        if "description" in updated_data:
            self._validate_description(updated_data["description"], 128)
            teams[team_id]["description"] = updated_data["description"]

        if "admin" in updated_data:
            users = self.user_db.read()
            if updated_data["admin"] not in users:
                raise ValueError(f"Admin user with id:[{updated_data['admin']}] not found")
            teams[team_id]["admin"] = updated_data["admin"]

            # making sure new admin is part of team
            if updated_data["admin"] not in teams[team_id]["users"]:
                teams[team_id]["users"].append(updated_data["admin"])

        self.team_db.write(teams)
        return json.dumps({"status": "success"})
