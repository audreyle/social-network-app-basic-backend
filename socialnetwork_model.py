from pymongo import MongoClient

mongo = MongoClient()
database = mongo.UserStatuses
user_collection = database["users"]
status_collection = database["status"]