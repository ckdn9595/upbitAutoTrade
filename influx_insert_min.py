import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pyupbit
from datetime import datetime, timezone, time, timedelta
import pandas as pd
import json
import pytz

timezone = pytz.timezone("Asia/Seoul")

## API 세팅
bucket="KRW"
token = os.environ.get("INFLUXDB_TOKEN")
org = "crypto-trade"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

start_str   = "202103070900"
end_str     = "202411020900"
start = datetime.strptime(start_str, "%Y%m%d%H%M%S")
end = datetime.strptime(end_str, "%Y%m%d%H%M%S")
diff = end - start
min_count = int(diff.total_seconds()/ 60) # 분 개수 뽑기 

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1",
                       count=min_count, to=end_str)
df.reset_index(inplace=True)
df.rename(columns={'index': 'timestamp'}, inplace=True)

# 타임스탬프 형식을 ISO8601로 변환

#df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat())
df['timestamp'] = df['timestamp'].apply(lambda x: x.tz_localize(timezone))

# DataFrame을 JSON 형식으로 변환, 날짜 포맷을 ISO 형식으로 유지
json_data = df.to_json(orient='records', date_format='iso')

# JSON 데이터를 파싱
data_points = json.loads(json_data)
    
for point in data_points:
    # 각 데이터 포인트를 InfluxDB 포인트 객체로 변환
    influx_point = Point("KRW-BTC") \
        .tag("exchange", "upbit") \
        .tag("interval", "min") \
        .field("open", point["open"]) \
        .field("high", point["high"]) \
        .field("low", point["low"]) \
        .field("close", point["close"]) \
        .field("volume", point["volume"]) \
        .field("value", point["value"]) \
        .time(point["timestamp"]) \
        ## 볼린저 밴드 정보를 위한 이평선도 같이 들어갈 수 있도록 해야해

    try:
        write_api.write(bucket=bucket, org=org, record=influx_point)
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")


