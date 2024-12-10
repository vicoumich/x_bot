import asyncio
import aiosqlite
import logging
import re
import json
# Configure logging
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
)


class TweetDatabaseManager:
    def __init__(self, db_name="../data/bot.db"):
        self.db_name = db_name
        self.conn = None

    async def init(self):
        self.conn = await aiosqlite.connect(self.db_name)
        await self._create_tweet_table()

    async def _create_tweet_table(self):
        """
        Create the 'tweets' table if it doesn't already exist, with extended attributes.
        """
        async with self.conn:
            await self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tweets (
                    id BIGINT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    created_at_datetime TIMESTAMP,
                    text TEXT NOT NULL,
                    lang TEXT,
                    in_reply_to BIGINT,
                    is_quote_status BOOLEAN,
                    quote_id BIGINT,
                    retweeted_tweet_id BIGINT,
                    possibly_sensitive BOOLEAN,
                    possibly_sensitive_editable BOOLEAN,
                    quote_count INT,
                    media TEXT,
                    reply_count INT,
                    favorite_count INT,
                    favorited BOOLEAN,
                    view_count INT,
                    view_count_state TEXT,
                    retweet_count INT,
                    place TEXT,
                    editable_until_msecs BIGINT,
                    is_translatable BOOLEAN,
                    is_edit_eligible BOOLEAN,
                    edits_remaining INT,
                    hashtags TEXT,
                    has_card BOOLEAN,
                    thumbnail_title TEXT,
                    thumbnail_url TEXT,
                    urls TEXT,
                    full_text TEXT
                )
            ''')
            await self.conn.commit()
            logging.info("Table 'tweets' created or already exists.")


    # def extract_hashtags(self, content):
    #     """
    #     Extract hashtags from the tweet content.

    #     :param content: The text content of the tweet.
    #     :return: A comma-separated string of hashtags.
    #     """
    #     hashtags = re.findall(r"#\w+", content)
    #     return ",".join(hashtags)

    async def add_tweet(self, tweet):
        """
        Add a tweet to the database.

        :param tweet: The tweet object containing all attributes.
        """
        async with self.conn:
            await self.conn.execute('''
                INSERT OR REPLACE INTO tweets (
                    id, user_id, created_at, created_at_datetime, text, lang,
                    in_reply_to, is_quote_status, quote_id, retweeted_tweet_id,
                    possibly_sensitive, possibly_sensitive_editable, quote_count, media,
                    reply_count, favorite_count, favorited, view_count, view_count_state,
                    retweet_count, place, editable_until_msecs, is_translatable,
                    is_edit_eligible, edits_remaining, replies, reply_to, related_tweets,
                    hashtags, has_card, thumbnail_title, thumbnail_url, urls, full_text
                ) VALUES (
                    ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (
                tweet.id,
                tweet.user.id,
                tweet.created_at,
                tweet.created_at_datetime,
                tweet.text,
                tweet.lang,
                tweet.in_reply_to,
                tweet.is_quote_status,
                getattr(tweet, 'quote', {}).get('id') if tweet.is_quote_status else None,
                getattr(tweet, 'retweeted_tweet', {}).get('id'),
                tweet.possibly_sensitive,
                tweet.possibly_sensitive_editable,
                tweet.quote_count,
                json.dumps(tweet.media) if tweet.media else None,
                tweet.reply_count,
                tweet.favorite_count,
                tweet.favorited,
                tweet.view_count,
                tweet.view_count_state,
                tweet.retweet_count,
                json.dumps(tweet.place) if tweet.place else None,
                tweet.editable_until_msecs,
                tweet.is_translatable,
                tweet.is_edit_eligible,
                tweet.edits_remaining,
                # json.dumps(tweet.replies) if tweet.replies else None,
                # json.dumps(tweet.reply_to) if tweet.reply_to else None,
                # json.dumps(tweet.related_tweets) if tweet.related_tweets else None,
                json.dumps(tweet.hashtags) if tweet.hashtags else None,
                tweet.has_card,
                tweet.thumbnail_title,
                tweet.thumbnail_url,
                json.dumps(tweet.urls) if tweet.urls else None,
                tweet.full_text
            ))
            await self.conn.commit()
            logging.info(f"Tweet ID {tweet.id} added to database.")


    async def get_tweets(self, user_id=None):
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
        
        cursor = await self.conn.execute(query, params)
        return [dict(row) for row in await cursor.fetchall()]

    async def close(self):
        if self.conn:
            await self.conn.close()


class UserDatabaseManager:
    def __init__(self, db_name="../data/bot.db"):
        self.db_name = db_name
        self.conn = None

    async def init(self):
        self.conn = await aiosqlite.connect(self.db_name)
        await self._create_user_table()

    async def _create_user_table(self):
        async with self.conn:
            await self.conn.execute('''
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
            await self.conn.commit()
    
    async def add_user(self, user):
        """
        Ajoute ou met à jour un utilisateur dans la base de données. 
        Gère les champs manquants en leur attribuant des valeurs par défaut.
        """
        async with self.conn:
            await self.conn.execute('''
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

            await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()