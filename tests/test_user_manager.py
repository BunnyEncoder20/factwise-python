import unittest
import os
import json
from impl.user_manager import UserManager
from impl.team_manager import TeamManager

class TestUserManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up TestUserManager Class...")
        # set db paths inside tests/tmp
        cls.user_db_path = "tests/tmp/test_users.json"
        cls.team_db_path = "tests/tmp/test_teams.json"

        # make sure tmp dir exists
        os.makedirs(os.path.dirname(cls.user_db_path), exist_ok=True)

        # create fresh empty json files
        with open(cls.user_db_path, "w") as f:
            json.dump({}, f)
        with open(cls.team_db_path, "w") as f:
            json.dump({}, f)

        # init managers once for all tests
        cls.user_manager = UserManager(
            user_db_path=cls.user_db_path,
            team_db_path=cls.team_db_path
        )
        # We also need a team manager to create teams for get_user_teams test
        cls.team_manager = TeamManager(
            team_db_path=cls.team_db_path,
            user_db_path=cls.user_db_path
        )

    @classmethod
    def tearDownClass(cls):
        print("Tearing down TestUserManager Class...")

        # cleanup tmp files at end
        if os.path.exists(cls.user_db_path):
            os.remove(cls.user_db_path)
        if os.path.exists(cls.team_db_path):
            os.remove(cls.team_db_path)
        # remove the directory
        if os.path.exists("tests/tmp"):
            os.rmdir("tests/tmp")


    def setUp(self):
        # Clean user and team dbs before each test
        with open(self.user_db_path, "w") as f:
            json.dump({}, f)
        with open(self.team_db_path, "w") as f:
            json.dump({}, f)


    def test_create_user(self):
        # Test successful user creation
        request = json.dumps({"name": "testuser", "display_name": "Test User"})
        response = self.user_manager.create_user(request)
        data = json.loads(response)
        self.assertIn("id", data)

        # Test creating a user with a name that is too long
        long_name = "a" * 65
        request = json.dumps({"name": long_name, "display_name": "Test User"})
        with self.assertRaises(ValueError):
            self.user_manager.create_user(request)

        # Test creating a user with a display name that is too long
        long_display_name = "a" * 65
        request = json.dumps({"name": "testuser2", "display_name": long_display_name})
        with self.assertRaises(ValueError):
            self.user_manager.create_user(request)

        # Test creating a user with a duplicate name
        request = json.dumps({"name": "testuser", "display_name": "Another User"})
        with self.assertRaises(ValueError):
            self.user_manager.create_user(request)

        print(".create_user OK")

    def test_list_users(self):
        # Test listing users when there are no users
        response = self.user_manager.list_users()
        data = json.loads(response)
        self.assertEqual(len(data), 0)

        # Create a user and then list users
        request = json.dumps({"name": "testuser", "display_name": "Test User"})
        self.user_manager.create_user(request)
        response = self.user_manager.list_users()
        data = json.loads(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "testuser")

        print("list_user OK")


    def test_describe_user(self):
        # Create a user
        request = json.dumps({"name": "testuser", "display_name": "Test User"})
        response = self.user_manager.create_user(request)
        user_id = json.loads(response)["id"]

        # Test describing the user
        request = json.dumps({"id": user_id})
        response = self.user_manager.describe_user(request)
        data = json.loads(response)
        self.assertEqual(data["name"], "testuser")

        # Test describing a user that does not exist
        request = json.dumps({"id": "nonexistentuser"})
        with self.assertRaises(ValueError):
            self.user_manager.describe_user(request)

        print("describe_user OK")


    def test_update_user(self):
        # Create a user
        request = json.dumps({"name": "testuser", "display_name": "Test User"})
        response = self.user_manager.create_user(request)
        user_id = json.loads(response)["id"]

        # Test updating the user's display name
        request = json.dumps({
            "id": user_id,
            "user": {"display_name": "New Display Name"}
        })
        response = self.user_manager.update_user(request)
        data = json.loads(response)
        self.assertEqual(data["status"], "success")

        # Test that the display name was updated
        users = self.user_manager.db.read()
        self.assertEqual(users[user_id]["display_name"], "New Display Name")


        # Test updating display name with a name that is too long
        long_display_name = "a" * 129
        request = json.dumps({
            "id": user_id,
            "user": {"display_name": long_display_name}
        })
        with self.assertRaises(ValueError):
            self.user_manager.update_user(request)

        # Test updating the user's name (which should fail)
        request = json.dumps({
            "id": user_id,
            "user": {"name": "newusername"}
        })
        with self.assertRaises(ValueError):
            self.user_manager.update_user(request)

        print("update_user OK")



    def test_get_user_teams(self):
        # Create a user
        request = json.dumps({"name": "testuser", "display_name": "Test User"})
        response = self.user_manager.create_user(request)
        user_id = json.loads(response)["id"]

        # Test getting user teams (should be an empty list)
        request = json.dumps({"id": user_id})
        response = self.user_manager.get_user_teams(request)
        data = json.loads(response)
        self.assertEqual(data, [])

        # Create a team with the user as admin
        team_request = json.dumps({"name": "Test Team", "description": "A test team", "admin": user_id})
        self.team_manager.create_team(team_request)

        # Test getting user teams again
        response = self.user_manager.get_user_teams(request)
        data = json.loads(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test Team")

        print("get_user_teams OK")

if __name__ == '__main__':
    unittest.main()
