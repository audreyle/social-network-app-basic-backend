"""
Unit testing the methods in UserCollection class
"""
from unittest import TestCase

from test_model import test_database
from users import UserCollection


class TestUserCollection(TestCase):
    """
    Creating a test User class for testing methods in User class
    """
    def setUp(self):
        """
        For the unittests to all pass, we need some seed data. I will create a
        test_users table and bind it to the TestDatabase I imported from test_model.py

        You also have to go to users.py and change the database table in __init__
        to ["test_users"]
        """
        # Bind the test_users table to the TestDatabase
        self.database = test_database["test_users"]
        self.test_user_collection = UserCollection(self.database)
        # seed data
        self.test_user_collection.add_user("jerry.tom1", "Jerry", "Mouse", "jerry.tom1@gmail.com")
        self.test_user_collection.add_user("scooby.doo1", "Scooby", "Doo", "scooby.doo1@gmail.com")


    def tearDown(self):
        """
        Drop the test_users table after running all unittests.
        """
        test_database["test_users"].drop()


    def test_add_user_success(self):
        """
        Testing if adding a user to test_users.test_users table of TestDatabase
        returns True.
        """
        self.assertTrue(self.test_user_collection.add_user("king.arthur1", "Arthuro",
                                                "Pendagrone", "king.arthur@ymail.com"))

    def test_add_user_fail(self):
        """
        Adding user to Test Database should fail when the user_id already exists and return False
        """
        self.test_user_collection.add_user("king.arthur", "Arthur",
                                                "Pendagron", "king.arthur@gmail.com")
        self.assertFalse(self.test_user_collection.add_user("king.arthur", "Arthur",
                                                "Pendagron", "king.arthur@gmail.com"))

    def test_search_user_success(self):
        """
        Returns a status pymongo cursor object if the status_id exists in the
        test_users.test_users table of the TestDatabase.

        Python understands this behavior to be the equivalent of True and pass the test.
        """
        self.assertTrue(
            self.test_user_collection.search_user("scooby.doo1"))

    def test_search_user_fail(self):
        """
        Search_user should fail when it can't find the user_id in test_status.test_status.
        The returned pymongo object in the function called should contain None.
        """
        self.assertIsNone(
            self.test_user_collection.search_user("cara.delevingne"))

    def test_update_user_success(self):
        """
        Returns an updated pymongo status object if the user_id exists in TestDatabase.

        Python understands this behavior to be the equivalent of True and pass the test.
        """
        self.assertTrue(self.test_user_collection.update_user("jerry.tom1", "Jerry",
                                                    "Mouse", "jerry.mouse@yahoo.com"))

    def test_update_user_fail(self):
        """
        The content of the updated pymongo user object should contain None
        if user_id does not exist in TestDatabase.
        """
        self.assertIsNone(
            self.test_user_collection.update_user("merlin1", "Merlin", "Wizard",
                                                    "merlin1@gmail.com"))

    def test_delete_user_success(self):
        """
        Returns True if it can find a user_id in test_users.test_users and deletes it.
        """
        self.assertTrue(self.test_user_collection.delete_user("king.arthur"))

    def test_delete_user_fail(self):
        """
        Fails to delete status when the user_id can't be found in test_users.test_users.
        """
        self.assertIsNone(self.test_user_collection.delete_user("master_shifu"))
