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
from algorithm.adx_bolinger_v1 import adx_bollinger, BuyorSell
from buy_sell.buysell import buysell
from datetime import datetime, timedelta
import pytz
import json
import logging


bollinger = bollinger()
adx = adx()
adx_bollinger = adx_bollinger()
buysell_instance = buysell(1000000)  # 초기 자금 100만원 가정
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

read_influx = influx_read.readInfluxData()
measure_name = "KRW-BTC"
# 시뮬레이션 시작 시간
simulation_start_time = datetime.strptime("2021-03-28 00:00:00", "%Y-%m-%d %H:%M:%S")
simulation_end_time = datetime.strptime("2021-03-29 00:00:00", "%Y-%m-%d %H:%M:%S")
# 시뮬레이션 현재 시간 조정하기
simulation_now_time = simulation_start_time

# 매처음 hour list 30개를 유지하는 방법으로 일단 가보자.
hour_list = [(simulation_now_time - timedelta(hours=i))
            .replace(minute=0, second=0, microsecond=0)
            for i in range(30, 0, -1)]
dataframes = []

now_hour = hour_list[(len(hour_list)-1)]
for hour in hour_list:
    temp = read_influx.read_with_range_pivot_tag(
        measure_name, hour.isoformat()+"Z", (hour + timedelta(minutes=1)).isoformat()+"Z", 'hour')

    temp_data = json.loads(temp)
    # 20시간 전부터 시간 별 종가 정보
    df = pd.DataFrame(temp_data, columns=[
                      "_time", "close", 'high', 'low'])
    dataframes.append(df)
    

# 시간봉 이전 30개 데이터
last_30hour = pd.concat(dataframes, ignore_index=True)
cnt = 0

## 지금은 adx를 매번 새로 구하고 있다. 이부분은 추후에 고도화가 분명 필요하다. 효율성을 높일 수 있다.
while (simulation_now_time <= simulation_end_time):
    # 실시간 가격 데이터를 받아오는 부분
    # 시간데이터를 기준으로 돌리고 현재가는 분 봉으로 대체 해서 시뮬레이션을 돌려본다.
    cnt+=1
    if(cnt == 60):
        cnt = 0
        last_30hour = last_30hour.iloc[1:, :] #맨 앞시간 버리고
        temp = read_influx.read_with_range_pivot_tag(
            measure_name, now_hour.isoformat()+"Z", (now_hour + timedelta(hours=1)).isoformat()+"Z", 'hour')

        temp_data = json.loads(temp)
        
        df = pd.DataFrame(temp_data, columns=[
                        "_time", "close", 'high', 'low'])
        last_30hour = pd.concat([last_30hour, df], ignore_index=True)
        now_hour += timedelta(hours=1)
        
    now_price = json.loads(read_influx.read_with_range_pivot_tag(
        measure_name, simulation_now_time.isoformat()+"Z",
        (simulation_now_time + timedelta(minutes=1)).isoformat()+"Z", 'min'))[0]["close"]
    
    # 현재가격 추가
    last_30hour.loc[len(last_30hour)] = {
        "_time": simulation_now_time.isoformat(), "close": now_price, "high": now_price, "low": now_price}
    adx.calc_adx(last_30hour)
    bollinger.calc_bolinger_hour(last_30hour)
    choice = adx_bollinger.buy_sell_algo(last_30hour)
    
    if(choice is BuyorSell.SELL):
        buysell_instance.sell(now_price)
    elif(choice is BuyorSell.BUY):
        buysell_instance.buy(now_price)
    
    simulation_now_time += timedelta(minutes=1)
# --- 거래 시뮬레이션 종료 --- #


# 끝나고 매수인 상태인 경우 결과 확인으르 위해 최종 매도 처리
if (buysell_instance.holding_numbers is not 0):
    now_price = json.loads(read_influx.read_with_range_pivot_tag(
        measure_name, simulation_end_time.isoformat()+"Z",
        (simulation_end_time + timedelta(minutes=1)).isoformat()+"Z", 'min'))[0]["close"]
    buysell_instance.sell(now_price)
    
# TODO: 시뮬레이션을 돌려본다.
buysell_instance.print()
# 그 후에 얼마를 벌고하는지 데이터 통계를 먼저 내보고
# 이를 추가적으로 차트화 시켜서 그래프상 어느지점에서 사고 팔았는지 시각화를 해보자.
# 여기까지하고 나서 코드 정리를 한번하고 알고리즘을 보강하자.
   




