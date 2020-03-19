from pycoingecko import CoinGeckoAPI
from coinlist import coin_list

from news import get_sentiment
from support import get_last_10_days

cg = CoinGeckoAPI()


def get_initial_coins():
    '''
    Top 10 coins by market capitalization as of 7:14pm EST, 3.18.2020

    Used to seed initial coin_list
    '''
    coin_list = []
    for coin in cg.get_coins_markets(vs_currency='usd')[0:10]:
        coin_list.append(coin['id'])

    return coin_list


def get_historical_data():
    '''
    Return current and historical market (CoinGecko) / news (NewsAPI) data for coins in coin_list
    '''
    out_file = open('results.txt', 'w')

    i = 1
    for coin in coin_list:
        print(f"Fetching data for {coin} ({i}/{len(coin_list)})")
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
            sentiment = get_sentiment(coin, day)

            out_file.write(
                f"Coin: {coin.capitalize()}, Day: {day}, Price: {price}, Market Cap: {market_cap}, Volume: {total_volume}, News Sentiment: {sentiment}\n")

        out_file.write("\n")
        i += 1

    out_file.close()


def get_categories_from_data():
    coin = 'bitcoin'
    data = cg.get_coin_history_by_id(coin, '18-03-2020')

    market_data = data['market_data']
    community_data = data['community_data']
    developer_data = data['developer_data']
    public_interest_data = data['public_interest_stats']

    print('\n')
    print('Market Data')
    for k in market_data:
        print(k)
    print('\n')
    print('Community Data')
    for k in community_data:
        print(k)
    print('\n')
    print('Developer Data')
    for k in developer_data:
        print(k)
    print('\n')
    print('Public Interest Data')
    for k in public_interest_data:
        print(k)

    print('\n')
    print('Reddit Data')
    for day in get_last_10_days():
        res = cg.get_coin_history_by_id(coin, day)
        reddit_posts = res['community_data']['reddit_average_posts_48h']
        reddit_comments = res['community_data']['reddit_average_comments_48h']
        total_content = round(reddit_posts * reddit_comments, 1)
        print(
            f"{day}: {reddit_posts} posts * {reddit_comments} comments = {total_content} pieces of content on Reddit for {coin} (48h average)")


def main():
    get_categories_from_data()


if __name__ == "__main__":
    main()
