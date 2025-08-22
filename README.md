# FactWise Python Mini Project

## Tech Stack
- Django
	-	Pros:
	    - aligns with company stack, ORM built-in, batteries included.
	-	Cons:
	    - Heavy for this small assignment.
		- Forces me into migrations, DB-style modeling (but problem states file-based persistence, not RDBMS).

- FastAPI
	-	Pros:
	    - Lightweight,
		- fast to implement REST APIs.
		- JSON I/O handling is built-in with Pydantic models → perfectly aligns with requirement.
		- Shows I can design clean, modular and production-grade APIs.
	- Assignment gives freedom of Python Library.

Hence chose **FastAPI** for this assignment.

## Implementations Order:
1. FileDB class (for persistent json storage)
2. Converting all base classes into Abstract classes and methods
3. Implementing Concrete User class. (Cause team and ProjectBoard will depend on it)
4. Made some unittest to check functioning of UserManager Class
5. Implementing Concrete Team class.
6. Implementing Concrete ProjectBoard class.
7. Wrapping the Business Logic with FastAPI for backend endpoints
8. Testing all routes with Postman

## Project Board Implementation Notes
- create_board
    - Validate name uniqueness within the given team.
    - Enforce max length on name (64) and description (128).
    - Add board to self.boards.

- close_board
    - Only allowed if all tasks are "COMPLETE".
    - Set status="CLOSED" and end_time=now.

- add_task
    - Check board exists and is OPEN.
    - Task title unique within board.
    - Enforce max length on title (64) and description (128).

- update_task_status
    - Change status among OPEN, IN_PROGRESS, COMPLETE.

- list_boards
    - Return all OPEN boards for a given team_id.

- export_board
    - Generate a .txt file in out/ folder.
    - Pretty print board metadata + task list with statuses.

```bash
# Board Data Structure
self.boards = {
    "<board_id>": {
        "id": "<board_id>",
        "name": "<board_name>",
        "description": "<desc>",
        "team_id": "<team_id>",
        "creation_time": "<ts>",
        "end_time": None,
        "status": "OPEN | CLOSED"
        #"tasks": {}   # tasks dictionary keyed by task_id
    }
}

# Task Data Structure
"tasks": {
    "<task_id>": {
        "id": "<task_id>",
        "title": "<title>",
        "description": "<desc>",
        "user_id": "<assigned_user>",
        "creation_time": "<ts>",
        "status": "OPEN | IN_PROGRESS | COMPLETE"
    }
}
```

## Assumptions

### Add Task method missing inputs
- The input of the add_task method under project_board_base abstract class were unclear and incomplete.
- I've assumped that the necessary details:
    - board_id
    - user_id
- have been provided.
- Have made the changes to the base abs class also.

## Important Commands:
- running unit tests:
```bash
python3-m unittest tests/test_user_manager.py
```
- installing requirements:
```bash
uv pip install -r requirements.txt
```
- Starting FastAPI server
```bash
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs # Swagger UI
http://127.0.0.1:8000/docs # ReDoc
```
