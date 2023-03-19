"""
main driver for a simple social network project
"""
import sys
from csv import DictReader

from pymongo.errors import DuplicateKeyError, BulkWriteError
from loguru import logger
import users
import user_status
from socialnetwork_model import database, mongo


logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')

logger.debug("This is a debug")
logger.info("This is an info")
logger.warning("This is a warning")
logger.error("This is an error")



def init_user_collection():
    """
    Creates and returns a new instance of UserCollection, and
    binds it to the UserStatuses database I created in
    socialnetwork_model.py
    """
    return users.UserCollection(database)


def init_status_collection():
    """
    Creates and returns a new instance of StatusCollection
    """
    return user_status.StatusCollection(database)


def add_user(user_id, first_name, last_name, email, user_collection):
    """
    Takes all the user inputs from menu.py and creates a new user
    in our user_collection, which it stores in the users table I bound to
    my UserStatuses database in users.py.

    Requirements:
    - user_id cannot already exist in the database.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """
    if not user_collection.add_user(user_id, first_name, last_name, email):
        print(f'{user_id} already exists.')
    print(f'{user_id} added.')


def add_status(status_id, user_id, status_text, user_collection, status_collection):
    """
    Takes all the user inputs from menu.py and creates a new status
    in our status_collection, which it stores in the status table I bound to
    my UserStatuses database in user_status.py.

    Requirements:
    - User_id must exist in the users table before we can add a status.
    If our search_user returns None, the code skips insert_one and prints
    a message to remind user to add a user before adding a status.
    - Next, it checks that the status_id is new. If the status_id already
    exists, it prints an error message.
    - Otherwise, it returns True and alerts the user that their status was added.
    """
    result = user_collection.search_user(user_id)
    # users.search_user returns None if the user_id can't be found.
    if result is None:
        print(f'{user_id} does not exist! Please add a user first before adding a status')
    # if user_id exists, call user_status.add_status
    else:
        status = status_collection.add_status(status_id, user_id, status_text)
        # if status_id does not exist, user_status.add_status will write the new status to
        # database and return True.
        if status: # status should be True.
            print(f'{status_id} added.')
            # if status is False owing to duplicate key, print error message
        else:
            print(f'{status_id} already exists.')




def delete_user(user_id, user_collection, status_collection):
    """
    Delete a user in our status_collection by calling delete_user in users.py
    which does a delete_one in our users table.

    Requirements:
    - Checks and deletes the statuses published by the user_id
    first before deleting the user.
    - If the user_id can't be found in the database, status is
    None and prints the error message.
    - if status is True, it deletes each status and prints a success message
    for each.
    - Finally, it deletes the user. If the user_id does not exist,
    result is None and an error message is printed.
    - If the user_id exists, the result is True and prints a success message
    once user is successfully deleted.
    - If the user_id exists, but no statuses are found in status
    collection, the code skips to delete_user.
    """
    # if user is to be deleted, search for their statuses and delete them before
    for status in status_collection.search_status_by_id(user_id):
        if status:
            status_collection.delete_status(status["_id"])
            print(f'Since {user_id} no longer exists, we took care to delete '
                  f'their messages: {status["_id"]}.')
        else:
            print(f'Verified {user_id} did not have any statuses to delete.')
    # now we can delete the user
    result = user_collection.delete_user(user_id)
    if result is None:
        print(f'{user_id} cannot be deleted because it does not exist.')
    else:
        print(f'{user_id} deleted.')

def search_status_by_id(user_id, status_collection):
    """
    This method allows us to query all statuses published by user_id
    and is called by main.delete_user to make sure we can delete the
    statuses associated by a user account when we delete the user.

    Since the corresponding user_status.search_status_by_id function
    returns an iterable status object, we can use a for loop to iterate
    through each status it finds to delete them one by one.
    """
    for status in status_collection.search_status_by_id(user_id):
        return status
