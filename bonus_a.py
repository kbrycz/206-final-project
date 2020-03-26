'''
BONUS A: Add Additional API Source
Earn up to 30 points for an additional API. 
1. You have to gather 100 items from the API and store it in the database. 
2. You must calculate something from the data in the database.
3. You must write out the calculation in a file.
'''

import nomics
from db import save_to_db, fetch_bonus_data
from datetime import datetime, timedelta
import dateutil.parser


n = nomics.Nomics('bc1f86879166ea948e87283fb43da92a')


def populate_historical_market_data():
    '''
    1. You have to gather 100 items from the API and store it in the database. 
    '''
    d = datetime.today()
    d_100 = d - timedelta(days=100)

    res = n.Markets.get_market_cap_history(
        start=d_100.isoformat("T")+"Z",
        end=d.isoformat("T")+"Z"
    )

    res = res[::-1]
    i = 1

    for r in res:
        market_cap = r['market_cap']
        time_stamp = dateutil.parser.parse(r['timestamp']).strftime('%d-%m-%Y')
        data = (time_stamp, market_cap)
        print(
            f"Saving total market cap data to db from {time_stamp} ({i}/100)")
        i += 1
        save_to_db(data, 'bonus')


def calculate_and_store_data():
    '''
    2. You must calculate something from the data in the database.
    3. You must write out the calculation in a file.
    '''
    out_file = open('output_calculations/bonus_calculations.txt', 'w')
    data = fetch_bonus_data()['total_market_cap_data']
    sorted_data = sorted(
        data, key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'), reverse=True)

    most_recent_day = sorted_data[0]
    oldest_day = sorted_data[-1]

    first_date = most_recent_day[0]
    ending_market_cap = float(most_recent_day[1])

    oldest_date = oldest_day[0]
    starting_market_cap = float(oldest_day[1])

    change_in_market_cap = round(
        ((ending_market_cap - starting_market_cap) / starting_market_cap) * 100, 2)

    out_file.write(
        f"Change in total market cap for all cryptocurrencies from {oldest_date} to {first_date}:\n{change_in_market_cap}%")

    out_file.close()


def main():
    populate_historical_market_data()
    calculate_and_store_data()


if __name__ == '__main__':
    main()
