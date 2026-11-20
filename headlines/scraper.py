"""Fetching and parsing logic. Raises exceptions instead of exiting."""

import requests
from bs4 import BeautifulSoup

from headlines.config import HEADERS, LIMIT, TIMEOUT, URL


def fetch_page(url=URL):
    """Return the HTML of ``url``.

    Raises ``requests.RequestException`` on network errors or non-2xx responses.
    """
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return response.text


def extract_headlines(html, limit=LIMIT):
    """Return up to ``limit`` unique, non-empty headlines found in ``html``."""
    soup = BeautifulSoup(html, "html.parser")

    # Try the specific selector first, fall back to all <h2> tags
    items = soup.select('h2[data-testid="card-headline"]') or soup.find_all("h2")

    headlines = []
    seen = set()
    for item in items:
        text = item.get_text(strip=True)
        if text and text not in seen:  # skip empty and duplicate entries
            seen.add(text)
            headlines.append(text)
        if len(headlines) == limit:
            break
    return headlines
