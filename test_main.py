"""
Unit testing methods in main.py.
What will become obvious is that these unittests are a repeat
of my unittests in test_user_status.py.
The assignment asked for 100% coverage of both users.py and user_status.py
and the unittests here only covered 37% of user_status.py.
To make it more interesting, I used MagicMock() because it is
important to understand that the functions in main.py call the functions
in users.py and user_status.py. We need to test the functions in main.py
separately, so we use MagicMock to do that. Sometimes, for the failure tests,
I feel I am talking with myself because I force the functions that the methods
in main.py call to return None, so naturally my assertions will say
something along the lines of "main.add_status etc. should also return None)

In this light, I would make sure that the unittests for load_csv_to_db functions
work since they are unique to the main.py file.
"""
import pymongo
import io
from unittest import TestCase
from unittest.mock import MagicMock, patch, mock_open

import main
import user_status
import users
from socialnetwork_model import database


class TestMain(TestCase):
    """
    Creating a test class for main menu
    """
    def test_init_user_collection(self):
        """
        Testing the function that creates a user collection instance
        """
        expected = type(users.UserCollection(database))
        self.assertEqual(type(main.init_user_collection()), expected)

    def test_init_status_collection(self):
        """
        Testing the function that creates a status collection instance
        """
        expected = type(user_status.UserStatusCollection(database))
        self.assertEqual(type(main.init_status_collection()), expected)

    def test_load_account_csv_to_db_success(self):
        """
        Testing loading csv data to UsersTable in database.
        Caution: It will actually write to the database.
        """
        test_user_collection = users.UserCollection(database)
        self.assertTrue(main.load_accounts_csv_to_db('test_main_load_user_file.csv',
                                                     test_user_collection))

    def test_load_accounts_csv_to_db_file_not_found(self):
        """
        Testing FileNotFoundError exception in load_accounts_csv_to_db
        """
        with patch('main.open', mock_open()) as mock_file:
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                # forcing the function to return a FileNotFoundError so I can
                # move on to test the error message and what the stream returns.
                # The load_accounts.csv_to_db should return False
                mock_file.side_effect = FileNotFoundError
                outcome = main.load_users('file.csv', users.UserCollection)
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out,
                                 ['Detailed error message:'])  # the error message cuts
                # out for some reason

    def test_load_status_csv_to_db_success(self):
        """
        Testing loading status data to UserStatusTable in database.
        Caution: It will actually write to the database.
        """
        test_status_collection = user_status.UserStatusCollection(database)
        # I actually created a test file so I could check the database UserStatusTable
        # in my database to verify it works
        self.assertTrue(main.load_status_csv_to_db('test_main_load_status_file.csv',
                                                   test_status_collection))

    def test_load_status_csv_to_db_file_not_found(self):
        """
        Testing FileNotFoundError exception in load_status_csv_to_db
        """
        with patch('main.open', mock_open()) as mock_file:
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                mock_file.side_effect = FileNotFoundError
                outcome = main.load_status_csv_to_db('file.csv', users.UserCollection)
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out,
                                 ['Detailed error message:'])

    def test_add_user_success(self):
        """
        Mocking add_user in main.py. It calls add_user in users.py
        and is called by add_user in menu.py so we need a way
        to test this in isolation. We therefore need to use MagicMock().
        """
        # Leveraging MagicMock instead of User to test main.add_user
        # in isolation
        user_collection = MagicMock()
        mock_user = MagicMock()
        # Setting values to pre-seeded data
        mock_user.user_id = "serena.tennis"
        mock_user.user_name = "Serena"
        mock_user.user_last_name = "Williams"
        mock_user.email = "serena.tennis@gmail.com"
        # Make sure add_user() in users.py returns a User object to our main.add_user
        user_collection.add_user.return_value = mock_user
        # calling add_user on our mocked user_collection
        new_user = main.add_user(mock_user.user_id, mock_user.user_name,
                                 mock_user.user_last_name, mock_user.email, user_collection)
        # compare what the 2 add_user functions returned.
        self.assertEqual(new_user, mock_user)
        # Verify main.add_user called add_user in users.py with our mock_data
        user_collection.add_user.assert_called_with("serena.tennis", "Serena",
                                                    "Williams", "serena.tennis@gmail.com")

    def test_search_user_success(self):
        """
        Mocking search_user in main.py
        """
        # Leveraging MagicMock instead of User to test main.search_user
        # in isolation
        user_collection = MagicMock()
        mock_user = MagicMock()
        # Setting values to pre-seeded data
        mock_user.user_id = "serena.tennis"
        mock_user.user_name = "Serena"
        mock_user.user_last_name = "Williams"
        mock_user.email = "serena.tennis@gmail.com"
        # main.search_user calls users.search_user which must return a user object
        # for the former to work
        user_collection.add_user.return_value = mock_user
        # Verify that main.search_user also returns the user object
        self.assertIsNotNone(main.search_user(mock_user.user_id, user_collection))
        # Verify that main.search_user called search_user in users.py with "serena.tennis"
        user_collection.search_user.assert_called_with("serena.tennis")

    def test_search_user_not_found(self):
        """
        Mocking failure of search_user in main.py
        """
        # Leveraging MagicMock instead of User
        user_collection = MagicMock()
        mock_user = MagicMock()
        # Change the return value of search_user() to None, signaling that user is not found
        user_collection.search_user.return_value = None
        # Verify that the function that was passed to main.search_user returned False
        self.assertFalse(main.search_user(mock_user, user_collection))

    def test_delete_user_success(self):
        """
        Mocking delete_user in main.py
        """
        # Leveraging MagicMock instead of User to test main.delete_user
        # in isolation
        mock_user = MagicMock()
        # Setting values to pre-seeded data
        mock_user.user_id = "scoobydoo1"
        mock_user.email = "scoobydoo1@yahoo.com"
        mock_user.user_name = "Scooby"
        mock_user.user_last_name = "Doo"
        user_collection = MagicMock()
        # verify that main.delete_user also returns True
        self.assertTrue(main.delete_user(mock_user.user_id, user_collection))
        # verify main.delete_user called delete_user() in users.py with
        # our mocked data
        user_collection.delete_user.assert_called_with("scoobydoo1")

    def test_delete_user_fail(self):
        """"
        Mocking failure of delete_user in main.py
        """
        user_collection = MagicMock()
        mock_user = MagicMock()
        # Trick main.delete_user into thinking that delete_user in users.py
        # could not find the user_id in UsersTable.
        user_collection.delete_user.return_value = None
        # If user_id does not exist, the method that main.delete_user calls
        # should return False
        self.assertFalse(main.delete_user(mock_user.user_id, user_collection))

    def test_update_email_success(self):
        """
        Mocking update_email in main.py
        """
        # Leveraging MagicMock instead of User to test main.update_email
        # in isolation
        mock_user = MagicMock()
        # Setting values to pre-seeded data so we can update email
        mock_user.user_id = "serena.tennis"
        mock_user.user_name = "Serena"
        mock_user.user_last_name = "Williams"
        mock_user.email = "serena.tennis@gmail.com"
        user_collection = MagicMock()
        # main.update_email should call update_email in users.py, which returns
        # True if successful. Verify that.
        self.assertTrue(main.update_email(mock_user.user_id, mock_user.email,
                                          user_collection))
        # Verify that main.update_email method called update_email from users.py
        # with our mocked data
        user_collection.update_email.assert_called_with("serena.tennis",
                                                        "serena.tennis@gmail.com")

    def test_update_email_fail(self):
        """"
        Mocking failure of update_email in main.py
        """
        user_collection = MagicMock()
        mock_user = MagicMock()
        # Trick main.update_email into thinking that update_email in users.py
        # could not find the user_id
        user_collection.update_email.return_value = None
        # Verify that the function that was passed to the main.update_email returned False
        self.assertFalse(main.update_email(mock_user.user_id, mock_user.email, user_collection))

    def test_add_status_success(self):
        """
        Mocking add_status in main.py
        """
        # Leveraging MagicMock instead of User to test main.add_status
        # in isolation
        mock_user = MagicMock()
        # Setting values to pre-seeded data. Add_status is dependent on there
        # being a user. So we mock user first.
        mock_user.user_id = "serena.tennis"
        mock_user.user_name = "Serena"
        mock_user.user_last_name = "Williams"
        mock_user.email = "serena.tennis@gmail.com"
        user_collection = MagicMock()
        # Add mock_user to mocked user_collection instance
        user_collection.add_user.return_value = mock_user
        # now mock status instance
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "serena.tennis_00001"
        mock_status.user_id = "serena.tennis"
        mock_status.status_text = "I don't like to lose"
        # Make sure add_status in user_status.py returns a UserStatus object to
        # main.add_status
        status_collection.add_status.return_value = mock_status
        # calling add_status on our mocked status_collection
        new_status = main.add_status(mock_status.status_id, mock_user.user_id,
                                     mock_status.status_text, status_collection)
        # Compare the two add_status functions in main and user_status.py.
        # They should return the same UserStatus object
        self.assertEqual(new_status, mock_status)
        # Verify that main.add_status called add_status in user_status.py
        # with our mock data
        status_collection.add_status.assert_called_with("serena.tennis_00001", "serena.tennis",
                                                        "I don't like to lose")

    def test_search_status_success(self):
        """
        Mocking search_status in main.py
        """
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "serena.tennis_00001"
        # Hard code user_id, so we don't have to mock user as well.
        mock_status.user_id = "serena.tennis"
        mock_status.status_text = "I don't like to lose"
        # Verify that main.search_status() called search_status()
        # and that search_status() in user_status.py returned a result
        # to main.search_status()
        self.assertIsNotNone(main.search_status(mock_status.status_id, status_collection))
        # Verify that the method was called with our mock data "serena.tennis_00001"
        status_collection.search_status.assert_called_with("serena.tennis_00001")

    def test_search_status_not_found(self):
        """
        Mocking failure of search_status in main.py
        """
        status_collection = MagicMock()
        mock_status = MagicMock()
        # Trick main.search_status into thinking that search_status in user_status.py
        # could not find the status_id in UserStatusTable and returned None.
        status_collection.search_status.return_value = None
        # Verify that main.search_status also returns None
        self.assertIsNone(main.search_status(mock_status.status_id, status_collection))

    def test_delete_status_success(self):
        """
        Mocking delete_status in main.py
        """
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "serena.tennis_00002"
        # Hard code user_id, so we don't have to mock user as well.
        mock_status.user_id = "serena.tennis"
        mock_status.status_text = "You have to believe in yourself when no one else does."
        # Verify that main.delete_status() also returns True
        self.assertTrue(main.delete_status(mock_status.status_id, status_collection))
        # Verify that main.delete_status called delete_status() in user_status.py
        # with mock data
        status_collection.delete_status.assert_called_with("serena.tennis_00002")

    def test_delete_status_fail(self):
        """
        Mocking failure of delete_status in main.py
        """
        status_collection = MagicMock()
        mock_status = MagicMock()
        # Trick main.delete_status into thinking that delete_status in user_status.py
        # could not find the status_id in UserStatusTable and returned None.
        status_collection.delete_status.return_value = None
        # Verify that main.delete_status also returns None
        self.assertFalse(main.delete_status(mock_status.status_id, status_collection))

    def test_update_status_success(self):
        """
        Mocking update_status in main.py
        """
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "madonna_lyrics_00001"
        # Hard coding Madonna's user_id to avoid mocking up user as well
        mock_status.user_id = "madonna_lyrics"
        mock_status.status_text = "You're frozen when your heart's not open"
        # Verify that update_status_text in user_status.py returned a result
        # to main_update_status(). The result is a magicMock object, but the
        # method main_update_status() calls also returns True
        self.assertTrue(main.update_status(mock_status.status_id,
                                            mock_status.status_text, status_collection))
        # Verify the original user_status.update_status_text that was passed to
        # main.update_status was called with our mocked two values
        status_collection.update_status_text.assert_called_with("madonna_lyrics_00001",
                                            "You're frozen when your heart's not open")

    def test_update_status_fail(self):
        """
        Mocking failure of update_status in main.py
        """
        status_collection = MagicMock()
        mock_status = MagicMock()
        mock_status.status_id = "simba_lion_00001"
        mock_status.status_text = "I am king of the safari"
        # Trick main.update_status into thinking that update_status in user_status.py
        # could not find the status_id in UserStatusTable and returned None.
        status_collection.update_status_text.return_value = None
        # Verify that main.delete_status also returns None
        self.assertIsNone(main.update_status(mock_status.status_id, mock_status.status_text,
                                            status_collection))
