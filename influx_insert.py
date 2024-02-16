import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pyupbit
from datetime import datetime, timezone
import json

## API 세팅
bucket="crypto"
token = os.environ.get("INFLUXDB_TOKEN")
org = "upbit-trade"
url = "http://3.36.115.87:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

### Dataframe to json
# df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1440, to="202101020000")
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1, to="202401010005")
## 이코드 확인 필요 컬럼명이 제대로 바꿔지나?
df.reset_index(inplace=True)
df.rename(columns={'index': 'timestamp'}, inplace=True)

# 타임스탬프 형식을 ISO8601로 변환
#df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat())
df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat())

# DataFrame을 JSON 형식으로 변환, 날짜 포맷을 ISO 형식으로 유지
json_data = df.to_json(orient='records', date_format='iso')

# JSON 데이터를 파싱
data_points = json.loads(json_data)

for point in data_points:
    # 각 데이터 포인트를 InfluxDB 포인트 객체로 변환
    influx_point = Point("crypto-trade") \
        .tag("currency_pair", "KRW-BTC") \
        .tag("unit", "MIN") \
        .tag("exchange", "upbit") \
        .field("open", point["open"]) \
        .field("high", point["high"]) \
        .field("low", point["low"]) \
        .field("close", point["close"]) \
        .field("volume", point["volume"]) \
        .field("value", point["value"]) \
        .time('2023-01-05T18:04:56.865943')
        #.time(point["timestamp"]) \
        ## 볼린저 밴드 정보를 위한 이평선도 같이 들어갈 수 있도록 해야해

    try:
        write_api.write(bucket=bucket, org=org, record=influx_point)
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")
