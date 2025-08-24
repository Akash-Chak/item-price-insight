from flask import Blueprint, render_template, current_app
import os
from utils.data_loader import load_latest_data

home_bp = Blueprint('home', __name__, template_folder='../templates')

# Use record_once instead of before_app_first_request
@home_bp.record_once
def load_data(setup_state):
    app = setup_state.app
    app.config['LATEST_ITEMS'] = load_latest_data()


@home_bp.route('/home')
@home_bp.route('/')
def home():
    # Fetch items from cache
    items = current_app.config.get('LATEST_ITEMS', [])

    results = []
    for item in items:
        item_id = item.get('id')
        item_name = item.get('title')
        image_url = item.get('image_url')
        e_price = item.get('price')

        results.append({
            'id': item_id,
            'name': item_name,
            'image_url': image_url,
            'ecommerce_price': e_price
        })

    return render_template('home.html', results=results)
