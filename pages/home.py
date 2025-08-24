from flask import Blueprint, render_template, current_app, redirect, url_for
import os
from utils.data_loader import load_latest_data

home_bp = Blueprint('home', __name__, template_folder='../templates')

@home_bp.record_once
def load_data(setup_state):
    app = setup_state.app
    app.config['LATEST_ITEMS'] = load_latest_data()

@home_bp.route('/home')
@home_bp.route('/')
def home():
    items = current_app.config.get('LATEST_ITEMS', [])
    results = []
    for item in items:
        results.append({
            'id': item.get('id'),
            'name': item.get('title'),
            'image_url': item.get('image_url'),
            'ecommerce_price': item.get('price'),
            'official_price': item.get('official_price'),
            'recommendation': item.get('recommendation')
        })
    return render_template('home.html', results=results)

# ✅ NEW ROUTE: Reload latest data
@home_bp.route('/reload')
def reload_data():
    current_app.config['LATEST_ITEMS'] = load_latest_data()
    return redirect(url_for('home.home'))
