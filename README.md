# Headlines

A small Python command-line tool that scrapes the [BBC News](https://www.bbc.com/news) front page and prints the top headlines.

```
$ python -m headlines
1. <headline one>
2. <headline two>
...
```

## Project structure

```
headlines_Project/
├── headlines/            # application package
│   ├── __init__.py
│   ├── __main__.py       # enables `python -m headlines`
│   ├── cli.py            # argument parsing and output
│   ├── config.py         # URL, headers, default limit, timeout
│   └── scraper.py        # fetch_page() and extract_headlines()
├── main.py               # shortcut: `python main.py`
├── tests/
│   └── test_scraper.py   # offline unit tests (no network needed)
├── requirements.txt      # runtime dependencies
├── requirements-dev.txt  # runtime + test dependencies
├── README.md
└── .gitignore
```

## Requirements

- Python 3.9 or newer
- Packages listed in [requirements.txt](requirements.txt): `requests`, `beautifulsoup4`

## Setup

```powershell
# create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1        # macOS/Linux: source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py                   # same as `python -m headlines`
python -m headlines              # top 5 headlines (default)
python -m headlines -n 10        # top 10 headlines
python -m headlines --url https://www.bbc.com/news/world
python -m headlines --help
```

Run these from the project root. Don't run files inside `headlines/` directly (e.g. `python headlines/cli.py`), because the package import will fail.

Exit code is `0` on success and `1` if the page can't be fetched or no headlines are found.

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

The tests use sample HTML and mocked requests, so they run offline.

## How it works

1. `fetch_page()` downloads the page (10 s timeout) and raises on network or HTTP errors.
2. `extract_headlines()` parses the HTML with BeautifulSoup. It looks for `h2[data-testid="card-headline"]` first and falls back to every `<h2>`. Empty and duplicate headlines are skipped.
3. `cli.main()` prints the numbered results.

## Troubleshooting

- **"No headlines found. The selector may need updating."** BBC changed its page markup. Update the selector in `headlines/scraper.py`.
- **Network or HTTP errors.** Check your connection. The site may also be blocking automated requests.

## Notes

Check BBC's terms of use before scraping at scale. This tool makes one request per run.
