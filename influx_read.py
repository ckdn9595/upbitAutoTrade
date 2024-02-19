from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

bucket="KRW"
token = os.environ.get("INFLUXDB_TOKEN")
org = "crypto-trade"
url = "http://localhost:8086"

with InfluxDBClient(url=url, token=token, org=org) as client:

    """
    Query: using Table structure
    """
    tables = client.query_api().query(f'from(bucket:"{bucket}") |> range(start: -1d) |> filter(fn: (r) => r["_measurement"] == "KRW-BTC")')

    """
    Serialize to JSON
    """
    output = tables.to_json(indent=5) #indent=5는 JSON 출력 포맷을 보기 좋게 들여쓰기하기 위한 옵션
    print(output)