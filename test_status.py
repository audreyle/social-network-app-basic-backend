"""
Unit testing the methods in StatusCollection class
"""
from unittest import TestCase

from test_model import test_database
from user_status import StatusCollection


class TestStatusCollection(TestCase):
    """
    Creating a test Status class for testing methods in User class
    """
    def setUp(self):
        """
        For the unittests to all pass, we need some seed data. I will create a
        test_status table and bind it to the TestDatabase I imported from test_model.py

        You also have to go to user_status.py and change the database table in __init__
        to ["test_status"]
        """
        # Bind the test_status table to the TestDatabase
        self.database = test_database["test_status"]
        self.test_status_collection = StatusCollection(self.database)
        # seed data
        self.test_status_collection.add_status("jerry.tom1_00001", "jerry.tom1",
                                               "Tom never saw it coming")
        self.test_status_collection.add_status("scooby.doo1_00001", "scooby.doo1",
                                               "Scooby, Scooby Dooo!")
        self.test_status_collection.add_status("velma2_00002", "velma2", "Jinkies!")


    def tearDown(self):
        """
        Drop the test_users table after running all unittests.
        """
        test_database["test_status"].drop()


    def test_add_status_success(self):
        """
        Testing if adding a status to test_status.test_status table of TestDatabase
        returns True.
        """
        self.assertTrue(self.test_status_collection.add_status("king.arthur_00001",
                                                               "king.arthur", "I am a squirrel!"))


    def test_add_status_fail(self):
        """
        Adding status to test_status collection in TestDatabase should fail and return False
        when a duplicate status id is found in the test_status.test_status table of TestDatabase
        """
        self.assertFalse(self.test_status_collection.add_status(
            "honore_de_balzac_00001", "honore_de_balzac", "All happiness depends "
                                                          "on courage and work."))

    def test_search_status_success(self):
        """
        Returns a status pymongo cursor object if the status_id exists in the
        test_status.test_status table of the TestDatabase.

        Python understands this behavior to be the equivalent of True and pass the test.
        """
        self.assertTrue(
            self.test_status_collection.search_status("scooby.doo1_00001"))

    def test_search_status_fail(self):
        """
        Search_status should fail when it can't find the status_id in test_status.test_status.
        The returned pymongo object in the function called should contain None.
        """
        self.assertIsNone(
            self.test_status_collection.search_status("cara.delevingne_00001"))

    def test_update_status_success(self):
        """
        Returns an updated pymongo status object if the status_id exists in TestDatabase/

        Python understands this behavior to be the equivalent of True and pass the test.
        """
        self.assertTrue(self.test_status_collection.update_status("jerry.tom1_00001",
                                                        "I am not a toy I'm a mouse!"))

    def test_update_status_fail(self):
        """
        The content of the updated pymongo status object should contain None
        if status_id does not exist in TestDatabase
        """
        self.assertIsNone(
            self.test_status_collection.update_status("merlin1",
                                            "A dark age indeed! Age of inconvenience!"))

    def test_delete_status_success(self):
        """
        Returns True if it can find a status_id in test_status.test_status and deletes it.
        """
        self.assertTrue(self.test_status_collection.delete_status("king.arthur_00001"))

    def test_delete_status_fail(self):
        """
        Fails to delete status when the status_id can't be found in test_status.test_status
        """
        self.assertIsNone(self.test_status_collection.delete_status("master_shifu"))
