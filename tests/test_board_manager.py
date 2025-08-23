import unittest
import json
import os
import datetime
from impl.board_manager import BoardManager
from impl.team_manager import TeamManager
from impl.user_manager import UserManager

class TestBoardManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up TestBoardManager Class...")
        cls.user_db_path = "tests/tmp/test_users.json"
        cls.team_db_path = "tests/tmp/test_teams.json"
        cls.board_db_path = "tests/tmp/test_boards.json"
        cls.task_db_path = "tests/tmp/test_tasks.json"

        os.makedirs(os.path.dirname(cls.user_db_path), exist_ok=True)

        cls.user_manager = UserManager(user_db_path=cls.user_db_path)
        cls.team_manager = TeamManager(team_db_path=cls.team_db_path, user_db_path=cls.user_db_path)
        cls.board_manager = BoardManager(
            boards_db_path=cls.board_db_path,
            tasks_db_path=cls.task_db_path,
            team_db_path=cls.team_db_path,
            user_db_path=cls.user_db_path
        )

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestBoardManager Class...")
        for path in [cls.user_db_path, cls.team_db_path, cls.board_db_path, cls.task_db_path]:
            if os.path.exists(path):
                os.remove(path)
        if os.path.exists("tests/tmp"):
            os.rmdir("tests/tmp")
        if os.path.exists("out"):
            for f in os.listdir("out"):
                os.remove(os.path.join("out", f))
            os.rmdir("out")


    def setUp(self):
        for path in [self.user_db_path, self.team_db_path, self.board_db_path, self.task_db_path]:
            with open(path, "w") as f:
                json.dump({}, f)

        self.admin_user = json.loads(self.user_manager.create_user(json.dumps({"name": "admin", "display_name": "Admin User"})))
        self.team = json.loads(self.team_manager.create_team(json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})))

    def test_create_board(self):
        request = json.dumps({
            "name": "Test Board",
            "description": "A test board",
            "team_id": self.team['id'],
            "creation_time": datetime.datetime.now().isoformat()
        })
        response = self.board_manager.create_board(request)
        data = json.loads(response)
        self.assertIn("id", data)

        # Test creating a board with a duplicate name for the same team
        with self.assertRaises(ValueError):
            self.board_manager.create_board(request)

        print("create_baord OK")

    def test_close_board(self):
        # Create a board
        request = json.dumps({
            "name": "Test Board",
            "description": "A test board",
            "team_id": self.team['id'],
            "creation_time": datetime.datetime.now().isoformat()
        })
        board = json.loads(self.board_manager.create_board(request))

        # Close the board
        close_request = json.dumps({"id": board["id"]})
        response = self.board_manager.close_board(close_request)
        data = json.loads(response)
        self.assertEqual(data["id"], board["id"])
        self.assertIn("CLOSED", data["status"])

        # Test closing a board that is already closed
        with self.assertRaises(ValueError):
            self.board_manager.close_board(close_request)

        print("close_board OK")


    def test_add_task(self):
        # Create a board
        board_request = json.dumps({
            "name": "Test Board",
            "description": "A test board",
            "team_id": self.team['id'],
            "creation_time": datetime.datetime.now().isoformat()
        })
        board = json.loads(self.board_manager.create_board(board_request))

        # Add a task
        task_request = json.dumps({
            "board_id": board["id"],
            "title": "Test Task",
            "description": "A test task",
            "user_id": self.admin_user["id"],
            "creation_time": datetime.datetime.now().isoformat()
        })
        response = self.board_manager.add_task(task_request)
        data = json.loads(response)
        self.assertIn("id", data)

        # Test adding a task with a duplicate title to the same board
        with self.assertRaises(ValueError):
            self.board_manager.add_task(task_request)

        print("add_task OK")


    def test_update_task_status(self):
        # Create a board and a task
        board_request = json.dumps({
            "name": "Test Board",
            "description": "A test board",
            "team_id": self.team['id'],
            "creation_time": datetime.datetime.now().isoformat()
        })
        board = json.loads(self.board_manager.create_board(board_request))
        task_request = json.dumps({
            "board_id": board["id"],
            "title": "Test Task",
            "description": "A test task",
            "user_id": self.admin_user["id"],
            "creation_time": datetime.datetime.now().isoformat()
        })
        task = json.loads(self.board_manager.add_task(task_request))

        # Update task status
        update_request = json.dumps({"id": task["id"], "status": "IN_PROGRESS"})
        response = self.board_manager.update_task_status(update_request)
        data = json.loads(response)
        self.assertEqual(data["status"], "IN_PROGRESS")

        print("update_task_status OK")


    def test_list_boards(self):
        # Create a board
        board_request = json.dumps({
            "name": "Test Board",
            "description": "A test board",
            "team_id": self.team['id'],
            "creation_time": datetime.datetime.now().isoformat()
        })
        self.board_manager.create_board(board_request)

        # List boards for the team
        list_request = json.dumps({"id": self.team["id"]})
        response = self.board_manager.list_boards(list_request)
        data = json.loads(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test Board")

        print("list_team_boards OK")


    def test_export_board(self):
        # Create a board and a task
        board_request = json.dumps({
            "name": "Test Board",
            "description": "A test board",
            "team_id": self.team['id'],
            "creation_time": datetime.datetime.now().isoformat()
        })
        board = json.loads(self.board_manager.create_board(board_request))
        task_request = json.dumps({
            "board_id": board["id"],
            "title": "Test Task",
            "description": "A test task",
            "user_id": self.admin_user["id"],
            "creation_time": datetime.datetime.now().isoformat()
        })
        self.board_manager.add_task(task_request)

        # Export the board
        export_request = json.dumps({"id": board["id"]})
        response = self.board_manager.export_board(export_request)
        data = json.loads(response)
        self.assertIn("out_file", data)
        self.assertTrue(os.path.exists(data["out_file"]))

        print("export_board OK")


if __name__ == '__main__':
    unittest.main()
