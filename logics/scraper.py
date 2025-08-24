import re
import os
import json
import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from typing import Dict, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ITEMS_FILE = os.path.join(DATA_DIR, 'items.json')
SNAPSHOT_DIR = os.path.join(DATA_DIR, 'snapshots')

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def fetch_product_page(url: str) -> str:
    """Fetch HTML content of the ecommerce page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def parse_product_page(html: str) -> Dict[str, Optional[str]]:
    """
    Extract image, description, price, and model name from Flipkart product HTML.
    Returns clean str or None (avoids _AttributeValue issues).
    """

    soup = BeautifulSoup(html, "html.parser")

    # --- Image ---
    image_url: Optional[str] = None
    image_tag = soup.find("img")
    if isinstance(image_tag, Tag):
        src_val = image_tag.get("src")
        image_url = str(src_val) if isinstance(src_val, str) else None

    # Fallback: OpenGraph image
    if not image_url:
        og_img = soup.find("meta", property="og:image")
        if isinstance(og_img, Tag):
            content = og_img.get("content")
            image_url = str(content) if isinstance(content, str) else None

    # --- Price ---
    price: Optional[str] = None
    price_tag = soup.find("div", class_=re.compile(r"Nx9bqj"))
    if isinstance(price_tag, Tag):
        price = price_tag.get_text(strip=True)

    # Fallback: OpenGraph description with regex
    if not price:
        og_desc = soup.find("meta", property="og:description")
        if isinstance(og_desc, Tag):
            content = og_desc.get("content")
            text = str(content) if isinstance(content, str) else None
            if text:
                match = re.search(r"₹[\d,]+", text)
                if match:
                    price = match.group(0)

    # --- Description (Highlights list) ---
    description: Optional[str] = None
    desc_tags = soup.select("ul.G4BRas li")
    if desc_tags:
        description = " | ".join(
            li.get_text(strip=True) for li in desc_tags if isinstance(li, Tag)
        )

    # Fallback: OpenGraph description
    if not description:
        og_desc = soup.find("meta", property="og:description")
        if isinstance(og_desc, Tag):
            content = og_desc.get("content")
            description = str(content) if isinstance(content, str) else None

    # --- Model / Item Name ---
    model_name: Optional[str] = None
    title_tag = soup.find("span", class_=re.compile(r"VU-ZEz"))
    if isinstance(title_tag, Tag):
        model_name = title_tag.get_text(strip=True)

    # Fallback: <meta property="og:title">
    if not model_name:
        og_title = soup.find("meta", property="og:title")
        if isinstance(og_title, Tag):
            content = og_title.get("content")
            model_name = str(content) if isinstance(content, str) else None

    return {
        "image_url": image_url,
        "description": description,
        "price": price,
        "model_name": model_name,
    }

def scrape_items():
    """Scrape ecommerce data for each item and save a dated snapshot."""
    with open(ITEMS_FILE, "r") as f:
        items = json.load(f)

    results = []
    for item in items:
        link = item.get("ecommerce_link")
        if not link:
            continue

        try:
            html = fetch_product_page(link)
            parsed = parse_product_page(html)

            enriched = {
                "id": item.get("id"),
                "title": parsed.get("model_name"),
                "ecommerce_link": link,
                "image_url": parsed.get("image_url"),
                "description": parsed.get("description"),
                "price": parsed.get("price"),
                "scraped_at": datetime.now().isoformat(),
            }
            results.append(enriched)

        except Exception as e:
            print(f"❌ Failed to scrape {link}: {e}")

    # Save snapshot
    date_str = datetime.now().strftime("%Y-%m-%d")
    outfile = os.path.join(SNAPSHOT_DIR, f"scraped_{date_str}.json")
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(results)} items to {outfile}")


if __name__ == "__main__":
    scrape_items()
