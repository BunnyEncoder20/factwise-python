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

        self._validate_name(name, 64)
        self._validate_description(description, 128)

        teams = self.team_db.read()
        users = self.user_db.read()

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
            # "id": team["id"],
            "name": team["name"],
            "description": team["description"],
            "admin": team["admin"],
            # "users": team["users"],
            "creation_time": team["creation_time"]
        } for team in teams.values()]
        return json.dumps(result)
