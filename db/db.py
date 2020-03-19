import sqlite3 as db


conn = db.connect('/Users/rishi/SI-206/206-final-project/db/scooby.db')

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS MarketData')
cur.execute('CREATE TABLE MarketData (date TEXT, price INTEGER)')
cur.execute('INSERT INTO MarketData (date, price) VALUES (?, ?)',
            ('18-03-2020', 3400))

conn.commit()

print("Data")
cur.execute('SELECT * FROM MarketData')

for row in cur:
    print(row)

cur.close()
