import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def getTickers():
    # Send a GET request to the webpage
    response = requests.get("https://www.mse.mk/en/stats/symbolhistory/KMB")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the select element
    select_tag = soup.find('select', {'id': 'Code'})
    # Extract all option tags within the select tag
    option_tags = select_tag.find_all('option')
    # Filter the tags to exclued non letters and len < 5
    tickerCodes = []
    id = 1
    for option in option_tags:
        tag = option.get_text(strip=True)  # Remove whitespace
        if tag.isalpha() and len(tag) <= 5:
            tickerCodes.append({'Index': id, 'tickerCode': tag})
            id+=1

    return tickerCodes


# Function to process data: check for existing data, fetch missing data, and save to file
def processTickerTagData(file_name="ticker_codes.csv"):
    # Fetch ticker data
    ticker_data = getTickers()

    if ticker_data:
        # Create new DF
        new_df = pd.DataFrame(ticker_data)

        if os.path.exists(file_name):
            existing_df = pd.read_csv(file_name)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates()
            combined_df.to_csv(file_name, index=False)  # Save to CSV
        else:
            new_df.to_csv(file_name, index=False)  # Save to new file
        print(f"Data for ticker codes has been updated in {file_name}.")
    else:
        print(f"No new data available for ticker codes.")

processTickerTagData("ticker_codes.csv")


