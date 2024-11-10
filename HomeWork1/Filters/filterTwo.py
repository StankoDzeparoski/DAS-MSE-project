import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime, timedelta
import calendar
import os

# Function to check if the issuer data exists in the file
def check_existing_data(ticker_code, file_name="tickers_data.csv"):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        # Ensure date is in datetime format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        if ticker_code in df['ticker_code'].values:
            last_date = df[df['ticker_code'] == ticker_code]['date'].max()
            return last_date
    return None  # No data available

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

            start_date_str = start_date.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
            to_date_str = to_date.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'

            params = {'fromDate': start_date_str, 'toDate': to_date_str}
            response = requests.get(url, params=params)  # 10 years ago

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table')

                if table == None: # If no data go next
                    return data

                for row in table.find_all('tr')[1:]:  # Skip header row
                    cells = row.find_all('td')
                    date = cells[0].text.strip()
                    price = cells[1].text.strip().replace(",", "")
                    maxPrice = cells[2].text.strip().replace(",", "")
                    minPrice = cells[3].text.strip().replace(",", "")
                    volume = cells[6].text.strip().replace(",", "")

                    # Skip rows with invalid price
                    if price and price.replace('.', '', 1).isdigit():
                        data.append({'date': date, 'price': float(price), 'ticker_code': ticker_code, 'maxPrice': float(maxPrice or 0), 'minPrice': float(minPrice or 0), 'volume': float(volume or 0)})
                    else:
                        print(f"Skipping row with invalid price for {ticker_code} on date {date}")

                to_date = start_date
                continue
            else:
                print(f"Failed to fetch data for {ticker_code}")
                return None
    return data


# Function to automatically retrieve all issuers from MSE dropdown
def fetch_issuer_codes():
    url = "https://www.mse.mk/en/stats/symbolhistory/KMB"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    select_tag = soup.find('select', {'id': 'Code'})
    issuer_codes = []
    option_tags = select_tag.find_all('option')

    for option in option_tags:
        value = option['value']
        if re.match("^[A-Za-z]+$", value):  # Only include codes without numbers
            issuer_codes.append(value)

    return issuer_codes

# Function to process data: check for existing data, fetch missing data, and save to file
def process_data(ticker_code, file_name="tickers_data.csv"):
    # Check for existing data and get the last available date
    last_date = check_existing_data(ticker_code, file_name)

    if last_date:
        # Convert the string date to a datetime object
        print(f"Existing data for {ticker_code} found. Last available date: {last_date}")
    else:
        last_date = None
        print(f"No existing data found for {ticker_code}. Fetching last 10 years of data.")

    # Fetch missing data starting from the last available date (or from 10 years ago)
    missing_data = fetch_missing_data(ticker_code, last_date)

    if missing_data:
        # If new data is fetched, append it to the existing data (or create new data)
        new_df = pd.DataFrame(missing_data)

        if os.path.exists(file_name):
            existing_df = pd.read_csv(file_name)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_csv(file_name, index=False)  # Save to CSV
        else:
            new_df.to_csv(file_name, index=False)  # Save to new file
        print(f"Data for {ticker_code} has been updated in {file_name}.")
    else:
        print(f"No new data available for {ticker_code}.")


