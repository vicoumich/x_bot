from api_client import TwitterAPI
from db_manager import UserDatabaseManager, TweetDatabaseManager
from behavior_simulator import BehaviorSimulator
class ApiDbService:
    """
    Service pour coordonner les appels API et la sauvegarde automatique dans la base de données.
    """

    def __init__(self, api_client: TwitterAPI, 
                 user_db: UserDatabaseManager#, tweet_db: TweetDatabaseManager
                 ):
        """
        Initialise le service avec les clients API et base de données.
        """
        self.api = api_client
        self.user_db = user_db
        # Pas encore ( à créer à la main )
        # self.tweet_db = tweet_db

    async def fetch_and_save_user_info(self, username):
        """
        Récupère les informations utilisateur et les enregistre dans la base de données.
        """
        ## AJOUTE DES APPELS A ASYNCIO.CREATE_TASK POUR PARALLELISER ##
        db_result = await self.user_db.get_user_by_username(username)
        if db_result != []:
            print("user already saved")
            return db_result[0]
        
        user_info = await self.api.get_user_info(username)
        if user_info:
            await self.user_db.add_user(user_info)
            return user_info
        return None

    async def fetch_and_save_followers(self, username, count=20):
        """
        Récupère les followers d'un utilisateur et les enregistre dans la base de données.
        """
        db_result = await self.user_db.get_user_by_username(username)
        if db_result != []:
            id = db_result[0]["id"]
            followers = await self.api.get_user_followers(id=id, count=count)
        else:
            infos = await self.api.get_user_info(username=username)
            await self.user_db.add_user(infos)
            id = infos["id"]
            followers = await self.api.get_user_followers(id=id, count=count)

        for follower in followers:
            await self.user_db.add_user(follower)  # Enregistrer chaque follower
        return followers[1:]

    async def scroll_home(self, scrolls=3) -> list:
        scrolled_tweets = []
        cursor, tweets = await self.api.get_timeline()
        scrolled_tweets.append(tweets)
        for _ in range(scrolls - 1):
            await BehaviorSimulator.random_delay(8, 25)
            scrolled_tweets.append(await cursor.next())
        return scrolled_tweets
    
    
    #### METTRE A JOUR db_manager ####
    # def fetch_and_save_tweets(self, username, count=10):
    #     """
    #     Récupère les tweets récents d'un utilisateur et les enregistre dans la base de données.
    #     """
    #     tweets = self.api.get_user_timeline(username, count)
    #     for tweet in tweets:
    #         self.tweet_db.add_tweet(tweet)
    #     return tweets
