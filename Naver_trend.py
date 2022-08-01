import urllib.request
from datetime import datetime
from pandas._libs import json
import numpy as np
import pandas as pd


def get_trend(body):
    url = "https://openapi.naver.com/v1/datalab/search"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", "tUHLrGw5VojPF05u2w3o")  # 생성된 클라이언트 아이디
    request.add_header("X-Naver-Client-Secret", "wZHCwf3RCT")  # 생성된 클라이언트 비밀번호
    request.add_header("Content-Type", "application/json")  # json 형태로 생성
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))

    return json.loads(response.read().decode('utf-8'))


body = {
    "startDate": "2019-01-01",  # 시작 날짜
    "endDate": "2019-04-30",  # 끝나는 날짜
    "timeUnit": "week",  # 시간 단위
    "keywordGroups": [
        {"groupName": "타다", "keywords": ["타다", "소카", "vcnc", "VCNC"]},  # 원하는 검색어, 관련 키워드
    ],
}

body = json.dumps(body)  # json 형식으로 만들어줌
print(body)

result = get_trend(body)  # 함수에 전달
print(result)

data = result["results"][0]["data"]
time = np.array([datetime.strptime(i["period"], "%Y-%M-%d") for i in data])
value = np.array([i["ratio"] for i in data])
data = pd.DataFrame({"TIme": time, "Trend_index": value})
print(data)

