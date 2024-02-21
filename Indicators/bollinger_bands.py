import matplotlib.pyplot as plt
import pandas as pd
import pyupbit
from influx_read import readInfluxData


class bollinger:
    # data는 기간별 종가 리스트
    def _init__(self, data: list):
        self.data = data
        self.len = len(data)

    def calc_standard_deviation(self, now_price):
        print(self.data)
        print(now_price)
        
##볼린저 1일, 1시간, 10분, 1분 단위로 총 4가지 기간으로 본다.
measure_name = "KRW-BTC"
interval = 'd' # d h m 
period = '-1'
##실시간 가격 데이터를 받아오는 부분
now_price = pyupbit.get_current_price("KRW-BTC")

# 1일이면 19일, 1시간 19시간, 10분 190분, 1분 19분
# 1일을 꺼내면 20ma가 있을 것이다. 사실상 21ma로 써야한다. 나중에 19ma로 쓰자
# -1d를 넣으면 24시간 정보가 오고
read_influx = readInfluxData()
data = read_influx.read_with_period("KRW-BTC", period, interval)
bollinger = bollinger(data)
bollinger.calc_standard_deviation(now_price)

    