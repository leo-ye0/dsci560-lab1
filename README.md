# CNBC Web Scraper

A Python web scraper that extracts market data and news from CNBC using Playwright and requests.

## Features

- **Market Data**: Scrapes 9 market sections (ASIA, US, EUR, PRE-MKT, BONDS, FX, CRYPTO, GOLD, OIL)
- **News Data**: Extracts latest news headlines with timestamps and links
- **Hybrid Approach**: Uses Playwright for dynamic content and requests for static content
- **CSV Output**: Processes data into structured CSV files for analysis

## Files

- `scripts/web_scraper.py` - Main scraper using Playwright + requests
- `scripts/data_filter.py` - Processes HTML into CSV format
- `requirements.txt` - Python dependencies
- `data/raw_data/web_data.html` - Raw scraped HTML
- `data/processed_data/market_data.csv` - Market data (45 entries)
- `data/processed_data/news_data.csv` - News data (30 entries)

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
# Scrape data
python scripts/web_scraper.py

# Process into CSV
python scripts/data_filter.py
```

## Data Structure

**Market Data**: Symbol, Stock Position (numeric), Change %  
**News Data**: Timestamp, Title, Link

## Technologies

- **Playwright**: Dynamic content scraping
- **Requests**: Static content fetching  
- **BeautifulSoup**: HTML parsing
- **CSV**: Data output format