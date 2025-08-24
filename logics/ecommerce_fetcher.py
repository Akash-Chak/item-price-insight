# NOTE: This file contains a stubbed fetcher. Replace the stubbed logic with real
# requests + HTML parsing or API calls.

from .base_fetcher import BaseFetcher
import random
import time


class EcommerceFetcher(BaseFetcher):
    def __init__(self, user_agent: str = ''):
        self.user_agent = user_agent

    def fetch_price(self, item: dict) -> float:
        """Stubbed fetch — in a real implementation, use requests to fetch product page or API."""
        # simulate network latency
        time.sleep(0.05)
        # return random price around provided seed or a mocked value
        seed = item.get('seed_price', 100.0)
        noise = random.uniform(-0.1, 0.15)  # -10% to +15%
        return round(seed * (1 + noise), 2)

    def parse_response(self, response_text: str) -> float:
        # parse HTML or JSON to extract price
        raise NotImplementedError('parse_response should be implemented for real fetches')