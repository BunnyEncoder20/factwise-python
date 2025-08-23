import unittest
import json
import os
from impl.team_manager import TeamManager
from impl.user_manager import UserManager

class TestTeamManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up TestTeamManager Class...")
        # set db paths inside tests/tmp
        cls.user_db_path = "tests/tmp/test_users.json"
        cls.team_db_path = "tests/tmp/test_teams.json"

        # make sure tmp dir exists
        os.makedirs(os.path.dirname(cls.user_db_path), exist_ok=True)

        # init managers once for all tests
        cls.user_manager = UserManager(
            user_db_path=cls.user_db_path
        )
        cls.team_manager = TeamManager(
            team_db_path=cls.team_db_path,
            user_db_path=cls.user_db_path
        )

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestTeamManager Class...")

        # cleanup tmp files at end
        if os.path.exists(cls.user_db_path):
            os.remove(cls.user_db_path)
        if os.path.exists(cls.team_db_path):
            os.remove(cls.team_db_path)
        if os.path.exists("tests/tmp"):
            os.rmdir("tests/tmp")

    def setUp(self):
        # Clean user and team dbs before each test
        with open(self.user_db_path, "w") as f:
            json.dump({}, f)
        with open(self.team_db_path, "w") as f:
            json.dump({}, f)

        # Create a dummy user for testing
        self.admin_user = json.loads(self.user_manager.create_user(json.dumps({"name": "admin", "display_name": "Admin User"})))

    def test_create_team(self):
        # Test successful team creation
        request = json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})
        response = self.team_manager.create_team(request)
        data = json.loads(response)
        self.assertIn("id", data)

        # Test creating a team with a name that is too long
        long_name = "a" * 65
        request = json.dumps({"name": long_name, "description": "A test team", "admin": self.admin_user['id']})
        with self.assertRaises(ValueError):
            self.team_manager.create_team(request)

        # Test creating a team with a duplicate name
        request = json.dumps({"name": "Test Team", "description": "Another test team", "admin": self.admin_user['id']})
        with self.assertRaises(ValueError):
            self.team_manager.create_team(request)

        print("create_team OK")

    def test_list_teams(self):
        # Test listing teams when there are no teams
        response = self.team_manager.list_teams()
        data = json.loads(response)
        self.assertEqual(len(data), 0)

        # Create a team and then list teams
        request = json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})
        self.team_manager.create_team(request)
        response = self.team_manager.list_teams()
        data = json.loads(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test Team")

        print("list_team OK")


    def test_describe_team(self):
        # Create a team
        request = json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})
        response = self.team_manager.create_team(request)
        team_id = json.loads(response)["id"]

        # Test describing the team
        request = json.dumps({"id": team_id})
        response = self.team_manager.describe_team(request)
        data = json.loads(response)
        self.assertEqual(data["name"], "Test Team")

        # Test describing a team that does not exist
        request = json.dumps({"id": "nonexistentteam"})
        with self.assertRaises(ValueError):
            self.team_manager.describe_team(request)

        print("describe_team OK")

    def test_update_team(self):
        # Create a team
        request = json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})
        response = self.team_manager.create_team(request)
        team_id = json.loads(response)["id"]

        # Test updating the team's description
        request = json.dumps({
            "id": team_id,
            "team": {"description": "New Description"}
        })
        response = self.team_manager.update_team(request)
        data = json.loads(response)
        self.assertEqual(data["status"], "success")

        # Test updating the team's name to a duplicate name
        self.team_manager.create_team(json.dumps({"name": "Another Team", "description": "desc", "admin": self.admin_user['id']}))
        request = json.dumps({
            "id": team_id,
            "team": {"name": "Another Team"}
        })
        with self.assertRaises(ValueError):
            self.team_manager.update_team(request)

        print("update_team OK")

    def test_add_users_to_team(self):
        # Create a team
        request = json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})
        response = self.team_manager.create_team(request)
        team_id = json.loads(response)["id"]

        # Create a new user
        new_user = json.loads(self.user_manager.create_user(json.dumps({"name": "newuser", "display_name": "New User"})))

        # Add the new user to the team
        request = json.dumps({"id": team_id, "users": [new_user["id"]]})
        response = self.team_manager.add_users_to_team(request)
        data = json.loads(response)
        self.assertEqual(data["status"], "success")
        self.assertIn(new_user["id"], data["users"])

        print(".add_users_to_team OK")

    def test_remove_users_from_team(self):
        # Create a team and add a user
        request = json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})
        response = self.team_manager.create_team(request)
        team_id = json.loads(response)["id"]
        new_user = json.loads(self.user_manager.create_user(json.dumps({"name": "newuser", "display_name": "New User"})))
        self.team_manager.add_users_to_team(json.dumps({"id": team_id, "users": [new_user["id"]]}))

        # Remove the user from the team
        request = json.dumps({"id": team_id, "users": [new_user["id"]]})
        response = self.team_manager.remove_users_from_team(request)
        data = json.loads(response)
        self.assertEqual(data["status"], "success")
        self.assertNotIn(new_user["id"], data["users"])

        print("remove_users_from_team OK")

    def test_list_team_users(self):
        # Create a team and add a user
        request = json.dumps({"name": "Test Team", "description": "A test team", "admin": self.admin_user['id']})
        response = self.team_manager.create_team(request)
        team_id = json.loads(response)["id"]
        new_user = json.loads(self.user_manager.create_user(json.dumps({"name": "newuser", "display_name": "New User"})))
        self.team_manager.add_users_to_team(json.dumps({"id": team_id, "users": [new_user["id"]]}))

        # List the users in the team
        request = json.dumps({"id": team_id})
        response = self.team_manager.list_team_users(request)
        data = json.loads(response)
        self.assertEqual(len(data), 2) # Admin and the new user
        self.assertTrue(data[0]["name"] == 'newuser' or data[1]["name"] == 'newuser')

        print("list_team_users OK")

if __name__ == '__main__':
    unittest.main()
