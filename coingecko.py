from pycoingecko import CoinGeckoAPI

from news import get_sentiment
from support import get_last_20_days

from db import save_to_db, setup_db

cg = CoinGeckoAPI()
coin_list = ['bitcoin', 'ethereum', 'ripple', 'tether', 'litecoin']


def get_historical_data():
    '''
    Return current and historical market (CoinGecko) / news (NewsAPI) data for coins in coin_list
    '''
    starting_day = '18-03-2020'

    # First, clear the DB
    setup_db()

    i = 1
    for coin in coin_list:
        print(
            f"Fetching 20 days worth of data for {coin} ({i}/{len(coin_list)} coins)...")
        for day in get_last_20_days(starting_day):
            res = cg.get_coin_history_by_id(coin, day)

            # Market Data (CoinGeckoAPI)
            market_data = res['market_data']
            price = str(round(market_data['current_price']['usd'], 2))
            market_cap = str(round(market_data['market_cap']['usd'], 2))
            total_volume = str(round(market_data['total_volume']['usd'], 2))

            # Reddit Data (CoinGeckoAPI)
            community_data = res['community_data']
            reddit_posts_48h = str(community_data['reddit_average_posts_48h'])
            reddit_comments_48h = str(
                community_data['reddit_average_comments_48h'])

            # News Data (NewsAPI)
            sentiment = str(get_sentiment(coin, day))

            # Save to DB
            market_data_to_save = (day, coin, price, market_cap, total_volume)
            reddit_data_to_save = (
                day, coin, reddit_posts_48h, reddit_comments_48h)
            sentiment_data_to_save = (day, coin, sentiment)

            save_to_db(market_data_to_save, 'market')
            save_to_db(reddit_data_to_save, 'reddit')
            save_to_db(sentiment_data_to_save, 'sentiment')

        i += 1


def main():
    get_historical_data()


if __name__ == "__main__":
    main()
