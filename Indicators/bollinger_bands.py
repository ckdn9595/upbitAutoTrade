import unittest
import matplotlib.pyplot as plt
import readInfluxData
from datetime import datetime, timezone, time, timedelta
import pytz


# 날짜 및 시간 객체 간의 차이 계산
# delta = datetime.datetime(2022, 3, 1, 12, 30, 45) - datetime.datetime(2022, 2, 28, 11, 15, 30)
# print("두 날짜 및 시간의 차이:", delta)
timezone = pytz.timezone("Asia/Seoul")
influx_reader = readInfluxData()
start_str = "2023-12-02 09:00"
end_str = "2023-12-03 09:00"
start = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
end = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
json_data = influx_reader.read_with_range("KRW-BTC", start, end)
print(json_data)
