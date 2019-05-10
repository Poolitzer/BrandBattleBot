import aiocron
from reddit_instance import reddit
from Database import database
from utils import get_percentages
from constants import INITIAL_REPLY
from time import time
from datetime import datetime
import logging


@aiocron.crontab('* * */1 * *')
async def daily_cron():
    logger = logging.getLogger(__name__)
    logger.info("Started daily function: " + datetime.now().strftime("%d.%m-%H:%M:%S"))
    for submission in database.get_submissions("daily"):
        first_id = next(iter(submission["first_vote"]))
        first_score = reddit.get_comment(first_id)
        second_id = next(iter(submission["second_vote"]))
        second_score = reddit.get_comment(second_id)
        if database.insert_votes("daily", submission["submission"], first_score, second_score):
            percentages = get_percentages(first_score, second_score)
            brands = submission["brands"]
            addition = "This comment will be updated daily.*"
            body = INITIAL_REPLY.format(first_brand=brands[0], first_percent=percentages[0],
                                        second_brand=brands[1], second_percent=percentages[1]) + addition
            reddit.edit_comment(submission["initial"], body)
        if int(time()) - submission["utc"] >= (604800 + 86400 + 18000):
            database.to_weekly(submission["submission"])
    logger.info("Finished daily function: " + datetime.now().strftime("%d.%m-%H:%M:%S"))
