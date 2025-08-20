import unittest
import json
import os
from impl.user_manager import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.db_path = 'db/test_users.json'
        self.user_manager = UserManager(db_path=self.db_path)

        # Clean up the test database file before each test
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        # Clean up the test database file after each test
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

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

        # Test creating a user with a duplicate name
        request = json.dumps({"name": "testuser", "display_name": "Another User"})
        with self.assertRaises(ValueError):
            self.user_manager.create_user(request)

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

        # Test updating the user's name (which should fail)
        request = json.dumps({
            "id": user_id,
            "user": {"name": "newusername"}
        })
        with self.assertRaises(ValueError):
            self.user_manager.update_user(request)

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

if __name__ == '__main__':
    unittest.main()
