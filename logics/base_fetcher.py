from abc import ABC, abstractmethod


class BaseFetcher(ABC):
    """Abstract fetcher class. Concrete fetchers implement fetch_price and parse_response."""

    @abstractmethod
    def fetch_price(self, item: dict) -> float:
        """Fetch current price for an item. Return float or None."""
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, response_text: str) -> float:
        """Parse raw response and return price as float."""
        raise NotImplementedError