"""Headlines: a small scraper that prints the top BBC News headlines."""

from headlines.scraper import extract_headlines, fetch_page

__all__ = ["extract_headlines", "fetch_page"]
__version__ = "0.1.0"
