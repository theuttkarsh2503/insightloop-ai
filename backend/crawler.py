# backend/crawler.py
# Fetch webpage HTML

import requests
from requests.exceptions import RequestException

def fetch_page(url: str) -> str:
    """
    Fetch the HTML content of a webpage.
    Returns HTML string or empty string if error.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        return f"Error fetching {url}: {e}"
