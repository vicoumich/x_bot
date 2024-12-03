import sqlite3
import logging
import re

# Configure logging
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
)


class TweetDatabaseManager:
    def __init__(self, db_name="bot.db"):
        self.conn = sqlite3.connect(db_name)
        self._create_tweet_table()

    def _create_tweet_table(self):
        """
        Create the 'tweets' table if it doesn't already exist.
        """
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tweets (
                    id BIGINT PRIMARY KEY,
                    user_id BIGINT,
                    created_at TIMESTAMP,
                    retweets_count INT,
                    likes_count INT,
                    hashtags TEXT
                )
            ''')
            logging.info("Table 'tweets' created or already exists.")

    def extract_hashtags(self, content):
        """
        Extract hashtags from the tweet content.

        :param content: The text content of the tweet.
        :return: A comma-separated string of hashtags.
        """
        hashtags = re.findall(r"#\w+", content)
        return ",".join(hashtags)

    def add_tweet(self, tweet):
        """
        Add a tweet to the database.

        :param tweet: The tweet object returned by the Twitter API.
        """
        hashtags = self.extract_hashtags(tweet.text)
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO tweets (
                    id, user_id, created_at, retweets_count, likes_count, hashtags
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                tweet.id,
                tweet.user.id,
                tweet.created_at,
                tweet.retweet_count,
                tweet.favorite_count,
                hashtags
            ))
            logging.info(f"Tweet ID {tweet.id} added to database.")

    def get_tweets(self, user_id=None):
        """
        Retrieve tweets from the database, optionally filtered by user_id.

        :param user_id: The ID of the user whose tweets to retrieve.
        :return: A list of tweets as dictionaries.
        """
        query = "SELECT * FROM tweets"
        params = ()
        if user_id:
            query += " WHERE user_id = ?"
            params = (user_id,)
        
        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
