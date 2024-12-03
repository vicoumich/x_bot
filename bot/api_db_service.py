from .api_client import TwitterAPI
from .db_manager import UserDatabaseManager, TweetDatabaseManager

class ApiDbService:
    """
    Service pour coordonner les appels API et la sauvegarde automatique dans la base de données.
    """

    def __init__(self, api_client: TwitterAPI, 
                 user_db: UserDatabaseManager, #tweet_db: TweetDatabaseManager
                 ):
        """
        Initialise le service avec les clients API et base de données.
        """
        self.api = api_client
        self.user_db = user_db
        # Pas encore ( à créer à la main )
        # self.tweet_db = tweet_db

    def fetch_and_save_user_info(self, username):
        """
        Récupère les informations utilisateur et les enregistre dans la base de données.
        """
        user_info = self.api.get_user_info(username)
        if user_info:
            self.user_db.add_user(user_info)
            return user_info
        return None

    def fetch_and_save_followers(self, username, count=100):
        """
        Récupère les followers d'un utilisateur et les enregistre dans la base de données.
        """
        followers = self.api.get_user_followers(username, count)
        for follower in followers:
            self.user_db.add_user(follower)  # Enregistrer chaque follower
        return followers

    #### METTRE A JOUR db_manager ####
    # def fetch_and_save_tweets(self, username, count=10):
    #     """
    #     Récupère les tweets récents d'un utilisateur et les enregistre dans la base de données.
    #     """
    #     tweets = self.api.get_user_timeline(username, count)
    #     for tweet in tweets:
    #         self.tweet_db.add_tweet(tweet)
    #     return tweets
