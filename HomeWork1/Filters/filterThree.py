import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import calendar
import filterOne

# Establish a connection to the SQLite database
conn = sqlite3.connect("mse_data.db")  # Database name is "mse_data.db"
cursor = conn.cursor()
conn.commit()

def fetch_all_data_from_db(db_name="mse_data.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM 'mse_data.db' ORDER BY date ASC")
    rows = cursor.fetchall()
    connection.close()
    return rows

# Function to check the last available date for a ticker in the database
def check_existing_data(ticker_code):
    cursor.execute('SELECT MAX(date) FROM "mse_data.db" WHERE ticker_code = ?', (ticker_code,))
    result = cursor.fetchone()
    return result[0] if result and result[0] else None

# Function to fetch missing data from the last available date up to today
def fetch_missing_data(ticker_code, start_date):
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce', dayfirst=True)

    url = f"https://www.mse.mk/mk/stats/symbolhistory/{ticker_code}"
    data = []
    to_date = datetime.now()

    while start_date < to_date:
        end_date = start_date + timedelta(days=365 if not calendar.isleap(start_date.year) else 366)
        params = {'fromDate': start_date.strftime('%Y-%m-%d'), 'toDate': min(end_date, to_date).strftime('%Y-%m-%d')}

        response = requests.get(url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if not table:
                break  # Exit if there's no data table

            for row in table.find_all('tr')[1:]:  # Skip header row
                cells = row.find_all('td')
                date = pd.to_datetime(cells[0].text.strip(), errors='coerce', dayfirst=True).strftime('%Y-%m-%d')
                price = cells[1].text.strip().replace(",", "")
                max_price = cells[2].text.strip().replace(",", "")
                min_price = cells[3].text.strip().replace(",", "")
                volume = cells[6].text.strip().replace(",", "")

                if price.replace('.', '', 1).isdigit():
                    data.append((ticker_code, date, float(price), float(max_price or 0), float(min_price or 0), float(volume or 0)))
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
            last_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')  # Default to 10 years ago if no data

        print(f"Fetching missing data for {ticker_code} starting from {last_date}")
        missing_data = fetch_missing_data(ticker_code, last_date)
        if missing_data:
            cursor.executemany("""
                INSERT INTO "mse_data.db" (ticker_code, date, lastPrice, maxPrice, minPrice, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, missing_data)
            conn.commit()
    print("Database has been updated.")

    # Close the database connection when done
    conn.close()



