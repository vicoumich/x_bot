from .surfacic_behavior import Stage1Manager
from .api_db_service import ApiDbService
from .db_manager import UserDatabaseManager
from .api_client import TwitterAPI

if __name__ =="__main__":
    target_username = input("Entre l'utilisateur >>")
    comportement_basique = Stage1Manager(api_db_service=ApiDbService
                                            (
                                                api_client=TwitterAPI(),
                                                user_db=UserDatabaseManager()
                                            )
                                        )
    comportement_basique.follow_and_save_followers(target_username)