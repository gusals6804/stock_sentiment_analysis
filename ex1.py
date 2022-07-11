import pandas as pd
from pandas import DataFrame as df
import collections
import glob
import os
import matplotlib.pyplot as plt
import matplotlib



csv = pd.read_csv("C:\\Users\\gusals\\잡것\\Desktop\\데이터분석 특론\\금융\\word_result_KB금융_kb금융주가.csv")
csv.rename(columns={"Unnamed: 0": "date"}, inplace=True)
# print(csv.columns)

csv["date"] = csv["date"].astype('datetime64[ns]')
df = csv.set_index("date")

counter_numbers = collections.Counter(df["UpDown_trend"])
p = counter_numbers[1]
n = counter_numbers[0]
print(counter_numbers[1], counter_numbers[0])
print(len(csv["date"]), len(df))
a = 5000000
b = 20
result = 0
price = []
for j in range(len(df)):
    if b >= 0 and j < len(df) - 1:
        if df["UpDown_trend"][j] == 0:
            a -= int(df["close"][j] * 50 * 1.001)
            price.append(result)
            b += 50
            print(a, b, "살떄")
        elif df["UpDown_trend"][j] == 1 and df["UpDown_trend"][j + 1] == 0:
            a += int(df["close"][j] * b * 0.996)
            result = (((a - 5000000) / 5000000) * 100)
            print(a, b, result, "팔때")
            price.append(result)
            b -= b
        else:
            price.append(result)
print(b)
if b > 0:
    a += int(df["close"][j] * b * 0.98)
    result = (((a - 5000000) / 5000000) * 100)
    print(a, result)
    price.append(result)
    b -= b

print(a)