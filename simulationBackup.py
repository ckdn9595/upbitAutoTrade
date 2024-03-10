import matplotlib.pyplot as plt
# import sys
# import os
import io
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
import pyupbit
import influx_read
from Indicators.bollinger_bands import bollinger
from Indicators.adx import adx
from datetime import datetime, timedelta
import pytz
import json
import logging

#컬럼 출력 조절되는 기본 옵션 제거
pd.set_option('display.max_columns', None)
# 로깅 기본 설정: 로그 레벨, 로그 파일 경로 및 로그 메시지 포맷
logging.basicConfig(level=logging.DEBUG,
                    filename='websocket.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 콘솔에도 로그 출력을 원할 경우 핸들러 추가
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
logging.getLogger('').addHandler(consoleHandler)

timezone = pytz.timezone("Asia/Seoul")

# 볼린저 1일, 1시간, 1분 단위로 총 3가지 기간으로 본다.
read_influx = influx_read.readInfluxData()
measure_name = "KRW-BTC"
# 시뮬레이션 시작 시간
simulation_start_time = datetime.strptime(
    "2024-02-09 17:00:00", "%Y-%m-%d %H:%M:%S")
# 시뮬레이션 현재 시간 조정하기
simulation_now_time = simulation_start_time
# 실시간 가격 데이터를 받아오는 부분
# now_price = pyupbit.get_current_price("KRW-BTC")
now_price = json.loads(read_influx.read_with_range_pivot(
    measure_name, simulation_now_time.isoformat()+"Z",
    (simulation_now_time + timedelta(minutes=1)).isoformat()+"Z"))[0]["close"]
# 과거 19일 동안의 날짜를 오전 9시로 설정하여 리스트에 저장
dates_list = [(simulation_now_time - timedelta(days=i))
              .replace(hour=9, minute=0, second=0, microsecond=0)
              for i in range(30, 0, -1)]
hour_list = [(simulation_now_time - timedelta(hours=i))
             .replace(minute=0, second=0, microsecond=0)
             for i in range(30, 0, -1)]
last_19days = pyupbit.get_ohlcv(
    "KRW-BTC", interval="day", to="202402091700", count=30)

last_19days.reset_index(drop=True, inplace=True) # 인덱스로 타임스탬프는 너무 사용하기 힘들어서 인덱스로 바꿔버림
#last_19days = []
last_19hour = []
dataframes = []
# RFC3339 포맷으로 변환하여 출력
# for date in dates_list:
#     temp = read_influx.read_with_range_pivot(
#         measure_name, date.isoformat()+"Z", (date + timedelta(minutes=1)).isoformat()+"Z")

#     temp_data = json.loads(temp)
#     df = pd.DataFrame(temp_data, columns=[
#                       "_time", "close", "da20", 'high', 'low'])
#     dataframes.append(df)
# last_19days = pd.concat(dataframes, ignore_index=True)
# last_19days.set_index('_time', inplace=True)
dataframes = []
for hour in hour_list:
    temp = read_influx.read_with_range_pivot(
        measure_name, hour.isoformat()+"Z", (hour + timedelta(minutes=1)).isoformat()+"Z")

    temp_data = json.loads(temp)
    # 20시간 전부터 시간 별 종가 정보
    df = pd.DataFrame(temp_data, columns=["_time", "close", "da20", 'high', 'low'])
    dataframes.append(df)
last_19hour = pd.concat(dataframes, ignore_index=True)

start_time = simulation_now_time - timedelta(minutes=30)
json_data = io.StringIO(read_influx.read_with_range_pivot(
    measure_name, start_time.isoformat()+"Z", simulation_now_time.isoformat()+"Z"))
last_19min = pd.read_json(json_data)[["_time", "close", "da20", 'high', 'low']]

bollinger = bollinger()
bollinger.calc_bolinger_day(last_19days, now_price, simulation_now_time.isoformat())
bollinger.calc_bolinger_hour(last_19hour, now_price, simulation_now_time.isoformat())
bollinger.calc_bolinger_min(last_19min, now_price, simulation_now_time.isoformat())
adx = adx()
adx.calc_adx(last_19days, now_price)
adx.calc_adx(last_19hour, now_price)
adx.calc_adx(last_19min, now_price)
logging.info(last_19days)
