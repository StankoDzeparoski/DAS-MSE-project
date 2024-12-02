import requests
from bs4 import BeautifulSoup
import sqlite3

def getTickers():
    # Send a GET request to the webpage
    response = requests.get("https://www.mse.mk/en/stats/symbolhistory/KMB")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the select element
    select_tag = soup.find('select', {'id': 'Code'})

    # Extract all option tags within the select tag
    option_tags = select_tag.find_all('option')

    # Filter the tags to exclude non-letter codes or those longer than 5 characters
    ticker_codes = []
    for option in option_tags:
        tag = option.get_text(strip=True)  # Remove whitespace
        if tag.isalpha() and len(tag) <= 5:
            ticker_codes.append(tag)
    return ticker_codes


def save_tickers_to_db(tickers, db_name="mse_data.db"):
    # Connect to the database
    issuers = db_name
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issuers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker_code TEXT NOT NULL UNIQUE
        )
    """)

    for ticker in tickers:
        cursor.execute("INSERT OR IGNORE INTO issuers (ticker_code) VALUES (?)", (ticker,))

    connection.commit()
    connection.close()
    print(f"Inserted {len(tickers)} tickers into the database.")