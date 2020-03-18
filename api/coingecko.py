from pycoingecko import CoinGeckoAPI
from coinlist import coin_list
from datetime import datetime, timedelta

cg = CoinGeckoAPI()


def get_initial_coins():
    '''
    Top 10 coins as of 7:14pm EST, 3.18.2020

    Used to seed initial coin_list
    '''
    coin_list = []
    for coin in cg.get_coins_markets(vs_currency='usd')[0:10]:
        coin_list.append(coin['id'])

    return coin_list


def get_last_10_days():
    '''
    Get dates for the 10 days, inclusive    
    '''
    first_day = '18-03-2020'
    d = datetime.strptime(first_day, '%d-%m-%Y')

    date_list = []

    for i in range(10):
        formatted_date = d.strftime('%d-%m-%Y')
        date_list.append(formatted_date)
        d = d - timedelta(days=1)

    return date_list


def get_coin_data():
    '''
    Return current and historical market data for coins in coin_list
    '''
    out_file = open('results.txt', 'w')
    for coin in coin_list:
        out_file.write(
            f"{coin.capitalize()} historical data for past 10 days\n")
        for day in get_last_10_days():
            res = cg.get_coin_history_by_id(coin, day)

            # Market Data
            market_data = res['market_data']
            price = market_data['current_price']['usd']
            market_cap = market_data['market_cap']['usd']
            total_volume = market_data['total_volume']['usd']

            out_file.write(
                f"Day: {day}, Price: {price}, Market Cap: {market_cap}, Volume: {total_volume}\n")

        out_file.write("\n")

    out_file.close()


get_coin_data()
