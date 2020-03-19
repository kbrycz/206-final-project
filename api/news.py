from newsapi import NewsApiClient
from textblob import TextBlob
from datetime import datetime, timedelta

newsapi = NewsApiClient(api_key='d38ea2916e134db3a2e0deeca8e71a1e')


def get_sentiment(coin, day):
    '''
    Returns aggregate sentiment score for all news content on a given day

    Returns 0 if no content for a given coin on a given day
    '''
    reformatted_date = datetime.strptime(day, '%d-%m-%Y').strftime('%Y-%m-%d')
    top_headlines = newsapi.get_everything(q=coin,
                                           from_param=reformatted_date,
                                           to=reformatted_date,
                                           language='en',
                                           sort_by='popularity')

    articles = top_headlines['articles']
    content = ''

    # Merge all headlines and descriptions together and determine sentiment based on aggregate content
    if (len(articles) > 0):
        for article in articles:
            if (article.get('title') and article.get('description')):
                content += article['title'] + " " + article['description']

    content = TextBlob(content)
    sentiment = round(content.sentiment.polarity, 2)

    # If no articles for that day, assign a sentiment score of 0
    if (len(content) == 0):
        sentiment = 0

    return sentiment
