import aiocron
from reddit_instance import reddit
from Database import database
from utils import get_brands
from constants import INITIAL_REPLY, COMMENT
from datetime import datetime
from time import time
import logging


@aiocron.crontab('*/1 * * * *')
async def get_new_submission():
    logger = logging.getLogger(__name__)
    logger.info("Started submission function: " + datetime.now().strftime("%d.%m-%H:%M:%S"))
    for submission in reddit.get_new_submissions():
        sub_id = submission.id
        if database.find_submission(sub_id):
            logger.info("Skipped post: " + sub_id)
            pass
        else:
            logger.info("Started adding post: " + sub_id)
            brands = get_brands(submission.title)
            if brands:
                addition = "This comment will be updated every five minutes.*"
                body = INITIAL_REPLY.format(first_brand=brands[0], first_percent="0%",
                                            second_brand=brands[1], second_percent="0%") + addition
                ini_id = reddit.reply_submission(sub_id, body)
                first_id = reddit.reply_comment(ini_id, COMMENT.format(brand=brands[0]))
                second_id = reddit.reply_comment(ini_id, COMMENT.format(brand=brands[1]))
                database.insert_comment(sub_id, ini_id, first_id, second_id, int(time()), brands)
                logger.info("Finished adding post: " + sub_id)
            else:
                if not database.find_ignore(sub_id):
                    reddit.report(sub_id)
                    database.insert_ignore(sub_id)
            pass
    logger.info("Finished submission function: " + datetime.now().strftime("%d.%m-%H:%M:%S"))
