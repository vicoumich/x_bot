# bot/api_client.py

from twikit import Client, User
import logging
import os
from .config import (
    USERNAME,
    PASSWORD,
    EMAIL,
    COOKIE_PATH
)

# Configure logging
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
)


class TwitterAPI:
    def __init__(self):
        """
        Initialize the Twitter API client using credentials from config.py.
        Saves cookies if doesn't exists.
        """
        # self.api = tweepy.Client(bearer_token=BAREAR_TOKEN)
        self.client = Client('en-US')
        # try:
        #     if os.path.exists(COOKIE_PATH):
        #         self.client.load_cookies(COOKIE_PATH)
        #         print('using cookies')
        #     else:
        #         print('using login')
        #         info_login = self.client.login(
        #             auth_info_1=USERNAME,
        #             auth_info_2=EMAIL,
        #             password=PASSWORD
        #         )
        #         print(info_login)
        #         print(f"\n\n\n type info login: {type(info_login)}")
        #         self.client.save_cookies(COOKIE_PATH)
        # except Exception as e:
        #     logging.error(f"Error during Twitter API authentication: {e}")
        #     raise e
        
    async def init(self):
        try:
            if os.path.exists(COOKIE_PATH):
                self.client.load_cookies(COOKIE_PATH)
                print('using cookies')
            else:
                print('using login')
                info_login = await self.client.login(
                    auth_info_1=USERNAME,
                    auth_info_2=EMAIL,
                    password=PASSWORD
                )
                print(info_login)
                print(f"\n\n\n type info login: {type(info_login)}")
                self.client.save_cookies(COOKIE_PATH)
        except Exception as e:
            logging.error(f"Error during Twitter API authentication: {e}")
            raise e

    def _parse_user(self, user:User) -> dict:
        user_info = {
                "id": user.id,
                "screen_name": user.screen_name,
                "name": user.name,
                "description": user.description,
                "location": user.location,
                "is_blue": user.is_blue_verified,
                "followers_count": user.followers_count,
                "following_count": user.following_count,
                "statuses_count": user.statuses_count,
                "favourites_count": user.favourites_count,
                "created_at": user.created_at,
                "verified": user.verified,
                "statuses_count": user.statuses_count,
                # "profile_image_url": user.profile_image_url,
                # "profile_banner_url": getattr(user, "profile_banner_url", None),
                "protected": user.protected,
            }
        return user_info

    async def post_tweet(self, content):
        """
        Post a tweet with the given content.

        :param content: The text content of the tweet.
        """
        try:
            await self.client.create_tweet(text=content)
            logging.info(f"Tweet posted: {content}")
            print("Tweet posted successfully.")
        except Exception as e:
            logging.error(f"Error posting tweet: {e}")
            print(f"Error posting tweet: {e}")

    async def like_tweet(self, tweet_id):
        """
        Like a tweet specified by tweet_id.

        :param tweet_id: The ID of the tweet to like.
        """
        try:
            await self.client.favorite_tweet(tweet_id)
            logging.info(f"Liked tweet ID: {tweet_id}")
            print(f"Liked tweet ID: {tweet_id}")
        except Exception as e:
            logging.error(f"Error liking tweet ID {tweet_id}: {e}")
            print(f"Error liking tweet ID {tweet_id}: {e}")

    async def retweet(self, tweet_id):
        """
        Retweet a tweet specified by tweet_id.

        :param tweet_id: The ID of the tweet to retweet.
        """
        try:
            await self.client.retweet(tweet_id)
            logging.info(f"Retweeted tweet ID: {tweet_id}")
            print(f"Retweeted tweet ID: {tweet_id}")
        except Exception as e:
            logging.error(f"Error retweeting tweet ID {tweet_id}: {e}")
            print(f"Error retweeting tweet ID {tweet_id}: {e}")

    async def search_tweets(self, query, count=10):
        """
        Search for tweets matching a query.

        :param query: The search query string.
        :param count: The number of tweets to retrieve.
        :return: A list of tweet objects.
        """
        try:
            tweets = await self.client.search_tweet(query=query, product='Top', count=count)
            logging.info(f"Searched for tweets with query: {query}")
            return tweets
        except Exception as e:
            logging.error(f"Error searching tweets with query '{query}': {e}")
            print(f"Error searching tweets: {e}")
            return []

    async def get_user_timeline(self, username=None, id=None, count=10):
        """
        Get recent tweets from a user's timeline.

        :param username: The Twitter handle of the user.
        :param count: The number of tweets to retrieve.
        :return: A list of tweet objects.
        """
        try:
            if (id is None):
                if (username is None):
                    print("Provide username or id.")
                    return
                else:
                    id = str((await self.get_user_info())["id"])

            tweets = await self.client.get_user_tweets(id, count=count)
            logging.info(f"Retrieved timeline for user: {username if username else id}")
            return tweets
        except Exception as e:
            logging.error(f"Error retrieving timeline for user '{username if username else id}': {e}")
            print(f"Error retrieving user timeline: {e}")
            return []

    async def get_following(self, username=None, id=None, count=20):
        """
        Get a list of accounts the user is following.

        :param username: The Twitter handle of the user (default is authenticated user).
        :param count: The maximum number of accounts to retrieve.
        :return: A list of user objects.
        """
        try:
            if (id is None):
                if (username is None):
                    print("Provide username or id.")
                    return
                else:
                    id = str((await self.get_user_info())["id"])

            following = await self.client.get_user_following(id, count)
            logging.info(f"Retrieved following list for user: {username if username else id}")
            return following
        except Exception as e:
            logging.error(f"Error retrieving following list for user '{username if username else id}': {e}")
            print(f"Error retrieving following list: {e}")
            return []

    async def follow(self, username=None, id=None) -> None:
        """
        Follow the user specified in parameter.

        :param username: The Twitter handle of the user.
        :return: None
        """
        try:
            if (id is None):
                if (username is None):
                    print("Provide username or id.")
                    return
                else:
                    id = str((await self.get_user_info())["id"])
                    
            await self.client.follow_user(id)
            logging.info(f"Successfully followed '{username if username else id}'")
            print(f"Followed: {username if username else id}")
        except Exception as e:
            print(f"Error following {username if username else id}: {e}")
            logging.info(f"Error attempting to follow '{username if username else id}' : {e}")

    async def unfollow(self, username=None, id=None):
        """
        Unfollow the user specified in parameter.

        :param username: The Twitter handle of the user.
        :return: None
        """
        try:
            if (id is None):
                if (username is None):
                    print("Provide username or id.")
                    return
                else:
                    id = str((await self.get_user_info())["id"])

            await self.client.unfollow_user(id)
            logging.info(f"Successfully unfollowed '{username}'")
            print(f"Unfollowed: {username}")
        except Exception as e:
            logging.info(f"Error unfollwing '{username}': {e}")
            print(f"Error unfollowing {username}: {e}")
    
    async def get_user_info(self, username: str):
        """
        Récupère les informations détaillées d'un utilisateur.

        :param username: Nom d'utilisateur (Twitter handle, sans le @).
        :return: Un dictionnaire contenant les informations utilisateur, ou None en cas d'erreur.
        """

        try:
            user = await self.client.get_user_by_screen_name(screen_name=username)
            user_info = self._parse_user(user)
            logging.info(f"Fetched user info for: {username}")
            return user_info
        except Exception as e:
            logging.error(f"Error fetching user info for {username}: {e}")
            print(f"Error fetching user info for {username}: {e}")
            return None

    async def get_user_followers(self, username=None, id=None, count=20):
        """
        Récupère les followers d'un utilisateur.

        :param username: Nom d'utilisateur (Twitter handle, sans le @).
        :param count: Nombre maximum de followers à récupérer (limité par l'API).
        :return: Une liste de dictionnaires contenant les informations de chaque follower.
        """
        try:
            if (id is None):
                if (username is None):
                    print("Provide username or id.")
                    return
                else:
                    id = str((await self.get_user_info())["id"])

            followers = await self.client.get_user_followers(id)
            followers = [self._parse_user(u) for u in followers]
            logging.info(f"Fetched {len(followers)} followers for: {username if username else id}")
            return followers
        except Exception as e:
            logging.error(f"Error fetching followers for {username if username else id}: {e}")
            print(f"Error fetching followers for {username if username else id}: {e}")
            return []

###########################V2###############################()
    #     id = self.get_user_id_by_username(username=username)
    #     print(f"\n\nid = {id}\n\n")
    #     response = self.api.get_users_followers(id=id, max_results=count)
    #     print(response.data)
    #     followers = []
    #     for follower in response.data:
    #         followers.append({
    #             "id": follower.id,
    #             "screen_name": follower.screen_name,
    #             "name": follower.name,
    #             "followers_count": follower.followers_count,
    #             "friends_count": follower.friends_count,
    #             "statuses_count": follower.statuses_count,
    #             "verified": follower.verified,
    #             "protected": follower.protected,
    #         })
    #         logging.info(f"Fetched {len(followers)} followers for: {username}")
    #     return followers
    
    # def get_user_id_by_username(self, username):
    #     try:
    #         # Appel API pour récupérer l'utilisateur
    #         user = self.api.get_user(username=username)
    #         if user.data:
    #             print(f"Username: {user.data.username}, User ID: {user.data.id}")
    #             return user.data.id
    #         else:
    #             print(f"Utilisateur '{username}' introuvable.")
    #             return None
    #     except tweepy.TweepyException as e:
    #         print(f"Erreur lors de la récupération de l'utilisateur : {e}")
    #         return None