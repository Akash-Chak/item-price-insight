from flask import Blueprint, render_template, current_app
from logics.ecommerce_fetcher import EcommerceFetcher
from logics.official_fetcher import OfficialFetcher
import json
import os

home_bp = Blueprint('home', __name__, template_folder='../templates')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ITEMS_FILE = os.path.join(DATA_DIR, 'items.json')


@home_bp.route('/home')
@home_bp.route('/')
def home():
    # load items from data/items.json
    if not os.path.exists(ITEMS_FILE):
        items = []
    else:
        with open(ITEMS_FILE, 'r') as f:
            items = json.load(f)

    # instantiate fetchers (stubs) and fetch current prices
    ecommerce = EcommerceFetcher()
    official = OfficialFetcher()

    results = []
    for item in items:
        item_id = item.get('id')
        item_name = item.get('title') or item.get('name')
        image_url = item.get('image', "")
        e_price = ecommerce.fetch_price(item)
        o_price = official.fetch_price(item)

        recommendation = None
        if e_price and o_price:
            recommendation = "Buy Online" if e_price < o_price else "Buy Official"

        results.append({
            'id': item_id,
            'name': item_name,
            'image_url': image_url,
            'ecommerce_price': e_price,
            'official_price': o_price,
            'recommendation': recommendation
        })

    return render_template('home.html', results=results)
