import csv
import os
from bs4 import BeautifulSoup

print("Reading web_data.html file...")

# Read the HTML file
with open("../data/raw_data/web_data.html", 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

print("Filtering fields...")

# Extract market data
market_data = []
market_cards = soup.find_all('a', class_=['MarketCard-container', 'MarketCard-down', 'MarketCard-up'])

for card in market_cards:
    symbol_elem = card.find('span', class_='MarketCard-symbol')
    position_elem = card.find('span', class_='MarketCard-stockPosition')
    change_pct_elem = card.find('span', class_='MarketCard-changesPct')
    
    if symbol_elem and position_elem:
        symbol = symbol_elem.get_text(strip=True)
        position_text = position_elem.get_text(strip=True)
        # Convert to numeric by removing commas
        try:
            position = float(position_text.replace(',', ''))
        except ValueError:
            position = position_text  # Keep as string if conversion fails
        change_pct = change_pct_elem.get_text(strip=True) if change_pct_elem else "N/A"
        
        market_data.append({
            'marketCard_symbol': symbol,
            'marketCard_stockPosition': position,
            'marketCard_changePct': change_pct
        })

# Extract news data
news_data = []
news_list = soup.find('ul', class_='LatestNews-list')

if news_list:
    news_items = news_list.find_all('li', class_='LatestNews-item')
    for item in news_items:
        timestamp_elem = item.find('time', class_='LatestNews-timestamp')
        headline_elem = item.find('a', class_='LatestNews-headline')
        
        if headline_elem:
            timestamp = timestamp_elem.get_text(strip=True) if timestamp_elem else "N/A"
            title = headline_elem.get_text(strip=True)
            link = headline_elem.get('href', '')
            
            news_data.append({
                'LatestNews_timestamp': timestamp,
                'title': title,
                'link': link
            })

print("Storing Market data...")

# Create processed_data directory
os.makedirs("../data/processed_data", exist_ok=True)

# Save market data to CSV
with open("../data/processed_data/market_data.csv", 'w', newline='', encoding='utf-8') as f:
    if market_data:
        writer = csv.DictWriter(f, fieldnames=['marketCard_symbol', 'marketCard_stockPosition', 'marketCard_changePct'])
        writer.writeheader()
        writer.writerows(market_data)

print("Market data CSV created")

print("Storing News data...")

# Save news data to CSV
with open("../data/processed_data/news_data.csv", 'w', newline='', encoding='utf-8') as f:
    if news_data:
        writer = csv.DictWriter(f, fieldnames=['LatestNews_timestamp', 'title', 'link'])
        writer.writeheader()
        writer.writerows(news_data)

print("News data CSV created")
print(f"Processed {len(market_data)} market entries and {len(news_data)} news entries")