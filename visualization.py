import db
from pprint import pprint
import plotly.offline as po
import pandas as pd
import plotly.graph_objs as go

import matplotlib.pyplot as plt
import seaborn as sns

# {'bitcoin': [('18-03-2020',
#               'bitcoin',
#               '5389.42',
#               '98079756006.79',
#               '36007089253.82',
#               '7.75',
#               '413.833',
#               '0.1'),

data = db.fetch_all_data()

# ------Vis 1 : Returns over (28-02-2020 to 21-03-2020)---------
coins = ['Bitcoin', 'Ethereum', 'Litecoin', 'Ripple', 'Tether']
returns = []

# Bitcoin
bitcoin_data = data['bitcoin']
lastIndex = 0
firstIndex = 0
count = 0
for it in bitcoin_data:
    if it[0] == "28-02-2020":
        firstIndex = count
    elif it[0] == "21-03-2020":
        lastIndex = count
    count += 1

last_price = float(bitcoin_data[lastIndex][2])
first_price = float(bitcoin_data[firstIndex][2])
return_val = ((last_price - first_price) / first_price) * 100
returns.append(return_val)

# Ethererum
ether_data = data['ethereum']
lastIndex = 0
firstIndex = 0
count = 0
for it in ether_data:
    if it[0] == "28-02-2020":
        firstIndex = count
    elif it[0] == "21-03-2020":
        lastIndex = count
    count += 1

last_price = float(ether_data[lastIndex][2])
first_price = float(ether_data[firstIndex][2])
return_val = ((last_price - first_price) / first_price) * 100
returns.append(return_val)

# Litecoin
lit_data = data['litecoin']
lastIndex = 0
firstIndex = 0
count = 0
for it in lit_data:
    if it[0] == "28-02-2020":
        firstIndex = count
    elif it[0] == "21-03-2020":
        lastIndex = count
    count += 1

last_price = float(lit_data[lastIndex][2])
first_price = float(lit_data[firstIndex][2])
return_val = ((last_price - first_price) / first_price) * 100
returns.append(return_val)

# Ripple
rip_data = data['ripple']
lastIndex = 0
firstIndex = 0
count = 0
for it in rip_data:
    if it[0] == "28-02-2020":
        firstIndex = count
    elif it[0] == "21-03-2020":
        lastIndex = count
    count += 1

last_price = float(rip_data[lastIndex][2])
first_price = float(rip_data[firstIndex][2])
return_val = ((last_price - first_price) / first_price) * 100
returns.append(return_val)

# Tether
tether_data = data['tether']
lastIndex = 0
firstIndex = 0
count = 0
for it in tether_data:
    if it[0] == "28-02-2020":
        firstIndex = count
    elif it[0] == "21-03-2020":
        lastIndex = count
    count += 1

last_price = float(tether_data[lastIndex][2])
first_price = float(tether_data[firstIndex][2])
return_val = ((last_price - first_price) / first_price) * 100
returns.append(return_val)

# Print visualization
trace1 = go.Bar(
    x = coins,
    y = returns,
    marker=dict(
        color='rgb(26, 118, 255)'
    )
)
d = [trace1]
layout = go.Layout(
    title='Percent Change in Price (28-02-2020 to 21-03-2020)',
    xaxis=dict(
        title='Coins',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='Percent Change',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
fig = go.Figure(data=d, layout=layout)
fig.update_layout(title_text='Percent Change in Price (2/28/2020 to 3/21/2020)', title_x=0.5)
po.iplot(fig)

# ---------Vis 2: Create pie chart with market cap---------------
marketCaps = []
# for 18-03-2020
dataBonus = db.fetch_bonus_data()
totalMarket = dataBonus['total_market_cap_data'][4][1]
for it in data['bitcoin']:
    if it[0] == '18-03-2020':
        marketCaps.append(float(it[3]))
for it in data['ethereum']:
    if it[0] == '18-03-2020':
        marketCaps.append(float(it[3]))
for it in data['litecoin']:
    if it[0] == '18-03-2020':
        marketCaps.append(float(it[3]))
for it in data['ripple']:
    if it[0] == '18-03-2020':
        marketCaps.append(float(it[3]))
for it in data['tether']:
    if it[0] == '18-03-2020':
        marketCaps.append(float(it[3]))

fig = {
  "data": [
    {
      "values": marketCaps,
      "labels": coins,
      "name": "Coin Percentages",
      "hoverinfo":"label+percent+name",
      "hole": .4,
      "type": "pie"
    }],
  "layout": {
        "title":"Percentage of Total Market Cap of Coins on 3/18/2020",
        "title_x": 0.5,
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": "Coin %",
                "x": 0.5,
                "y": 0.5
            },
        ]
    }
}

