from .base_fetcher import BaseFetcher
import time
import random


class OfficialFetcher(BaseFetcher):
    def __init__(self):
        pass

    def fetch_price(self, item: dict) -> float:
        # simulate an official price lookup
        time.sleep(0.02)
        seed = item.get('official_seed', None)
        if seed is None:
            # if there is no official seed, fallback to seed_price
            seed = item.get('seed_price', 100.0)
        noise = random.uniform(-0.05, 0.05)
        return round(seed * (1 + noise), 2)

    def parse_response(self, response_text: str) -> float:
        raise NotImplementedError('parse_response should be implemented for real fetches')