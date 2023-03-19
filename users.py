"""
Database methods for user collection
"""
import sys
from pymongo.errors import DuplicateKeyError

from loguru import logger

logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')


class UserCollection:
    """
    Creating a User Collection class to instantiate users table in
    my UserStatuses MongoDB database.
    """
    def __init__(self, database):
        """
        Please make sure to change "users" to "test_users" for unit testing!
        """
        self.database = database["users"]

    def add_user(self, user_id, first_name, last_name, email):
        """
        Adds a new user to the users table of my UserStatuses database.
        If the user_id already exists, it raises a DuplicateKeyError and returns
        False. Otherwise, it returns True.
        """
        try:
            self.database.insert_one(
                {"_id": user_id, "NAME": first_name, "LASTNAME": last_name, "EMAIL": email})
            return True
        except DuplicateKeyError:
            return False


    def delete_user(self, user_id):
        """
        Deletes a user in the users table of my UserStatuses database if the
        user_id exists and returns True. If it doesn't, it returns None.
        """
        query = {'_id': user_id}
        if self.database.count_documents(query) == 0:
            return None
        self.database.delete_one({"_id": user_id})
        return True


    def search_user(self, user_id):
        """
        Searches for a user in the users table of the UserStatuses database
        and returns the user object.

        Returns None if the user does not exist.
        """
        query = {'_id': user_id}
        if self.database.count_documents(query) == 0:
            return None
        return self.database.find({"_id": user_id})


    def update_user(self, user_id, first_name, last_name, email):
        """
        Updates the information on a user. Returns None if the user does not exist.
        If the user exists, it returns True.
        """
        query = {'_id': user_id}
        if self.database.count_documents(query) == 0:
            return None
        new_data = {"NAME": first_name, "LASTNAME": last_name, "EMAIL": email}
        self.database.update_one(query, {"$set": new_data})
        return True
