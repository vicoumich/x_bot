from surfacic_behavior import Stage1Manager
from api_db_service import ApiDbService
from db_manager import UserDatabaseManager
from api_client import TwitterAPI
from behavior_simulator import BehaviorSimulator
import asyncio

async def main():
    user_db = UserDatabaseManager()
    await user_db.init()
    api = TwitterAPI()
    await api.init()
    service = ApiDbService(api_client=api, user_db=user_db)
    comportement_basique = Stage1Manager(api_db_service=service)
    accounts_list = ["HAL_9000_Bundy", "LeoTechMaker", "DarkChris91", "TheOnlyLeukos", "Redeset2"]

    # await BehaviorSimulator.random_delay(5, 10)
    for account in accounts_list:
        print(f"\nrécupération et sauvegarde des aboonés de {account}")
        await comportement_basique.follow_and_save_followers(account)

async def test():
    user_db = UserDatabaseManager()
    await user_db.init()
    api = TwitterAPI()
    await api.init()
    service = ApiDbService(api_client=api, user_db=user_db)
    info=await api.get_user_info(username="HAL_9000_Bundy")
    print(info)
    

if __name__ =="__main__":
    # target_username = input("Entre l'utilisateur >>")
    asyncio.run(main())