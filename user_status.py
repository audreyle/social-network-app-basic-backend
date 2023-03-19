"""
Database methods for status collection
"""
import sys
from pymongo.errors import DuplicateKeyError

from loguru import logger

logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')


class StatusCollection:
    """
    Creating a StatusCollection class to instantiate a status table
    in my UserStatuses MongoDB database.
    """
    def __init__(self, database):
        """
        Please make sure to change "status" to "test_status" for unit testing!
        """
        self.database = database["status"]

    def add_status(self, status_id, user_id, status_text):
        """
        Adds a new status to the status table of my UserStatuses database.
        If the status_id already exists, it raises a DuplicateKeyError and returns
        False. Otherwise, it returns True.
        """
        try:
            self.database.insert_one(
                {"_id": status_id, "USER_ID": user_id, "STATUS_TEXT": status_text}
            )
            return True
        except DuplicateKeyError:
            return False


    def delete_status(self, status_id):
        """
        Deletes a status in the status table of my UserStatuses database if the
        status_id exists and returns True. If it doesn't, it returns None.

        """
        query = {'_id': status_id}
        if self.database.count_documents(query) == 0:
            return None
        self.database.delete_one({"_id": status_id})
        return True


    def search_status(self, status_id):
        """
        Searches for status in the status table of UserStatuses database
        and returns a pymongo status object.

        If the status_id does not exist the content of the returned object
        will actually be None. Adding "Return None" here will not make
        a difference.

        Also, the corresponding function in main.py can read the object
        and recognize that it is None and print an error message.
        """
        query = {'_id': status_id}
        if self.database.count_documents(query) == 0:
            return None
        return self.database.find({"_id": status_id})

    def search_status_by_id(self, user_id):
        """"
        Searches for all statuses by user_id in the status table
        """
        # query = {'USER_ID': user_id}
        # if self.database.count_documents(query) == 0:
        #     return None
        return self.database.find({"USER_ID": user_id})


    def update_status(self, status_id, status_text):
        """"
        Updates a status if a status id can be found in the status table
        of UserStatuses database. If the status_id does not exist,
        it returns None. Otherwise, it returns True.
        """
        query = {'_id': status_id}
        if self.database.count_documents(query) == 0:
            return None
        new_data = {"STATUS_TEXT": status_text}
        self.database.update_one(query, {"$set": new_data})
        return True