po.iplot(fig)

# -------------Vis 3: Average sentiment score over time
sentimentsBC = []
avg = 0
for it in data['bitcoin']:
    sentimentsBC.append(float(it[-1]))

sentimentsET = []
avg = 0
for it in data['ethereum']:
    sentimentsET.append(float(it[-1]))

sentimentsLC = []
avg = 0
for it in data['litecoin']:
    sentimentsLC.append(float(it[-1]))

sentimentsRP = []
avg = 0
for it in data['ripple']:
    sentimentsRP.append(float(it[-1]))

sentimentsTR = []
avg = 0
for it in data['tether']:
    sentimentsTR.append(float(it[-1]))

days = []
for i in range(21):
    days.append(i)
    
# Create traces
trace0 = go.Scatter(
    x = days,
    y = sentimentsBC,
    mode = 'lines+markers',
    name = 'Bitcoin Sentiment'
)
trace1 = go.Scatter(
    x = days,
    y = sentimentsET,
    mode = 'lines+markers',
    name = 'Ethereum Sentiment'
)
trace2 = go.Scatter(
    x = days,
    y = sentimentsLC,
    mode = 'lines+markers',
    name = 'Litecoin Sentiment'
)
trace3 = go.Scatter(
    x = days,
    y = sentimentsRP,
    mode = 'lines+markers',
    name = 'Ripple Sentiment'
)
trace4 = go.Scatter(
    x = days,
    y = sentimentsTR,
    mode = 'lines+markers',
    name = 'Tether Sentiment'
)

layout = dict(title = 'Change in Sentiment Scores (2/28/2020 to 3/21/2020)',
              title_x=0.5,
              xaxis = dict(title = 'Day'),
              yaxis = dict(title = 'Sentiment Score (-1 to 1)'),
              )

fig = [trace0, trace1, trace2, trace3, trace4]
fig = dict(data=fig, layout=layout)

po.iplot(fig)

# ----------Vis 4 Comments per post--------------

commentsPerPost = []
total = 0
count = 0
for it in data['bitcoin']:
    posts = float(it[-3])
    comments = float(it[-2])
    total += (posts/ comments)
    count += 1
commentsPerPost.append(total / count)

total = 0
count = 0
for it in data['ethereum']:
    posts = float(it[-3])
    comments = float(it[-2])
    total += (posts/ comments)
    count += 1
commentsPerPost.append(total / count)

total = 0
count = 0
for it in data['litecoin']:
    posts = float(it[-3])
    comments = float(it[-2])
    total += (posts/ comments)
    count += 1
commentsPerPost.append(total / count)

total = 0
count = 0
for it in data['ripple']:
    posts = float(it[-3])
    comments = float(it[-2])
    total += (posts/ comments)
    count += 1
commentsPerPost.append(total / count)

total = 0
count = 0
for it in data['tether']:
    posts = float(it[-3])
    comments = float(it[-2])
    total += (posts/ comments)
    count += 1
commentsPerPost.append(total / count)

trace1 = go.Bar(
    x = coins,
    y = commentsPerPost,
    marker=dict(
        color='rgb(200, 11, 25)'
    )
)
d = [trace1]
layout = go.Layout(
    title='Average Comments per Post (28-02-2020 to 21-03-2020)',
    xaxis=dict(
        title='Coins',
        titlefont=dict(
            size=16,
            color='rgb(17, 207, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(17, 207, 107)'
        )
    ),
    yaxis=dict(
        title='Comments per Post',
        titlefont=dict(
            size=16,
            color='rgb(17, 207, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(17, 207, 107)'
        )
    ),
    barmode='group',
    bargap=0.3,
    bargroupgap=0.3
)
fig = go.Figure(data=d, layout=layout)
fig.update_layout(title_text='Average Comments per Post (28-02-2020 to 21-03-2020)', title_x=0.5)
po.iplot(fig)