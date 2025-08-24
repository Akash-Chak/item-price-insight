"""
Very simple analyzer for Phase 1. It expects `history` as a list of dicts
with keys `date` and `price` (float). Current is a dict with keys 'ecommerce' and 'official'.

Decision logic (simple heuristics):
- If current ecommerce price < historical mean - x% => BUY NOW
- If current ecommerce price > historical mean + y% => WAIT (price likely higher)
- If trending down (last k points decreasing) => WAIT
- Otherwise => HOLD (or BUY if small discount)

This is intentionally simple for phase 1; can be replaced with ARIMA or ML models later.
"""
from datetime import datetime
from statistics import mean
from dateutil.parser import parse as parse_date


class PriceAnalyzer:
    def __init__(self, buy_threshold_pct: float = 0.08, sell_threshold_pct: float = 0.12):
        # thresholds are fractions (e.g., 0.08 = 8%)
        self.buy_threshold = buy_threshold_pct
        self.sell_threshold = sell_threshold_pct

    def load_history(self, item: dict):
        """Stub: load historical prices for an item. For now, return mocked history.
        Replace with actual historical load from price_cache.json or external API."""
        # mocked: last 12 months monthly points
        import random
        base = item.get('seed_price', 100)
        hist = []
        for i in range(12, 0, -1):
            # create older dates
            price = round(base * (1 + random.uniform(-0.12, 0.18)), 2)
            date = datetime.now().replace(day=1).isoformat()
            hist.append({'date': date, 'price': price})
        return hist

    def decide(self, history: list, current: dict):
        # compute simple stats
        prices = [h['price'] for h in history if 'price' in h]
        if not prices:
            return 'NO_DATA', 'No historical data available.'

        avg = mean(prices)
        cur_price = current.get('ecommerce')
        if cur_price is None:
            return 'NO_CURRENT', 'No current ecommerce price.'

        diff_pct = (avg - cur_price) / avg

        # detect simple downtrend: last 3 decreasing
        downtrend = False
        if len(prices) >= 3:
            downtrend = prices[-1] < prices[-2] < prices[-3]

        reasoning = f"historical_avg={avg:.2f}, current={cur_price:.2f}, diff_pct={diff_pct:.3f}"

        if diff_pct >= self.buy_threshold:
            return 'BUY_NOW', reasoning + ' (significant discount)'
        if diff_pct <= -self.sell_threshold:
            return 'WAIT', reasoning + ' (price higher than usual)'
        if downtrend:
            return 'WAIT', reasoning + ' (recent downtrend)'

        return 'HOLD', reasoning + ' (no strong signal)'