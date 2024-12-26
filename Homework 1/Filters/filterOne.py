import requests
from bs4 import BeautifulSoup
import sqlite3
import logging

# Constants
BASE_URL = "http://www.mse.mk/mk/symbol/"
DB_NAME = "mse_data.db"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def getTickers():
    """
    Fetch ticker codes from the MSE website.
    Returns a list of ticker codes.
    """

    response = requests.get("https://www.mse.mk/en/stats/symbolhistory/KMB")
    soup = BeautifulSoup(response.content, 'html.parser')

    select_tag = soup.find('select', {'id': 'Code'})

    option_tags = select_tag.find_all('option')

    ticker_codes = []
    for option in option_tags:
        tag = option.get_text(strip=True)  # Remove whitespace
        if tag.isalpha() and len(tag) <= 5:
            ticker_codes.append(tag)
    return ticker_codes


def get_company_name(ticker_name):
    """
    Fetch the company name for a given ticker from the MSE website.
    Returns the company name or None if not found.
    """
    url = f"{BASE_URL}{ticker_name}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        company_name_tag = soup.select_one("#izdavach .col-md-8.title")
        if company_name_tag:
            return company_name_tag.text.strip()

        alternative_name_tag = soup.select_one("#titleKonf2011.panel-heading")
        if alternative_name_tag:
            text = alternative_name_tag.text.strip()
            if " - " in text:
                return text.split(" - ", maxsplit=2)[-1]

        logging.warning(f"Company name not found for ticker: {ticker_name}")
        return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching company name for {ticker_name}: {e}")
        return None


def save_tickers_to_db(tickers, db_name="mse_data.db"):
    """
    Save ticker codes and their corresponding company names to the database.
    """

    issuers = db_name;
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create the issuers table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS issuers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker_code TEXT NOT NULL UNIQUE,
            company_name TEXT
        )
        """
    )

    # Insert ticker and company name
    for ticker in tickers:
        company_name = get_company_name(ticker)
        cursor.execute(
            "INSERT OR IGNORE INTO issuers (ticker_code, company_name) VALUES (?, ?)",
            (ticker, company_name)
        )

    connection.commit()
    connection.close()
    print(f"Inserted {len(tickers)} tickers into the database.")
