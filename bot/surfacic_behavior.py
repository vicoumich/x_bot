from api_db_service import ApiDbService
from behavior_simulator import BehaviorSimulator
class Stage1Manager:
    def __init__(self, api_db_service: ApiDbService):
        """
        Initialise le Stage 1 Manager avec le service API ↔ BDD.
        """
        self.service = api_db_service

    async def follow_and_save_followers(self, username, count=20):
        """
        Suivre les followers d'un utilisateur et enregistrer leurs informations.
        """
        followers = await self.service.fetch_and_save_followers(username, count)
        for follower in followers:
            await BehaviorSimulator.random_delay(5, 10)
            await self.service.api.follow(follower['screen_name'])  # Suivre
            print(f"Followed and saved: {follower['screen_name']}")
            await BehaviorSimulator.random_delay(180, 600)
    
