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


def main():
    get_historical_data()


if __name__ == "__main__":
    main()
