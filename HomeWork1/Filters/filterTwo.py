import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime, timedelta
import calendar
import os
import threading
import time

data_lock = threading.Lock()

# Function to check if the issuer data exists in the file
def check_existing_data(ticker_code, file_name="tickers_data.csv"):
    try:
        if os.path.exists(file_name):
            df = pd.read_csv(file_name)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

            if ticker_code in df['ticker_code'].values:
                last_date = df[df['ticker_code'] == ticker_code]['date'].max()
                return last_date
        return None
    except Exception as e:
        print(f"Error in check_existing_data for {ticker_code}: {e}")
        return None


# Function to fetch missing data for the ticker (last 10 years)
def fetch_missing_data(ticker_code, start_date=None):
    url = f"https://www.mse.mk/mk/stats/symbolhistory/{ticker_code}"
    data = []
    to_date = datetime.now()

    if not start_date:
        for i in range(1, 11):
            if calendar.isleap(to_date.year):
                start_date = to_date - timedelta(days=366)
            else:
                start_date = to_date - timedelta(days=365)

            start_date_str = start_date.strftime('%Y-%m-%d')
            to_date_str = to_date.strftime('%Y-%m-%d')

            params = {'fromDate': start_date_str, 'toDate': to_date_str}

            # Implement retry logic with exponential backoff
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, params=params, timeout=10)  # Set a timeout of 10 seconds
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        table = soup.find('table')

                        if table is None:
                            continue

                        for row in table.find_all('tr')[1:]:  # Skip header row
                            cells = row.find_all('td')
                            date = cells[0].text.strip()
                            price = cells[1].text.strip().replace(",", "")
                            maxPrice = cells[2].text.strip().replace(",", "")
                            minPrice = cells[3].text.strip().replace(",", "")
                            volume = cells[6].text.strip().replace(",", "")

                            if price and price.replace('.', '', 1).isdigit():
                                data.append({
                                    'date': date, 'price': float(price), 'ticker_code': ticker_code,
                                    'maxPrice': float(maxPrice or 0), 'minPrice': float(minPrice or 0),
                                    'volume': float(volume or 0)
                                })
                            else:
                                print(f"Skipping row with invalid price for {ticker_code} on date {date}")

                        to_date = start_date
                        break  # Exit retry loop on success
                    else:
                        print(f"Failed to fetch data for {ticker_code}, status code: {response.status_code}")
                        return None
                except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                    print(f"Attempt {attempt + 1} failed for {ticker_code}: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        print(f"Max retries reached for {ticker_code}. Skipping...")
                        return None
        return data
    return data


# Function to automatically retrieve all issuers from MSE dropdown
def fetch_issuer_codes():
    try:
        url = "https://www.mse.mk/en/stats/symbolhistory/KMB"
        response = requests.get(url, timeout=10)  # Set a timeout
        soup = BeautifulSoup(response.content, 'html.parser')

        select_tag = soup.find('select', {'id': 'Code'})
        issuer_codes = []
        option_tags = select_tag.find_all('option')

        for option in option_tags:
            value = option['value']
            if re.match("^[A-Za-z]+$", value):  # Only include codes without numbers
                issuer_codes.append(value)

        return issuer_codes
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(f"Error in fetch_issuer_codes: {e}")
        return []


# Function to process data: check for existing data, fetch missing data, and save to file
def process_data(ticker_code, file_name="tickers_data.csv"):
    try:
        last_date = check_existing_data(ticker_code, file_name)

        if last_date:
            print(f"Existing data for {ticker_code} found. Last available date: {last_date}")
        else:
            last_date = None
            print(f"No existing data found for {ticker_code}. Fetching last 10 years of data.")

        missing_data = fetch_missing_data(ticker_code, last_date)

        if missing_data:
            new_df = pd.DataFrame(missing_data)

            with data_lock:  # Ensure only one thread writes to the file at a time
                if os.path.exists(file_name):
                    existing_df = pd.read_csv(file_name)
                    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                    combined_df.to_csv(file_name, index=False)
                else:
                    new_df.to_csv(file_name, index=False)
            print(f"Data for {ticker_code} has been updated in {file_name}.")
        else:
            print(f"No new data available for {ticker_code}.")
    except Exception as e:
        print(f"Error in process_data for {ticker_code}: {e}")


# Function to handle threading
def process_data_with_threading(ticker_codes, file_name="tickers_data.csv"):
    threads = []

    for ticker_code in ticker_codes:
        thread = threading.Thread(target=process_data, args=(ticker_code, file_name))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
