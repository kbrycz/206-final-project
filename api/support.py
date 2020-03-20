'''
Support functions
'''

from datetime import datetime, timedelta


def get_last_20_days(start_day):
    '''
    Get dates for the last 20 days from start_day
    '''
    d = datetime.strptime(start_day, '%d-%m-%Y')

    date_list = []

    NUM_DAYS = 20

    for i in range(NUM_DAYS):
        formatted_date = d.strftime('%d-%m-%Y')
        date_list.append(formatted_date)
        d = d - timedelta(days=1)

    return date_list
