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
    def __init__(self, db_name="../data/bot.db"):
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



class UserDatabaseManager:
    def __init__(self, db_name="./db/data.db"):
        self.conn = sqlite3.connect(db_name)
        self._create_user_table()

    def _create_user_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    screen_name TEXT,
                    name TEXT,
                    description TEXT,
                    location TEXT,
                    followers_count INT,
                    friends_count INT,
                    statuses_count INT,
                    favourites_count INT,
                    created_at TIMESTAMP,
                    verified BOOLEAN,
                    profile_image_url TEXT,
                    profile_banner_url TEXT,
                    last_tweet_id BIGINT,
                    last_active_at TIMESTAMP,
                    protected BOOLEAN
                )
            ''')

    def add_user(self, user):
        """
        Ajoute ou met à jour un utilisateur dans la base de données. 
        Gère les champs manquants en leur attribuant des valeurs par défaut.
        """
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO users (
                    id, screen_name, name, description, location, 
                    followers_count, friends_count, statuses_count, 
                    favourites_count, created_at, verified, 
                    profile_image_url, profile_banner_url, 
                    last_tweet_id, last_active_at, protected
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                # Utilisation de getattr ou user.get selon le type de user
                user.get('id') if isinstance(user, dict) else getattr(user, 'id', None),
                user.get('screen_name') if isinstance(user, dict) else getattr(user, 'screen_name', None),
                user.get('name') if isinstance(user, dict) else getattr(user, 'name', None),
                user.get('description') if isinstance(user, dict) else getattr(user, 'description', None),
                user.get('location') if isinstance(user, dict) else getattr(user, 'location', None),
                user.get('followers_count', 0) if isinstance(user, dict) else getattr(user, 'followers_count', 0),
                user.get('friends_count', 0) if isinstance(user, dict) else getattr(user, 'friends_count', 0),
                user.get('statuses_count', 0) if isinstance(user, dict) else getattr(user, 'statuses_count', 0),
                user.get('favourites_count', 0) if isinstance(user, dict) else getattr(user, 'favourites_count', 0),
                user.get('created_at') if isinstance(user, dict) else getattr(user, 'created_at', None),
                user.get('verified', False) if isinstance(user, dict) else getattr(user, 'verified', False),
                user.get('profile_image_url') if isinstance(user, dict) else getattr(user, 'profile_image_url', None),
                user.get('profile_banner_url') if isinstance(user, dict) else getattr(user, 'profile_banner_url', None),
                user.get('last_tweet_id') if isinstance(user, dict) else (
                    user.status.id if hasattr(user, 'status') else None
                ),
                user.get('last_active_at') if isinstance(user, dict) else (
                    user.status.created_at if hasattr(user, 'status') else None
                ),
                user.get('protected', False) if isinstance(user, dict) else getattr(user, 'protected', False)
            ))