def delete_status(status_id, status_collection):
    """
    Delete a status in our status_collection by calling delete_status in users.py
    which does a delete_one in our status table.

    Requirements:
    - If the status_id can't be found in the database, returns
    None
    - Otherwise, it returns True.
    """
    result = status_collection.delete_status(status_id)
    if result is None:
        print(f'Cannot delete {status_id} because it does not exist')
    print(f'{status_id} deleted.')


def search_user(user_id, user_collection):
    """
    Searches for a user in our user_collection by calling
    search_user in users.py.

    Requirements:
    - If the user_id exists in the users table, users.search_user
    returns the corresponding pymongo object. main calls
    print_user to look inside that object.
    - Returns None and prints an error message if user_id
    does not exist.
    """
    result = user_collection.search_user(user_id)
    if result is None:
        print(f'{user_id} does not exist...')
    else:
        for result in result:
            print_user(result)


def search_status(status_id, status_collection):
    """
    Searches for a status in our status_collection by calling
    search_status in status.py.

    Requirements:
    - If the status_id exists, user_status.search_status
    returns a pymongo object. main calls print_status to
    allow us to look inside that object.
    - Returns None and prints an error message if status_id
    does not exist.
    """
    for status in status_collection.search_status(status_id):
        if status is None:
            print(f'{status_id} does not exist.')
        else:
            print_status(status)


def print_user(user):
    """
    Prints the contents of the pymongo object returned by
    methods in users.py
    """
    print(
        f'{user["NAME"]} {user["LASTNAME"]} has user ID: {user["_id"]} '
        f'and email address: {user["EMAIL"]}'
    )

def print_status(status):
    """
    Prints the contents of the pymongo object returned by
    methods in user_status.py
    """
    print(
        f'#{status["_id"]}: {status["USER_ID"]} wrote "{status["STATUS_TEXT"]}"'
    )


def update_user(user_id, first_name, last_name, email, user_collection):
    """
    Updates a user's information if the user_id already exists. First it calls
    update_user in users.py which looks up the user by user_id. If it can't find
    it in the users table, the result in our main function is None. If successful,
    main.update_user returns True.
    """
    updated_user = user_collection.update_user(user_id, first_name, last_name, email)
    if updated_user is None:
        print(f'{user_id} cannot be updated because it does not.')
    else:
        print("User updated.")


def update_status(status_id, status_text, status_collection):
    """
    Updates a status text if the status_id already exists.
    Returns True if successful.
    Returns None if the status_id can't be found in the status table.
    """
    updated_status = status_collection.update_status(status_id, status_text)
    if updated_status is None:
        print(f'{status_id} cannot be updated because it does not exist.')
    else:
        print("Status updated.")


def load_users(user_file, user_collection):
    """
    Loads user data from accounts.csv row by row. Raises an exception if the seed
    data already exists in our users table.

    I should point out that if you add to the csv, Mongodb just stops when it detects
    that there's duplicate data. It doesn't continue to upload the data even if
    some of it is new.
    """
    try:
        with open(user_file, 'r', encoding="utf-8") as file:
            data = list(DictReader(file))
            for row in data:
                user_collection.add_user(row["USER_ID"], row["NAME"], row["LASTNAME"], row["EMAIL"])
    except (DuplicateKeyError, BulkWriteError):
        print("Already seeded user data...")
    except FileNotFoundError:
        print("User file not found.")


def load_status(status_file, status_collection):
    """
    Loads status data from status_updates.csv row by row. Raises an exception if the seed
    data already exists in our users table.
    """
    try:
        with open(status_file, 'r', encoding="utf-8") as file:
            data = list(DictReader(file))
            for row in data:
                status_collection.add_status(row["STATUS_ID"], row["USER_ID"], row["STATUS_TEXT"])
    except (DuplicateKeyError, BulkWriteError):
        print("Already seeded status data...")
    except FileNotFoundError:
        print("Status file not found")


def exit_program():
    """
    Exits the program and wipes out our users and status tables from memory.
    """
    user_input = input("Would you like to drop the tables? [y/n]").lower()
    if user_input == "y":
        database["users"].drop()
        database["status"].drop()
        mongo.close()
