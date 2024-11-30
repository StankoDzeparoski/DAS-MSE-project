import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import threading

# Lock for database access
data_lock = threading.Lock()

#Convert Numbered string into 36,900.000
def convertToStringFormat(convert):
    if convert.text.strip():
        temp = convert.text.replace(',', 'fak')
        temp = temp.replace('.', ',')
        temp = temp.replace('fak', '.')
        convert = temp
    else:
        convert = "0,00"
    return convert

#Convert Float string from 36,900.00 into float num 36900.00
def convertToFloatFormat(convert):
    if convert.text.strip():
        temp = convert.text.replace(',', '')
        convert = float(temp)
    else:
        convert = 0.00
    return convert

# Update in fetch_missing_data
def fetch_missing_data(ticker_code, start_date=None):
    url = f"https://www.mse.mk/mk/stats/symbolhistory/{ticker_code}"
    data = []
    to_date = datetime.now()

    if not start_date:
        # Fetch data for the last 10 years if no data exists
        for _ in range(10):
            start_date = to_date - timedelta(days=366 if to_date.year % 4 == 0 else 365)
            start_date_str = start_date.strftime('%d.%m.%Y')
            to_date_str = to_date.strftime('%d.%m.%Y')

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
                                'lastPrice': convertToStringFormat(cells[1]),
                                'maxPrice': convertToStringFormat(cells[2]),
                                'minPrice': convertToStringFormat(cells[3]),
                                'volume': convertToStringFormat(cells[4]),
                            })

                    to_date = start_date  # Update to_date for the next iteration
                else:
                    print(f"Failed to fetch data for {ticker_code}, status: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error fetching data for {ticker_code}: {e}")
        return data
    else:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date, format='%d-%m-%Y', errors='coerce', dayfirst=True)
        # Fetch data starting from the given start_date to now
        while start_date < to_date:
            start_date_str = start_date.strftime('%d.%m.%Y')
            to_date_str = to_date.strftime('%d.%m.%Y')

            params = {'fromDate': start_date_str, 'toDate': to_date_str}

            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    table = soup.find('table')

                    if table is None:
                        break

                    for row in table.find_all('tr')[1:]:  # Skip the header row
                        cells = row.find_all('td')
                        if len(cells) >= 7:  # Ensure row has enough columns
                            data.append({
                                'ticker_code': ticker_code,
                                'date': cells[0].text.strip(),
                                'lastPrice': convertToStringFormat(cells[1]),
                                'maxPrice': convertToStringFormat(cells[2]),
                                'minPrice': convertToStringFormat(cells[3]),
                                'volume': convertToStringFormat(cells[4]),
                            })

                    # Update start_date for the next iteration
                    if data:
                        start_date = datetime.strptime(data[-1]['date'], '%d.%m.%Y') + timedelta(days=1)
                    else:
                        break
                else:
                    print(f"Failed to fetch data for {ticker_code}, status: {response.status_code}")
                    break
            except requests.RequestException as e:
                print(f"Error fetching data for {ticker_code}: {e}")
                break

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

def get_latest_date(ticker_code, db_name="mse_data.db"):
    with data_lock:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT MAX(date) FROM "mse_data.db" WHERE ticker_code = ?
        """, (ticker_code,))
        result = cursor.fetchone()
        connection.close()

        return result[0] if result and result[0] else None

# Function to process a single ticker
def process_ticker(ticker_code):
    print(f"Processing {ticker_code}...")
    last_date = get_latest_date(ticker_code)
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