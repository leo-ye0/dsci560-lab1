import os
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://www.cnbc.com/world/?region=world"
TABS = ["ASIA", "US", "EUR", "PRE-MKT", "BONDS", "FX", "CRYPTO", "GOLD", "OIL"]

all_market_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(BASE_URL, timeout=60000)
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_timeout(3000)
    
    for tab in TABS:
        try:
            # Click the market banner tab specifically
            tab_button = page.locator(f'.MarketsBannerMenu-marketOption:has-text("{tab}")')
            if tab_button.count() > 0:
                tab_button.first.click()
                page.wait_for_timeout(1000)
                
                # Get market data after tab click
                page_content = page.content()
                soup = BeautifulSoup(page_content, 'html.parser')
                market_banner = soup.find("div", class_="MarketsBanner-marketData")
                
                if market_banner:
                    all_market_data.append(market_banner.prettify())
        except Exception:
            pass
    
    browser.close()

# Get news with requests + BeautifulSoup (static content)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(BASE_URL, headers=headers)
static_soup = BeautifulSoup(response.content, 'html.parser')
latest_news = static_soup.find("ul", class_="LatestNews-list")

# Save raw HTML
os.makedirs("../data/raw_data", exist_ok=True)
with open("../data/raw_data/web_data.html", 'w', encoding='utf-8') as f:
    for data in all_market_data:
        f.write(data)
        f.write("\n\n")
    if latest_news:
        f.write(latest_news.prettify())

print("Data saved to ../data/raw_data/web_data.html")

# Print first 10 lines of the HTML file
with open("../data/raw_data/web_data.html", 'r', encoding='utf-8') as f:
    for i in range(10):
        line = f.readline()
        if line:
            print(line.rstrip())
        else:
            break