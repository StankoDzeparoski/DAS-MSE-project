import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import os
import threading

# Lock for database access
data_lock = threading.Lock()

# Function to fetch missing data for a single ticker
def fetch_missing_data(ticker_code, start_date=None):
    url = f"https://www.mse.mk/mk/stats/symbolhistory/{ticker_code}"
    data = []
    to_date = datetime.now()

    if not start_date:
        for _ in range(10):  # Fetch data for the last 10 years
            start_date = to_date - timedelta(days=366 if to_date.year % 4 == 0 else 365)
            start_date_str = start_date.strftime('%Y-%m-%d')
            to_date_str = to_date.strftime('%Y-%m-%d')

            params = {'fromDate': start_date_str, 'toDate': to_date_str}

            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    table = soup.find('table')

                    if table is None:
                        continue

                    for row in table.find_all('tr')[1:]:  # Skip the header row
                        cells = row.find_all('td')
                        if len(cells) >= 7:  # Ensure row has enough columns
                            data.append({
                                'ticker_code': ticker_code,
                                'date': cells[0].text.strip(),
                                'lastPrice': float(cells[1].text.strip().replace(",", "") or 0),
                                'maxPrice': float(cells[2].text.strip().replace(",", "") or 0),
                                'minPrice': float(cells[3].text.strip().replace(",", "") or 0),
                                'volume': float(cells[6].text.strip().replace(",", "") or 0),

                            })

                    to_date = start_date  # Update to_date for the next iteration
                else:
                    print(f"Failed to fetch data for {ticker_code}, status: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error fetching data for {ticker_code}: {e}")
        return data
    return data


# Function to save data to the database
def save_data_to_db(data, db_name="mse_data.db"):
    with data_lock:
        connection = sqlite3.connect("mse_data.db")
        cursor = connection.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "mse_data.db" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker_code TEXT NOT NULL,
                date TEXT NOT NULL,
                lastPrice REAL,
                maxPrice REAL,
                minPrice REAL,
                volume REAL,
                UNIQUE (ticker_code, date) ON CONFLICT REPLACE
            )
        """)

        # Insert data
        for row in data:
            cursor.execute("""
                INSERT INTO "mse_data.db" (ticker_code, date, lastPrice, maxPrice, minPrice, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['ticker_code'], row['date'], row['lastPrice'], row['maxPrice'], row['minPrice'], row['volume']))

        connection.commit()
        connection.close()


# Function to process a single ticker
def process_ticker(ticker_code):
    print(f"Processing {ticker_code}...")
    existing_data = []  # You can extend this to check for existing data in the database
    last_date = max((row['date'] for row in existing_data), default=None)
    data = fetch_missing_data(ticker_code, last_date)
    if data:
        save_data_to_db(data)
    print(f"Completed {ticker_code}.")


# Function to process tickers using ThreadPoolExecutor
def process_data_with_threads(ticker_codes):
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of threads as needed
        futures = [executor.submit(process_ticker, ticker_code) for ticker_code in ticker_codes]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in thread execution: {e}")


# Function to fetch ticker codes from the MSE website
def fetch_issuer_codes():
    url = "https://www.mse.mk/en/stats/symbolhistory/KMB"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        select_tag = soup.find('select', {'id': 'Code'})
        if select_tag:
            return [option.text.strip() for option in select_tag.find_all('option') if option.text.strip().isalpha()]
    except requests.RequestException as e:
        print(f"Error fetching issuer codes: {e}")
    return []