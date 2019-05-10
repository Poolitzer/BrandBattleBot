import praw
import logging
from constants import REPORT


class Reddit:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.reddit = praw.Reddit(client_id='',
                                  client_secret='',
                                  user_agent='A battling Bot',
                                  username='BrandConnoisseur',
                                  password='ABattlingBrandPasswort!')
        self.logger.info("Successfully started reddit instance")

    def get_submission(self, submission_id):
        self.logger.info("Got submission " + submission_id)
        return self.reddit.submission(id=submission_id)

    def get_new_submissions(self):
        self.logger.info("Got new submissions")
        return self.reddit.subreddit("battleofthebrands").new()

    def reply_submission(self, submission_id, reply):
        comment = self.reddit.submission(id=submission_id).reply(reply)
        comment.mod.distinguish(how='yes', sticky=True)
        self.logger.info("Succesfully created initial comment and stickied it. Id: " + submission_id)
        return comment.id

    def reply_comment(self, comment_id, reply):
        self.logger.info("Replied to " + comment_id)
        return self.reddit.comment(id=comment_id).reply(reply).id

    def report(self, submission_id):
        self.logger.info("Reported the following post: " + submission_id)
        self.reddit.submission(id=submission_id).report(REPORT)

    def get_comment(self, comment_id):
        comment = self.reddit.comment(id=comment_id)
        comment.refresh()
        self.logger.info("Sucesfully got the comment " + comment_id)
        return comment.score

    def edit_comment(self, comment_id, body):
        self.logger.info("will edit comment: " + comment_id)
        self.reddit.comment(id=comment_id).edit(body)


reddit = Reddit()
