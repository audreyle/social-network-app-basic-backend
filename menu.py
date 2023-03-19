"""
Provides a basic frontend
"""

import sys
from loguru import logger
import main

logger.remove()
logger.add('loguru_file_{time:YYYY-MM-DD}.log', level='DEBUG')
logger.add(sys.stderr, level='WARNING')



def load_users(user_collection):
    """
    Loads user accounts from a file
    """
    user_file = input("Which user file would you like to upload? ")
    main.load_users(user_file, user_collection)


def load_status(status_collection):
    """
    Loads status updates from a file
    """
    status_file = input("Which status file would you like to upload? ")
    main.load_status(status_file, status_collection)


def add_user(user_collection):
    """
    Adds a new user into the database
    """
    user_id = input("User ID: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    main.add_user(user_id, first_name, last_name, email, user_collection)


def add_status(user_collection, status_collection):
    """
    Adds a new status into the database
    """
    status_id = input("Status ID: ")
    user_id = input("User ID: ")
    status_text = input("Status text: ")
    main.add_status(status_id, user_id, status_text, user_collection, status_collection)


def delete_user(user_collection, status_collection):
    """
    Deletes user from the database
    """
    user_id = input("User ID: ")
    main.delete_user(user_id, user_collection, status_collection)


def delete_status(status_collection):
    """
    Deletes status from the database
    """
    status_id = input("Status id: ")
    main.delete_status(status_id, status_collection)


def search_user(user_collection):
    """
    Searches a user in the database
    """
    user_id = input("Enter a user ID to search: ")
    main.search_user(user_id, user_collection)


def search_status(status_collection):
    """
    Searches a status in the database
    """
    status_id = input("Enter a status ID to search: ")
    main.search_status(status_id, status_collection)

def search_status_by_id(status_collection):
    """
    This function will likely not be called until we delete a user.
    But if you're interested, you can enter a user_id and get a list
    of all the statuses they've published.
    """
    user_id = input ("Enter a user_id to search their statuses")
    main.search_status_by_id(user_id, status_collection)

def update_user(user_collection):
    """
    Updates information for an existing user
    """
    user_id = input("Enter a user ID to update: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    main.update_user(user_id, first_name, last_name, email, user_collection)


def update_status(status_collection):
    """
    Updates the status_text of an existing status
    """
    status_id = input("Enter a status ID to update: ")
    status_text = input("Update status text to: ")
    main.update_status(status_id, status_text, status_collection)


if __name__ == "__main__":
    uc = main.init_user_collection()
    sc = main.init_status_collection()
    try:
        while True:
            response = input(
                "a to add to users\n"
                "b to add to status\n"
                "c to remove from users\n"
                "d to remove from status\n"
                "e to search in users\n"
                "f to search in status\n"
                "i to update user\n"
                "j to update status\n"
                "k to load users\n"
                "l to load status\n"
                "m to search for all statuses by user_id\n"
                "q to quit\n"
                "Enter option: "
            ).lower()
            if response == "a":
                add_user(uc)
            elif response == "b":
                add_status(uc, sc)
            elif response == "c":
                delete_user(uc, sc)
            elif response == "d":
                delete_status(sc)
            elif response == "e":
                search_user(uc)
            elif response == "f":
                search_status(sc)
            elif response == "i":
                update_user(uc)
            elif response == "j":
                update_status(sc)
            elif response == "k":
                load_users(uc)
            elif response == "l":
                load_status(sc)
            elif response == "m":
                search_status_by_id(sc)
            elif response == "q":
                main.exit_program()
            else:
                print("Unknown command", file=sys.stderr)
    except KeyboardInterrupt:
        main.exit_program()
