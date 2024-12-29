from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch and analyze news sentiment for a given company
def get_news_sentiment(ticker_code, company_name):
    urls = [f"https://www.mse.mk/mk/news/latest/{i}" for i in range(1, 10)]

    news_links = []
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content, "html.parser")
        panel_body = soup.find("div", class_="panel-body")
        if panel_body:
            links = panel_body.find_all("a", href=True)
            news_links.extend([link["href"] for link in links])

    if not news_links:
        return {"error": "No news links found."}

    sia = SentimentIntensityAnalyzer()
    company_sentiment = {"positive": 0, "negative": 0, "neutral": 0}
    company_news_found = False

    for link in news_links:
        if not link.startswith("http"):
            link = f"https://www.mse.mk{link}"
        response = requests.get(link)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content, "html.parser")
        news_text = soup.get_text()

        if company_name.lower() in news_text.lower() or ticker_code.lower() in news_text.lower():
            company_news_found = True
            sentiment_score = sia.polarity_scores(news_text)
            if sentiment_score["compound"] > 0.05:
                company_sentiment["positive"] += 1
            elif sentiment_score["compound"] < -0.05:
                company_sentiment["negative"] += 1
            else:
                company_sentiment["neutral"] += 1

    if not company_news_found:
        return {"error": f"No news found for {company_name} ({ticker_code})."}

    return company_sentiment

@app.route('/get-sentiment', methods=['GET'])
def sentiment():
    ticker_code = request.args.get('ticker_code')
    company_name = request.args.get('company_name')

    if not ticker_code or not company_name:
        return jsonify({"error": "ticker_code and company_name are required parameters."}), 400

    sentiment = get_news_sentiment(ticker_code, company_name)
    return jsonify(sentiment)

if __name__ == '__main__':
    app.run(debug=True)
