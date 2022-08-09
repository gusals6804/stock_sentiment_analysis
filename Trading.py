import pandas as pd
from pandas import DataFrame as df
import collections
import glob
import os
import matplotlib.pyplot as plt
import matplotlib

plt.ioff()

csv_list = glob.glob('C:\\Users\\gusals\\잡것\\Desktop\\데이터분석 특론\\광고/*.csv')

#csv = pd.read_csv("C:\\Users\\gusals\\잡것\\Desktop\\데이터분석 특론\\금융\\word_result_KB금융_kb금융지주.csv")
total = 0

o = []
x = []
total = 0
for i in csv_list:
    csv = pd.read_csv(i)
    csv.rename(columns={"Unnamed: 0": "date"}, inplace=True)
    #print(csv.columns)

    csv["date"] = csv["date"].astype('datetime64[ns]')
    df = csv.set_index("date")


    counter_numbers = collections.Counter(df["UpDown_trend"])
    p = counter_numbers[1]
    n = counter_numbers[0]
    #print(counter_numbers[1], counter_numbers[0])
    #print(len(csv["date"]), len(df))
    a = 1000000
    b = 20
    result = 0
    price = []
    for j in range(len(df)):
        if b >= 0 and j < len(df)-1:
            if df["UpDown_trend"][j] == 0:
                a -= int(df["close"][j] * 10 * 1.001)
                price.append(result)
                b += 10
            elif df["UpDown_trend"][j] == 1 and df["UpDown_trend"][j+1] == 0:
                a += int(df["close"][j] * b * 0.997)
                result = (((a-1000000)/1000000)*100)
                price.append(result)
                b -= b
            else:
                price.append(result)

    if b > 0:
        a += int(df["close"][j] * b * 0.98)
        result = (((a - 1000000) / 1000000) * 100)
        price.append(result)
        b -= b
    else:
        result = (((a - 1000000) / 1000000) * 100)
        price.append(result)

#plt.title(os.path.splitext(os.path.split(i)[1])[0])
    if price[len(price)-1] >= 0:
        # plt.ylim(min(price)-3, max(price)+3)
        # plt.plot(csv["date"], price)
        # plt.savefig('C:\\Users\\gusals\\잡것\\Desktop\\데이터분석 특론\\반도체결과\\플러스\\%s.png' % os.path.splitext(os.path.split(i)[1])[0], dpi=300)
        # plt.show()
        if p > n:
            o.append(max(price))
        else:
            x.append(min(price))
    else:
        # plt.ylim(min(price) - 3, max(price) + 3)
        # plt.plot(csv["date"], price)
        # plt.savefig('C:\\Users\\gusals\\잡것\\Desktop\\데이터분석 특론\\반도체결과\\마이너스\\%s.png' % os.path.splitext(os.path.split(i)[1])[0],
        #             dpi=300)
        # plt.show()
        if p < n:
            o.append(min(price))
        else:
            x.append(max(price))
    total += (a - 1000000)
    print(os.path.splitext(os.path.split(i)[1])[0], a, price[len(price)-1], p/(p+n)*100)

print(len(o), len(x))
print(len(o)/(len(o)+len(x))*100, total, len(o)+len(x))
