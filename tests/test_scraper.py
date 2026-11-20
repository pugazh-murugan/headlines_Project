from unittest.mock import Mock, patch

import pytest
import requests

from headlines import cli
from headlines.scraper import extract_headlines, fetch_page

SPECIFIC_HTML = """
<h2 data-testid="card-headline">First</h2>
<h2 data-testid="card-headline">Second</h2>
<h2 data-testid="card-headline">First</h2>
<h2 data-testid="card-headline">   </h2>
<h2>Not selected</h2>
"""

FALLBACK_HTML = "<h2>Alpha</h2><h2>Beta</h2><h2>Gamma</h2>"


def test_extract_uses_specific_selector_and_skips_duplicates_and_empty():
    assert extract_headlines(SPECIFIC_HTML) == ["First", "Second"]


def test_extract_falls_back_to_all_h2():
    assert extract_headlines(FALLBACK_HTML) == ["Alpha", "Beta", "Gamma"]


def test_extract_respects_limit():
    assert extract_headlines(FALLBACK_HTML, limit=2) == ["Alpha", "Beta"]


def test_extract_returns_empty_list_when_nothing_found():
    assert extract_headlines("<p>nothing here</p>") == []


def test_fetch_page_returns_text():
    response = Mock(text="<html></html>")
    with patch("headlines.scraper.requests.get", return_value=response) as get:
        assert fetch_page("http://example.test") == "<html></html>"
    get.assert_called_once()


def test_fetch_page_raises_on_http_error():
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("503")
    with patch("headlines.scraper.requests.get", return_value=response):
        with pytest.raises(requests.HTTPError):
            fetch_page("http://example.test")


def test_cli_prints_numbered_headlines(capsys):
    with patch("headlines.cli.fetch_page", return_value=FALLBACK_HTML):
        assert cli.main(["-n", "2"]) == 0
    assert capsys.readouterr().out == "1. Alpha\n2. Beta\n"


def test_cli_returns_1_on_network_error():
    with patch("headlines.cli.fetch_page", side_effect=requests.ConnectionError("down")):
        assert cli.main([]) == 1


def test_cli_returns_1_when_no_headlines():
    with patch("headlines.cli.fetch_page", return_value="<p>empty</p>"):
        assert cli.main([]) == 1
