import praw
import sqlite3

from . import utils

r = praw.Reddit(user_agent="Pulls post data information in" +
                           " intervals and stores it")

def writetoDB(data):
    sqlStatement = """
    INSERT INTO post_updates(post_id, score, ratio, num_comments, timestamp_update)
        VALUES(
            %s,
            %d,
            %f,
            %d,
            %d
        );
    """


class RedditBot:
    def __init__(self, postID):
        self.postID = postID
        self.updateTimestamp = utils.getTime()
        self.recentData = None

    def newPost(self):
        print("New post! %s" % (self.postID))
        post = r.get_submission(submission_id=self.postID)
        newData = {
            'post_id': self.postID,
            'link': post.permalink,
            'subreddit': post.subreddit.display_name,
            'title': post.title,
            'author': post.author.name,
            'timestamp_created': int(post.created_utc)
        }
        return newData

    def updateData(self):
        print("Updating post %s" % (self.postID))
        update = r.get_submission(submission_id=self.postID)
        newData = {
            'post_id': self.postID,
            'score': update.score,
            'ratio': update.upvote_ratio,
            'num_comments': update.num_comments,
            'timestamp_update': utils.getTime()
        }
        print("Caching data...")
        return newData
