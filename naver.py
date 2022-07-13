import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from datetime import datetime
from pandas._libs import json
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import collections
from Price_Cr import stock_price
import matplotlib.pyplot as plt


def search(name):
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%s" % (name)
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    event_list = bs_obj.find_all('a')

    relation_word = []

    idx = 0
    for s in event_list:
        try:
            if re.search("where=nexearch&query=", s.get('href')) != None:
                #print("%d : %s, %s" % (idx, s.get('href'), s.get_text()))
                relation_word.append(s.get_text())

        except UnicodeEncodeError:
            print("Errror : %d" % (idx))
        finally:
            idx += 1

    #print(list(set(relation_word)))

    return relation_word


def get_trend(name):
    #relation_word = search(str(name))
    print(name, "get_Trend")

    body = {
        "startDate": "2016-12-08",
        "endDate": "2019-12-16",
        "timeUnit": "date",
        "keywordGroups": [
            {"groupName": name, "keywords": [name]},
        ],
    }

    body = json.dumps(body, ensure_ascii=False)

    url = "https://openapi.naver.com/v1/datalab/search"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", "tUHLrGw5VojPF05u2w3o")
    request.add_header("X-Naver-Client-Secret", "wZHCwf3RCT")
    request.add_header("Content-Type", "application/json")
    response = urllib.request.urlopen(request, data=str(body).encode("utf-8"))
    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    #return json.loads(response.read().decode('utf-8'))


def chart(name, stock_name):

    stock_date, stock_close, stock_updown = stock_price("kb금융", "105560")

    result = get_trend(str(name))
    data = result["results"][0]["data"]
    time = np.array([(i["period"]) for i in data])
    value = np.array([i["ratio"] for i in data])
    #value = value * 10
    data = {"time": time, "trend": value}
    data = pd.DataFrame(data, columns=["time", "trend"])
    data.set_index('time', inplace=True)

    data['trendLag1'] = data['trend'].shift(-1)
    data['trendDiff'] = data['trendLag1'] - data['trend']
    data['trendPercent'] = round((data['trendDiff'] / data['trend'] * 100), 2)
    data['trendDiff'] = data['trendDiff'].shift(+1)
    data['trendPercent'] = data['trendPercent'].shift(+1)
    data['UpDown'] = [1 if data['trendPercent'].loc[date] > 0 else 0 for date in data.index]
    #data['s_UpDown'] = stock_updown
    x = pd.merge(data, stock_updown, left_index=True, right_index=True, how='inner')
    x = x.rename(
        columns={'UpDown_x': 'UpDown_trend', 'UpDown_y': 'UpDown_price'})
    try:
        x['same'] = [1 if x['UpDown_trend'].loc[date] == x['UpDown_price'].loc[date] else 0 for date in x.index]
    except:
        pass

    counter_numbers = collections.Counter(x['same'])
    # print(counter_numbers[1])
    if counter_numbers[1] > counter_numbers[0]:
        c = counter_numbers[1]
        b = counter_numbers[0]
        percent = round((c / (b + c)) * 100, 2)
        pn = 1
    else:
        c = counter_numbers[1]
        b = counter_numbers[0]
        if b != 0:
            percent = round((b / (b + c) * 100), 2)
            pn = 0
        else:
            percent = 0
            pn = 2

    x = pd.merge(stock_close, x, left_index=True, right_index=True, how='outer')

    #print(x['trend'].isnull().sum())
    trend_ratio = round(((len(x) - x['trend'].isnull().sum())/len(x))*100)

    if trend_ratio > 50:
        print(trend_ratio, "%")
        x.to_csv("C:\\Users\\gusals\\잡것\\Desktop\\데이터분석 특론\\디스플레이\\word_result_%s_%s.csv" % (stock_name, name))

    else:
        print(trend_ratio, "%")

    print(x, len(x), "\n")




    #data = [trace]
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02,
        row_heights=[0.5, 0.5]
    )

    fig.add_trace(go.Scatter(
        x=stock_date,
        y=stock_close,
        name=stock_name + "주가"), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data.trend,
        name="키워드:" + name), row=2, col=1)


    fig.update_layout(
        title='%s "%s" 키워드 Time Series' % (stock_name, name),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=3,
                         label='3m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        )
    )


    # #fig = go.Figure(data=data, layout=layout)
    fig.show()
    return percent, pn, trend_ratio

chart("헬스", "kb금융")
#search("이월드")
#get_trend("sdn")