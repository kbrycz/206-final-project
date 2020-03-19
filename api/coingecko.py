from pycoingecko import CoinGeckoAPI
from newsapi import NewsApiClient
from coinlist import coin_list
from datetime import datetime, timedelta
from textblob import TextBlob

cg = CoinGeckoAPI()
newsapi = NewsApiClient(api_key='d38ea2916e134db3a2e0deeca8e71a1e')


def get_initial_coins():
    '''
    Top 10 coins by market capitalization as of 7:14pm EST, 3.18.2020

    Used to seed initial coin_list
    '''
    coin_list = []
    for coin in cg.get_coins_markets(vs_currency='usd')[0:10]:
        coin_list.append(coin['id'])

    return coin_list


def get_last_10_days():
    '''
    Get dates for the last 10 days, inclusive
    '''
    first_day = '18-03-2020'
    d = datetime.strptime(first_day, '%d-%m-%Y')

    date_list = []

    NUM_DAYS = 10

    for i in range(NUM_DAYS):
        formatted_date = d.strftime('%d-%m-%Y')
        date_list.append(formatted_date)
        d = d - timedelta(days=1)

    return date_list


def get_sentiment(content):
    '''
    '''
    content = TextBlob(content)
    sentiment = round(content.sentiment.polarity, 2)

    return sentiment


def get_news(coin, day):
    '''
    Returns top headlines for given coin on given day

    Also, returns sentiment score of all headlines and descriptions to determine general sentiment of a coin on a given day
    '''
    reformatted_date = datetime.strptime(day, '%d-%m-%Y').strftime('%Y-%m-%d')
    top_headlines = newsapi.get_everything(q=coin,
                                           from_param=reformatted_date,
                                           to=reformatted_date,
                                           language='en',
                                           sort_by='popularity')

    articles = top_headlines['articles']
    content = ''

    # Merge all headlines and descriptions together and determine sentiment based on aggregate content
    if (len(articles) > 0):
        for article in articles:
            if (article.get('title') and article.get('description')):
                content += article['title'] + " " + article['description']

    sentiment = get_sentiment(content)

    # If no articles for that day, assign a sentiment score of 0
    if (len(content) == 0):
        sentiment = 0

    return sentiment


def get_coin_data():
    '''
    Return current and historical market data for coins in coin_list
    '''
    out_file = open('results.txt', 'w')
    for coin in coin_list:
        print(f"Fetching data for {coin}")
        out_file.write(
            f"{coin.capitalize()} historical data for past 10 days\n")
        for day in get_last_10_days():
            res = cg.get_coin_history_by_id(coin, day)

            # Market Data
            market_data = res['market_data']
            price = market_data['current_price']['usd']
            market_cap = market_data['market_cap']['usd']
            total_volume = market_data['total_volume']['usd']

            # News Data
            sentiment = get_news(coin, day)

            out_file.write(
                f"Coin: {coin.capitalize()}, Day: {day}, Price: {price}, Market Cap: {market_cap}, Volume: {total_volume}, News Sentiment: {sentiment}\n")
            print(f"{day} DONE")

        print("\n")
        out_file.write("\n")

    out_file.close()


get_coin_data()
