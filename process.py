from db import fetch_all_data
from datetime import datetime


def process_data(data):
    out_file = open('process_results.txt', 'w')
    for k, v in data.items():
        sorted_data = sorted(
            v, key=lambda x: datetime.strptime(x[0], '%d-%m-%Y'), reverse=True)
        most_recent_data = sorted_data[0]
        last_data = sorted_data[-1]

        end_date = most_recent_data[0]
        start_date = last_data[0]

        price_end = float(most_recent_data[2])
        price_start = float(last_data[2])
        market_cap_end = float(most_recent_data[3])
        market_cap_start = float(last_data[3])
        volume_end = float(most_recent_data[4])
        volume_start = float(last_data[4])

        # Calculated Statistics
        total_reddit_content = 0
        total_sentiment = 0
        for x in sorted_data:
            posts_48h = float(x[5])
            comments_48h = float(x[6])
            sentiment = float(x[7])
            total_reddit_content += posts_48h * comments_48h
            total_sentiment += sentiment

        average_reddit_content_48h = round(total_reddit_content / len(v), 2)
        average_sentiment_score = round(total_sentiment / len(v), 2)
        percent_change_price = round(
            ((price_end - price_start) / price_start) * 100, 2)
        percent_change_market_cap = round(
            ((market_cap_end - market_cap_start) / market_cap_start) * 100, 2)
        percent_change_volume = round(
            ((volume_end - volume_start) / volume_start) * 100, 2)

        data[k].append(percent_change_price)

        print(
            f'Processing {k.capitalize()} statistics from {start_date} to {end_date}')
        out_file.write(
            f"{k.capitalize()} statistics from {start_date} to {end_date}\n")
        out_file.write(
            f"Change in price: {percent_change_price}%\n")
        out_file.write(
            f"Change in market cap: {percent_change_market_cap}%\n")
        out_file.write(
            f"Change in volume: {percent_change_volume}%\n")
        out_file.write(
            f"Average 48h Reddit content (posts * comments): {average_reddit_content_48h}\n")
        out_file.write(
            f"Average sentiment score (1 means positive content, while -1 means negative content): {average_sentiment_score}\n")
        out_file.write('\n')

    price_changes = []
    for k, v in data.items():
        price_changes.append((k, v[-1]))

    price_changes = sorted(price_changes, key=lambda x: x[1])
    biggest_loser = price_changes[0]

    out_file.write(
        f"Coin with biggest loss: {biggest_loser[0].capitalize()} ({biggest_loser[1]}%)")

    out_file.close()


def main():
    data = fetch_all_data()
    process_data(data)


if __name__ == "__main__":
    main()
