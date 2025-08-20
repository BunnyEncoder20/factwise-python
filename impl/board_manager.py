import json
import uuid
import datetime

from project_board_base import ProjectBoardBase
from utils.file_db import FileDB

class BoardManager(ProjectBoardBase):
    def __init__(self, boards_db_path="db/boards.json", tasks_db_path="db/tasks.json", team_db_path="db/teams.json", user_db_path="db/users.json"):
        self.board_db = FileDB(boards_db_path)
        self.task_db = FileDB(tasks_db_path)
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
            # "tasks": []
        }
        boards[board_id] = board
        self.board_db.write(boards)

        return json.dumps({"id":board_id})

    def close_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get("id")
        if not board_id:
            raise ValueError("Board ID is required.")

        boards = self.board_db.read()
        if board_id not in boards:
            raise ValueError(f"Board with ID:[{board_id}] not found.")

        board = boards[board_id]
        if board["status"] == "CLOSED":
            raise ValueError(f"Board with ID [{board_id}] is already closed.")

        board["status"] = "CLOSED"
        board["end_time"] = datetime.datetime.now().isoformat()
        self.board_db.write(boards)

        return json.dumps({"id":board_id, "status": f"{board["status"]} on {board["end_time"]}"})

    def add_task(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get("bid")
        task_title = data.get("title")
        description = data.get("description")
        user_id = data.get("user_id")
        creation_time = data.get("creation_time")

        # validations
        self._validate_name(task_title, 64)
        self._validate_description(description, 128)

        boards = self.board_db.read()
        tasks = self.task_db.read()

        board = boards.get("board_id")
        if not board:
            raise ValueError(f"Board id:[{board_id}] not found")
        if board["status"] == "CLOSED":
            raise ValueError("Cannot add task to closed board")

        # task title must be unique for board
        if any(
            task["title"] == task_title and task["board_id"] == board_id for task in tasks.values()
        ): raise ValueError(f"Task with title '{task_title}' already exist under Board:[{board_id}]")

        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "title": task_title,
            "description": description,
            "board_id": board_id,
            "user_id": user_id,
            "creation_time": creation_time,
            "status": "OPEN",
        }
        tasks[task_id] = task

        self.task_db.write(tasks)
        return json.dumps({"id": task_id})


    def update_task_status(self, request: str) -> str:
        data = json.loads(request)
        task_id = data.get("id")
        updated_status = data.get("status")

        if not task_id:
            raise ValueError("Task id is required")

        tasks = self.task_db.read()
        if task_id not in tasks:
            raise ValueError(f"Task id:[{task_id}] not found")

        tasks[task_id]["status"] = updated_status
        self.task_db.write(tasks)
        return json.dumps({"id": task_id, "status": tasks[task_id]["status"]})
