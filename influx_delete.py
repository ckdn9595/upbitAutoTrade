import influxdb_client, os, time
from influxdb_client import InfluxDBClient
from datetime import datetime

## API 세팅
bucket="KRW"
token = os.environ.get("INFLUXDB_TOKEN")
org = "crypto-trade"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org, timeout=100000)

start = "2004-01-01T00:00:00Z"
stop = "2024-03-18T00:00:00Z"
predicate = '_measurement="KRW-BTC"'

# 삭제 요청 생성
delete_api = client.delete_api()
try:
    delete_api.delete(start, stop, predicate, bucket, org)
except Exception as e:
    print(f"Error writing to InfluxDB: {e}")
# 클라이언트 종료
client.close() 