import json
import uuid
import datetime

from project_board_base import ProjectBoardBase
from utils.file_db import FileDB


class BoardManager(ProjectBoardBase):
    def __init__(self, boards_db_path="db/boards.json", tasks_db_path="db/tasks.json", team_db_path="db/teams.json", user_db_path="db/users.json"):
        self.board_db = FileDB(boards_db_path)
        self.tasks_db = FileDB(tasks_db_path)
        self.team_db = FileDB(team_db_path)
        self.user_db = FileDB(user_db_path)

    def _validate_name(self, name: str, max_len: int):
        if not name or len(name) > max_len:
            raise ValueError(f"Invalid team name. Name must be between 1 - {max_len} characters.")

    def _validate_description(self, desc: str, max_len: int):
        if desc and len(desc) > max_len:
            raise ValueError(f"Description must be less than {max_len} characters.")



    def create_board(self, request: str) -> str:
        data = json.loads(request)
        board_name = data.get("name")
        description = data.get("description")
        team_id = data.get("team_id")
        creation_time = data.get("creation_time")

        # enforce constraints
        self._validate_name(board_name, 64)
        self._validate_description(description, 128)

        # board name must be unique for a team
        boards = self.board_db.read()
        if any(
            board["name"] == board_name and board["team_id"] == team_id
            for board in boards.values()
        ):
            raise ValueError(f"Board with name '{board_name}' already exists for team:[{team_id}].")

        board_id = str(uuid.uuid4())
        board = {
            "id": board_id,
            "name": board_name,
            "description": description,
            "team_id": team_id,
            "creation_time": creation_time,
            "status": "OPEN",
            "end_time": None,
            "tasks": []
        }
        boards[board_id] = board
        self.board_db.write(boards)

        return json.dumps({"id":board_id})
