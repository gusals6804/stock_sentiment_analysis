import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import plotly.offline as offline
import plotly.graph_objs as go
from konlpy.tag import Okt
from naver import chart
from naver import search

url = "https://finance.naver.com/sise/sise_group.nhn?type=upjong"
result = requests.get(url)
bs_obj = BeautifulSoup(result.content, "html.parser")

event_list = bs_obj.find_all('a')

event_name = []
event_number = []

idx = 0
for s in event_list[59:137]:
    try:
        event_name.append(s.get_text())
        event_number.append(s.get('href')[43:])
        #print("%d : %s, %s" % (idx, s.get('href'), s.get_text()))

    except UnicodeEncodeError:
        print("Errror : %d" % (idx))
    finally:
        idx += 1
#
# print(event_name)
# print(event_number)

def stock_name(s, word, result_percent, result_pn):
    stock_url = "https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no=" + s
    stock_result = requests.get(stock_url)
    stock_obj = BeautifulSoup(stock_result.content, "html.parser")
    stock_list = stock_obj.find_all('a')

    stock_code = []
    stock_name = []
    idx = 0
    top =0
    for s in stock_list:
        try:
            if re.search("/item/main.nhn", s.get('href')) != None:
                if top <= 10:
                    print("%d : %s, %s" % (idx, s.get('href')[20:], s.get_text()))
                    code = s.get('href')[20:]
                    name = s.get_text()
                    stock_code.append(code)
                    stock_name.append(name)

                    print(list(set(search(name))))
                    for i in list(set(search(name))):
                        stock_date, stock_close, stock_updown = stock_price(name, code)
                        percent, pn, trend_ratio = chart(i, stock_date, stock_close, stock_updown, name)
                        if trend_ratio > 50:
                            word.append(i)
                            result_percent.append(percent)
                            result_pn.append(pn)
                            print(i, percent, pn)
                            print("----------------------------------------------------")
                    top += 1

        except UnicodeEncodeError:
            pass
        finally:
            idx += 1


def stock_price(name, code):
    url = "http://finance.naver.com/item/sise_day.nhn?code=" + code
    df = pd.DataFrame()

    for page in range(1, 75):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    df = df.dropna()

    # 한글로 된 컬럼명을 영어로 바꿔줌
    df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

    # 데이터의 타입을 int형으로 바꿔줌
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df['date'] = pd.to_datetime(df['date'])

    # 일자(date)를 기준으로 오름차순 정렬
    df = df.sort_values(by=['date'], ascending=True)

    df.set_index(('date'), inplace=True)
    df['PriceLag1'] = df['close'].shift(-1)
    df['PriceDiff'] = df['PriceLag1'] - df['close']
    df['DiffPercent'] = round((df['PriceDiff'] / df['close'] * 100), 2)
    df['PriceDiff'] = df['PriceDiff'].shift(+1)
    df['DiffPercent'] = df['DiffPercent'].shift(+1)
    df = df[df['DiffPercent'] != 0]
    df['UpDown'] = [1 if df['DiffPercent'].loc[date] > 0 else 0 for date in df.index]
    print(df, name, len(df), "\n")


    # jupyter notebook 에서 출력
    #offline.init_notebook_mode(connected=True)

    trace = go.Scatter(
        x=df.index,
        y=df['DiffPercent'],
        name=name)

    data = [trace]

    # data = [celltrion]
    layout = dict(
        title='{}의 종가(close) Time Series'.format(name),
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

    fig = go.Figure(data=data, layout=layout)

    #fig.show()

    return df.index, df['close'], df['UpDown']

def word_pn():
    word = []
    result_percent = []
    result_pn = []
    stock_name("199", word, result_percent, result_pn)
    data = {"word": word, "persent": result_percent, "pn": result_pn}
    data = pd.DataFrame(data, columns=["word", "persent", "pn"])
    data.to_csv("C:\\Users\\gusals\\잡것\\Desktop\\데이터분석 특론\\word_result_디스플레이.csv")

#word_pn()

# spliter = Okt()
# nounslist = []
# for i in word:
#     nouns = spliter.nouns(i)
#
#     nounslist.append(i)
#     for j in nouns:
#         if len(j) >= 2:
#             nounslist.append(j)
#
# nounslist = list(set(nounslist))
# print(nounslist)
# print(len(nounslist))
#stock_price("젬백스지오", "041590")
#stock_price("현대에너지솔루션", "322000")




