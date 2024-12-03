import sqlite3

class UserDatabaseManager:
    def __init__(self, db_name="../db/data.db"):
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
                user.id, user.screen_name, user.name, user.description, user.location,
                user.followers_count, user.friends_count, user.statuses_count,
                user.favourites_count, user.created_at, user.verified,
                user.profile_image_url, user.profile_banner_url,
                user.status.id if hasattr(user, 'status') else None,
                user.status.created_at if hasattr(user, 'status') else None,
                user.protected
            ))
