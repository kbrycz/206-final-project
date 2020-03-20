import sqlite3 as db


def save_to_db(data, context):
    conn = db.connect('/Users/rishi/SI-206/206-final-project/api/scooby.db')
    cur = conn.cursor()

    cur.execute(
        f'SELECT * FROM {context.capitalize()}Data WHERE day=? AND coin=?', (data[0], data[1]))

    # Reject duplicate data if data already exists for given coin on given day
    try:
        cur.fetchone()[0]
        print(
            f'{context.capitalize()} data already exists for {data[1]} on {data[0]}')

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

        conn.commit()

    cur.close()


def setup_db():
    conn = db.connect('/Users/rishi/SI-206/206-final-project/api/scooby.db')
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS MarketData')
    cur.execute('DROP TABLE IF EXISTS SentimentData')
    cur.execute('DROP TABLE IF EXISTS RedditData')

    cur.execute(
        'CREATE TABLE MarketData (day TEXT, coin TEXT, price TEXT, market_cap TEXT, total_volume TEXT)')
    cur.execute(
        'CREATE TABLE RedditData (day TEXT, coin TEXT, reddit_posts_48h TEXT, reddit_comments_48h TEXT)')
    cur.execute(
        'CREATE TABLE SentimentData (day TEXT, coin TEXT, sentiment TEXT)')

    conn.commit()

    cur.close()


def main():
    setup_db()


if __name__ == "__main__":
    main()
