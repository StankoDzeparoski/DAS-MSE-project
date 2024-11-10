import requests
from bs4 import BeautifulSoup


def getTickers():
    # Send a GET request to the webpage
    response = requests.get("https://www.mse.mk/en/stats/symbolhistory/KMB")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the select element
    select_tag = soup.find('select', {'id': 'Code'})
    # Extract all option tags within the select tag
    option_tags = select_tag.find_all('option')
    # Filter the tags to exclued non letters and len < 5
    issuer_codes = []
    for option in option_tags:
        tag = option.get_text(strip=True)  # Remove whitespace
        if tag.isalpha() and len(tag) <= 5:
            issuer_codes.append(tag)

    return issuer_codes

print(getTickers())


