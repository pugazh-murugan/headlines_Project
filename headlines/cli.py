"""Command-line entry point."""

import argparse
import sys

import requests

from headlines.config import LIMIT, URL
from headlines.scraper import extract_headlines, fetch_page


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="headlines", description="Print the top headlines from BBC News."
    )
    parser.add_argument(
        "-n", "--limit", type=int, default=LIMIT, help=f"number of headlines (default: {LIMIT})"
    )
    parser.add_argument("--url", default=URL, help=f"page to scrape (default: {URL})")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    try:
        html = fetch_page(args.url)
    except requests.RequestException as e:
        print(f"Failed to fetch page: {e}", file=sys.stderr)
        return 1

    headlines = extract_headlines(html, args.limit)

    if not headlines:
        print("No headlines found. The selector may need updating.", file=sys.stderr)
        return 1

    if len(headlines) < args.limit:
        print(f"Only {len(headlines)} headlines found.", file=sys.stderr)

    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline}")
    return 0
