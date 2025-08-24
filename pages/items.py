from flask import Blueprint, render_template, request, jsonify
import json
import os

items_bp = Blueprint('items', __name__, template_folder='../templates')

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ITEMS_FILE = os.path.join(DATA_DIR, 'items.json')


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
