import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import calendar
import filterOne
import filterTwo

# Establish a connection to the SQLite database
conn = sqlite3.connect("mse_data.db")  # Database name is "mse_data.db"
cursor = conn.cursor()
conn.commit()

def fetch_all_data_from_db(db_name="mse_data.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM mse_data ORDER BY date ASC")  # Updated table name
    rows = cursor.fetchall()
    connection.close()
    return rows

# Function to check the last available date for a ticker in the database
def check_existing_data(ticker_code):
    cursor.execute('SELECT MAX(date) FROM mse_data WHERE ticker_code = ?', (ticker_code,))  # Updated table name
    result = cursor.fetchone()
    return result[0] if result and result[0] else None

# Function to fetch missing data from the last available date up to today
def fetch_missing_data(ticker_code, start_date):
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date, format='%m/%d/%Y', errors='coerce')  # Updated to MM/DD/YYYY format

    url = f"https://www.mse.mk/en/stats/symbolhistory/{ticker_code}"
    data = []
    to_date = datetime.now()

    while start_date < to_date:
        end_date = start_date + timedelta(days=365 if not calendar.isleap(start_date.year) else 366)
        params = {'fromDate': start_date.strftime('%m/%d/%Y'), 'toDate': min(end_date, to_date).strftime('%m/%d/%Y')}  # Updated to MM/DD/YYYY format

        response = requests.get(url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if not table:
                break  # Exit if there's no data table

            for row in table.find_all('tr')[1:]:  # Skip header row
                cells = row.find_all('td')
                date = pd.to_datetime(cells[0].text.strip(), errors='coerce').strftime('%m/%d/%Y')  # Updated to MM/DD/YYYY format
                last_price = filterTwo.convertToFloatFormat(cells[1])
                max_price = filterTwo.convertToFloatFormat(cells[2])
                min_price = filterTwo.convertToFloatFormat(cells[3])
                volume = filterTwo.convertToFloatFormat(cells[6])

                data.append((ticker_code, date, (last_price or "0.00"), (max_price or "0.00"), (min_price or "0.00"), (volume or "0.00")))

            start_date = end_date
        else:
            print(f"Failed to fetch data for {ticker_code}")
            break
    return data

# Function to update the database with new data
def update_data():
    issuer_codes = filterOne.getTickers()

    for ticker_code in issuer_codes:
        last_date = check_existing_data(ticker_code)
        if not last_date:
            last_date = (datetime.now() - timedelta(days=365*10)).strftime('%m/%d/%Y')  # Default to 10 years ago if no data

        print(f"Fetching missing data for {ticker_code} starting from {last_date}")
        missing_data = fetch_missing_data(ticker_code, last_date)
        if missing_data:
            cursor.executemany("""
                INSERT INTO mse_data (ticker_code, date, last_price, max_price, min_price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, missing_data)
            conn.commit()
    print("Database has been updated.")

    # Close the database connection when done
    conn.close()
