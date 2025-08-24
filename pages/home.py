from flask import Blueprint, render_template, current_app
from logics.ecommerce_fetcher import EcommerceFetcher
from logics.official_fetcher import OfficialFetcher
import json
import os

home_bp = Blueprint('home', __name__, template_folder='../templates')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ITEMS_FILE = os.path.join(DATA_DIR, 'items.json')


@home_bp.route('/')
def home():
    # load items from data/items.json
    with open(ITEMS_FILE, 'r') as f:
        items = json.load(f)

    # instantiate fetchers (stubs) and fetch current prices
    ecommerce = EcommerceFetcher()
    official = OfficialFetcher()

    results = []
    for item in items:
        item_id = item.get('id')
        item_name = item.get('name')
        e_price = ecommerce.fetch_price(item)
        o_price = official.fetch_price(item)
        results.append({
            'id': item_id,
            'name': item_name,
            'ecommerce_price': e_price,
            'official_price': o_price,
        })

    return render_template('home.html', results=results)