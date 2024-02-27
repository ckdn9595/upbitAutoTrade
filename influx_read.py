from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from datetime import datetime, timezone, time, timedelta
import pytz


class readInfluxData:

    def __init__(self):
        self.bucket = "KRW"
        self.token = os.environ.get("INFLUXDB_TOKEN")
        self.org = "crypto-trade"
        self.url = "http://localhost:8086"

    # 날짜 기간 설정 + 조인
    def read_with_range_join(self, measure_name, start_date, end_date):
        close_query = (
            f'from(bucket:"{self.bucket}")'
            f' |> range(start:{start_date}, stop:{end_date})'
            f' |> filter(fn: (r) => r["_measurement"] == "{measure_name}")'
            f' |> filter(fn: (r) => (r["_field"] == "close"))'
            f' |> keep(columns: ["_time", "_value", "_field"])'
        )
        volume_query = (
            f'from(bucket:"{self.bucket}")'
            f' |> range(start:{start_date}, stop:{end_date})'
            f' |> filter(fn: (r) => r["_measurement"] == "{measure_name}")'
            f' |> filter(fn: (r) => (r["_field"] == "volume"))'
            f' |> keep(columns: ["_time", "_value", "_field"])'
        )
        join = (
            'join('
            '    tables: {'
            f'        close: {close_query}, volume: {volume_query}'
            '        },'
            '    on: ["_time"])'
            '|> map(fn: (r) => ({_time: r._time,close: r._value_close,volume: r._value_volume}))'
        )
        return self.call_InfluxDBClient(join)

    # 날짜 기간 설정
    def read_with_range_pivot(self, measure_name, start_date, end_date):
        query = (
            f'from(bucket:"{self.bucket}")'
            f' |> range(start:{start_date}, stop:{end_date})'
            f' |> filter(fn: (r) => r["_measurement"] == "{measure_name}")'
            f' |> filter(fn: (r) => (r["_field"] == "close" or r["_field"] == "volume" or r["_field"] == "da20"))'
            f' |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")'
        )
        return self.call_InfluxDBClient(query)

    # 
    def read_with_period(self, measure_name, period):
        query = (
            f'from(bucket:"{self.bucket}")'
            f' |> range(start:-{period})'
            f' |> filter(fn: (r) => r["_measurement"] == "{measure_name}")'
            f' |> filter(fn: (r) => (r["_field"] == "close" or r["_field"] == "volume" or r["_field"] == "da20"))'
            f' |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")'
        )
        return self.call_InfluxDBClient(query)

    # 지난 N일동안 데이터 불러오기

    def read_last_days(self, measure_name, days):
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:

            tables = client.query_api().query(f'from(bucket:"{self.bucket}") \
                |> range(start: -{days}) \
                |> filter(fn: (r) => r["_measurement"] == "{measure_name}")')

            # indent=5는 JSON 출력 포맷을 보기 좋게 들여쓰기하기 위한 옵션
            output = tables.to_json(indent=5)
            return output

    def call_InfluxDBClient(self, query):
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:

            tables = client.query_api().query(query)
            # indent=5는 JSON 출력 포맷을 보기 좋게 들여쓰기하기 위한 옵션
            output = tables.to_json(indent=5)
            return output
# timezone = pytz.timezone("Asia/Seoul")
# influx_reader = readInfluxData()
# start_str = "2023-12-02 09:00"
# end_str = "2023-12-02 09:05"
# start = datetime.strptime(start_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone).isoformat()
# end = datetime.strptime(end_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone).isoformat()
# json_data = influx_reader.read_with_range_pivot("KRW-BTC", start, end)
# print(json_data)
