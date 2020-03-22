import sqlite3 as db
import os


source_dir = os.path.dirname(__file__)  # <-- directory name
full_path = os.path.join(source_dir, 'scooby.db')
conn = db.connect(full_path)


def save_to_db(data, context):
    cur = conn.cursor()
    date = data[0]

    if (context != 'bonus'):
        coin_name = data[1]
        cur.execute(
            f'SELECT * FROM {context.capitalize()}Data WHERE day=? AND coin=?', (date, coin_name))

        # Reject duplicate data if data already exists for given coin on given day
        try:
            cur.fetchone()[0]
            print(
                f'{context.capitalize()} data already exists for {coin_name} on {date}')

        except:
            if (context == 'market'):
                cur.execute(
                    'INSERT INTO MarketData (day, coin, price, market_cap, total_volume) VALUES (?, ?, ?, ?, ?)',
                    data)
            elif (context == 'reddit'):
                cur.execute(
                    'INSERT INTO RedditData (day, coin, reddit_posts_48h, reddit_comments_48h) VALUES (?, ?, ?, ?)',
                    data)
            elif (context == 'sentiment'):
                cur.execute(
                    'INSERT INTO SentimentData (day, coin, sentiment) VALUES (?, ?, ?)',
                    data)

    else:
        cur.execute(
            f'SELECT * FROM BonusData WHERE day=?', (date,))

        try:
            cur.fetchone()[0]
            print(f'Total Market Volume data already exists for {date}')

        except:
            cur.execute(
                'INSERT INTO BonusData (day, market_cap_of_market) VALUES (?, ?)',
                data)

    conn.commit()

    cur.close()


def setup_db():
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS MarketData')
    cur.execute('DROP TABLE IF EXISTS SentimentData')
    cur.execute('DROP TABLE IF EXISTS RedditData')
    cur.execute('DROP TABLE IF EXISTS BonusData')

    cur.execute(
        'CREATE TABLE MarketData (day TEXT, coin TEXT, price TEXT, market_cap TEXT, total_volume TEXT)')
    cur.execute(
        'CREATE TABLE RedditData (day TEXT, coin TEXT, reddit_posts_48h TEXT, reddit_comments_48h TEXT)')
    cur.execute(
        'CREATE TABLE SentimentData (day TEXT, coin TEXT, sentiment TEXT)')
    cur.execute(
        'CREATE TABLE BonusData (day TEXT, market_cap_of_market TEXT)')

    conn.commit()

    cur.close()


def fetch_all_data():
    '''
    Fetches data from 3 primary tables (not counting BonusData table)
    '''
    cur = conn.cursor()

    # Database Join for the three tables
    cur.execute(
        'SELECT MarketData.*, RedditData.reddit_posts_48h, RedditData.reddit_comments_48h, SentimentData.sentiment FROM MarketData INNER JOIN RedditData ON MarketData.coin=RedditData.coin AND MarketData.day=RedditData.day INNER JOIN SentimentData ON MarketData.coin=SentimentData.coin AND MarketData.day=SentimentData.day')

    res_dict = {'bitcoin': [], 'litecoin': [],
                'tether': [], 'ripple': [], 'ethereum': []}

    for r in cur:
        res_dict[r[1]].append(r)

    cur.close()
    return res_dict


def fetch_bonus_data():
    cur = conn.cursor()

    cur.execute('SELECT * FROM BonusData')

    res_dict = {'total_market_cap_data': []}

    for r in cur:
        res_dict['total_market_cap_data'].append(r)

    cur.close()
    return res_dict


def main():
    setup_db()


if __name__ == "__main__":
    main()
