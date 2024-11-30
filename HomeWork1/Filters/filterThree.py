import sqlite3

def fetch_all_data_from_db(db_name="mse_data.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM 'mse_data.db' ORDER BY date ASC")
    rows = cursor.fetchall()
    connection.close()
    return rows

# import requests
# from bs4 import BeautifulSoup
# import re
# import pandas as pd
# from datetime import datetime, timedelta
# import calendar
# import os
#
# # Function to check for the last available date for a ticker in the existing data
# def check_existing_data(ticker_code, df):
#     if ticker_code in df['ticker_code'].values:
#         last_date = df[df['ticker_code'] == ticker_code]['date'].max()
#         return last_date
#     return None
#
# # Function to fetch missing data from the last available date up to today
# def fetch_missing_data(ticker_code, start_date):
#     # Convert start_date to a datetime object if it's a string
#     if isinstance(start_date, str):
#         start_date = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce', dayfirst=True)
#
#     url = f"https://www.mse.mk/mk/stats/symbolhistory/{ticker_code}"
#     data = []
#     to_date = datetime.now()
#
#     while start_date < to_date:
#         end_date = start_date + timedelta(days=365 if not calendar.isleap(start_date.year) else 366)
#         params = {'fromDate': start_date.strftime('%Y-%m-%d'), 'toDate': min(end_date, to_date).strftime('%Y-%m-%d')}
#
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             table = soup.find('table')
#             if not table:
#                 break  # Exit if there's no data table
#
#             for row in table.find_all('tr')[1:]:  # Skip header row
#                 cells = row.find_all('td')
#                 # Use dayfirst=True for ambiguous date formats like "31.7.2024"
#                 date = pd.to_datetime(cells[0].text.strip(), errors='coerce', dayfirst=True).strftime('%Y-%m-%d')
#                 price = cells[1].text.strip().replace(",", "")
#                 max_price = cells[2].text.strip().replace(",", "")
#                 min_price = cells[3].text.strip().replace(",", "")
#                 volume = cells[6].text.strip().replace(",", "")
#
#                 # Ensure numeric values and append to data list
#                 if price.replace('.', '', 1).isdigit():
#                     data.append({
#                         'date': date,
#                         'price': float(price),
#                         'ticker_code': ticker_code,
#                         'maxPrice': float(max_price or 0),
#                         'minPrice': float(min_price or 0),
#                         'volume': float(volume or 0)
#                     })
#             start_date = end_date  # Move the date window forward
#         else:
#             print(f"Failed to fetch data for {ticker_code}")
#             break
#     return data
#
# # Function to load or create a DataFrame for the database
# def load_existing_data(file_name="tickers_data.csv"):
#     if os.path.exists(file_name):
#         return pd.read_csv(file_name, parse_dates=['date'])
#     else:
#         return pd.DataFrame(columns=['date', 'price', 'ticker_code', 'maxPrice', 'minPrice', 'volume'])
#
# # Main function to update data for each issuer, format, and save
# def update_data_with_formatting(file_name="tickers_data.csv"):
#     all_data_df = load_existing_data(file_name)
#     issuer_codes = fetch_issuer_codes()  # Assuming this function is from previous code
#
#     for ticker_code in issuer_codes:
#         # Check last date for the issuer
#         last_date = check_existing_data(ticker_code, all_data_df)
#         if not last_date:
#             last_date = (datetime.now() - timedelta(days=365*10)).strftime('%Y-%m-%d')  # Default to 10 years ago if no data
#
#         print(f"Fetching missing data for {ticker_code} starting from {last_date}")
#
#         # Fetch missing data from last date to present
#         missing_data = fetch_missing_data(ticker_code, last_date)
#         if missing_data:
#             new_data_df = pd.DataFrame(missing_data)
#             all_data_df = pd.concat([all_data_df, new_data_df], ignore_index=True)
#             all_data_df.drop_duplicates(subset=['date', 'ticker_code'], inplace=True)
#
#         # Format data into numeric values
#     if not pd.api.types.is_float_dtype(all_data_df['volume']):
#         all_data_df['price'] = pd.to_numeric(all_data_df['price'], errors='coerce')
#         all_data_df['maxPrice'] = pd.to_numeric(all_data_df['maxPrice'], errors='coerce')
#         all_data_df['minPrice'] = pd.to_numeric(all_data_df['minPrice'], errors='coerce')
#         all_data_df['volume'] = pd.to_numeric(all_data_df['volume'], errors='coerce')
#     else:
#         # Format prices with comma for thousands and period for decimals
#         all_data_df['price'] = all_data_df['price'].map('{:,.2f}'.format)
#         all_data_df['maxPrice'] = all_data_df['maxPrice'].map('{:,.2f}'.format)
#         all_data_df['minPrice'] = all_data_df['minPrice'].map('{:,.2f}'.format)
#         all_data_df['volume'] = all_data_df['volume'].map('{:,.0f}'.format)  # Assume volume as integer format
#
#     # Save updated data to CSV file with date format and comma delimiters
#     all_data_df.to_csv(file_name, index=False, date_format='%Y-%m-%d', float_format='%.2f')
#     print(f"Data has been saved and formatted in {file_name}.")
#
# # Function to fetch issuer codes from previous code
# def fetch_issuer_codes():
#     url = "https://www.mse.mk/en/stats/symbolhistory/KMB"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     select_tag = soup.find('select', {'id': 'Code'})
#     issuer_codes = []
#
#     if select_tag:
#         for option in select_tag.find_all('option'):
#             value = option['value']
#             if re.match("^[A-Za-z]+$", value):
#                 issuer_codes.append(value)
#     return issuer_codes
