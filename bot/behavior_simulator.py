# bot/behavior_simulator.py

import time
import random
import logging

# Configure logging
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
)


class BehaviorSimulator:
    @staticmethod
    def random_delay(min_seconds=1, max_seconds=5):
        """
        Introduce a random delay to simulate human behavior.

        :param min_seconds: Minimum number of seconds to wait.
        :param max_seconds: Maximum number of seconds to wait.
        """
        delay = random.uniform(min_seconds, max_seconds)
        logging.info(f"Delaying for {delay:.2f} seconds to simulate human behavior.")
        time.sleep(delay)