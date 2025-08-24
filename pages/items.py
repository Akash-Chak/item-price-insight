from flask import Blueprint, render_template, request, jsonify
import json
import os
from datetime import datetime
from logics.scraper import scrape_items  # import scraper function

items_bp = Blueprint('items', __name__, template_folder='../templates')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ITEMS_FILE = os.path.join(DATA_DIR, 'items.json')
SNAPSHOT_DIR = os.path.join(DATA_DIR, 'snapshots')


def get_latest_snapshot_path():
    """Find latest snapshot file path if exists."""
    if not os.path.exists(SNAPSHOT_DIR):
        return None
    files = [f for f in os.listdir(SNAPSHOT_DIR) if f.startswith("scraped_")]
    if not files:
        return None
    latest_file = max(files)  # because filenames have YYYY-MM-DD
    return os.path.join(SNAPSHOT_DIR, latest_file)


@items_bp.route('/items')
def items_page():
    if not os.path.exists(ITEMS_FILE):
        items = []
    else:
        with open(ITEMS_FILE, 'r') as f:
            items = json.load(f)
    return render_template('items.html', items=items)


@items_bp.route('/update_items', methods=['POST'])
def update_items():
    try:
        data = request.get_json()
        with open(ITEMS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@items_bp.route('/check_snapshot', methods=['GET'])
def check_snapshot():
    """Check if snapshot for today already exists."""
    today = datetime.now().strftime("%Y-%m-%d")
    latest_path = get_latest_snapshot_path()

    if latest_path and today in latest_path:
        return jsonify({"exists": True, "file": latest_path})
    return jsonify({"exists": False})


@items_bp.route('/run_scraper', methods=['POST'])
def run_scraper():
    """Run scraper and return result."""
    try:
        results, outfile = scrape_items(return_path=True)
        return jsonify({
            "status": "success",
            "message": f"Scraped {len(results)} items.",
            "file": outfile
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
