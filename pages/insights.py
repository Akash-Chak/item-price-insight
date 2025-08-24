from flask import Blueprint, render_template
import json
import os
from logics.price_analyzer import PriceAnalyzer
from logics.ecommerce_fetcher import EcommerceFetcher
from logics.official_fetcher import OfficialFetcher

insights_bp = Blueprint('insights', __name__, template_folder='../templates')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ITEMS_FILE = os.path.join(DATA_DIR, 'items.json')


@insights_bp.route('/insights')
def insights():
    print(DATA_DIR, ITEMS_FILE)
    with open(ITEMS_FILE, 'r') as f:
        items = json.load(f)

    ecommerce = EcommerceFetcher()
    official = OfficialFetcher()
    analyzer = PriceAnalyzer()

    insights = []

    for item in items:
        hist = analyzer.load_history(item)
        current = {
            'ecommerce': ecommerce.fetch_price(item),
            'official': official.fetch_price(item),
        }
        decision, reasoning = analyzer.decide(hist, current)

        insights.append({
            'id': item.get('id'),
            'title': item.get('title'),
            'current': current,
            'decision': decision,
            'reasoning': reasoning,
        })

    return render_template('insights.html', insights=insights)