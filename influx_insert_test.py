import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
#import pandas as pd
import pyupbit
from datetime import datetime
import json

## API 세팅
bucket="krw-btc"
token = os.environ.get("INFLUXDB_TOKEN")
org = "upbit-trade"
url = "http://3.36.115.87:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="upbit-trade", record=point)
  time.sleep(1)