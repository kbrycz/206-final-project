'''
Support functions
'''

from datetime import datetime, timedelta


def get_last_10_days():
    '''
    Get dates for the last 10 days, inclusive
    '''
    first_day = '18-03-2020'
    d = datetime.strptime(first_day, '%d-%m-%Y')

    date_list = []

    NUM_DAYS = 20

    for i in range(NUM_DAYS):
        formatted_date = d.strftime('%d-%m-%Y')
        date_list.append(formatted_date)
        d = d - timedelta(days=1)

    return date_list
