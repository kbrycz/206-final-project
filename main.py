from coingecko import coin_list, cg
from news import get_sentiment
from db import save_to_db

from datetime import datetime, timedelta


def fetch_market_data(day, coin):
    res = cg.get_coin_history_by_id(coin, day)

    market_data = res['market_data']
    price = str(round(market_data['current_price']['usd'], 2))
    market_cap = str(round(market_data['market_cap']['usd'], 2))
    total_volume = str(round(market_data['total_volume']['usd'], 2))

    return (day, coin, price, market_cap, total_volume)


def fetch_reddit_data(day, coin):
    res = cg.get_coin_history_by_id(coin, day)
    community_data = res['community_data']
    reddit_posts_48h = str(community_data['reddit_average_posts_48h'])
    reddit_comments_48h = str(
        community_data['reddit_average_comments_48h'])

    return (day, coin, reddit_posts_48h, reddit_comments_48h)


def fetch_sentiment_data(day, coin):
    sentiment = get_sentiment(coin, day)

    return (day, coin, sentiment)


def fetch_and_save_data():
    '''
    Remember: Must limit data from each API to 20 or fewer items

    Populates DB with following data from yesterday's date (most recent market close):
    CoinGecko API: 10 items (5 rows for market_data, 5 rows for sentiment_data)
    News API: 5 items (5 rows for sentiment_data)
    '''
    yesterdays_date = (datetime.today() - timedelta(days=1)
                       ).strftime('%d-%m-%Y')

    for coin in coin_list:
        print(
            f'Fetching {coin}\'s market, reddit and sentiment data for {yesterdays_date}')
        market_data = fetch_market_data(yesterdays_date, coin)
        reddit_data = fetch_reddit_data(yesterdays_date, coin)
        sentiment_data = fetch_sentiment_data(yesterdays_date, coin)

        save_to_db(market_data, 'market')
        save_to_db(reddit_data, 'reddit')
        save_to_db(sentiment_data, 'sentiment')
        print('\n')


def main():
    fetch_and_save_data()


if __name__ == '__main__':
    main()
