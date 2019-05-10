from pymongo import MongoClient
from constants import COLLECTIONS
import logging


class Database:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Database init")
        self.db = MongoClient()
        self.db = self.db["brandbattlebot"]

    def find_submission(self, submission_id):
        for collection in COLLECTIONS:
            if self.db[collection].find_one({"submission": submission_id}):
                return True
        return False

    def find_ignore(self, submission_id):
        if self.db.ignore.find_one({"submission": submission_id}):
            return True
        return False

    def insert_ignore(self, submission_id):
        self.db.ignore.insert_one({"submission": submission_id})

    def insert_comment(self, submission_id, initial_id, first_id, second_id, created_utc, brands):
        base = {"submission": submission_id, "initial": initial_id, "first_vote": {first_id: 0},
                "second_vote": {second_id: 0}, "utc": created_utc, "brands": brands}
        self.db.minutely.insert_one(base)

    def get_submissions(self, collection):
        return self.db[collection].find()

    def insert_votes(self, collection, submission_id, first_score, second_score):
        temp = self.db[collection].find_one({"submission": submission_id})
        if temp["first_vote"][next(iter(temp["first_vote"]))] != first_score or \
                temp["second_vote"][next(iter(temp["second_vote"]))] != second_score:
            self.db[collection].update_one({"submission": submission_id},
                                           {"$set": {"first_vote." + next(iter(temp["first_vote"])): first_score,
                                                     "second_vote." + next(iter(temp["second_vote"])): second_score}})
            return True
        else:
            return False

    def to_hourly(self, submission_id):
        temp = self.db.minutely.find_one({"submission": submission_id})
        self.db.hourly.insert_one(temp)
        self.db.minutely.delete_one({"submission": submission_id})

    def to_daily(self, submission_id):
        temp = self.db.hourly.find_one({"submission": submission_id})
        self.db.daily.insert_one(temp)
        self.db.hourly.delete_one({"submission": submission_id})

    def to_weekly(self, submission_id):
        temp = self.db.daily.find_one({"submission": submission_id})
        self.db.weekly.insert_one(temp)
        self.db.daily.delete_one({"submission": submission_id})


database = Database()
