import os
import json
from datetime import datetime
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'snapshots')


def get_latest_snapshot_file() -> str:
    """
    Finds the latest scraped_*.json file from DATA_DIR.

    Returns:
        str: Path to the latest snapshot file.
    """
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    files = [f for f in os.listdir(DATA_DIR) if f.startswith("scraped_") and f.endswith(".json")]
    if not files:
        raise FileNotFoundError("No snapshot files found in data/snapshots.")

    # Extract date part and sort
    files.sort(key=lambda x: datetime.strptime(x.replace("scraped_", "").replace(".json", ""), "%Y-%m-%d"), reverse=True)
    latest_file = files[0]

    return os.path.join(DATA_DIR, latest_file)


def load_latest_data() -> List[Dict[str, Any]]:
    """
    Loads data from the latest snapshot file.

    Returns:
        list[dict]: List of items in the latest snapshot.
    """
    latest_file = get_latest_snapshot_file()
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
