import pyupbit
from pyupbit import WebSocketManager
import logging
import json
from datetime import timezone

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

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1, to="202101010005")
## 이코드 확인 필요 컬럼명이 제대로 바꿔지나?
df.reset_index(inplace=True)
df.rename(columns={'index': 'timestamp'}, inplace=True)

# 타임스탬프 형식을 ISO8601로 변환
#df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat())
df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat().utcNow())
# DataFrame을 JSON 형식으로 변환, 날짜 포맷을 ISO 형식으로 유지
json_data = df.to_json(orient='records', date_format='iso')
print(json_data)
# JSON 데이터를 파싱
data_points = json.loads(json_data)
print(data_points)
# df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=1440, to="202101020000")
# df.reset_index(inplace=True)
# df.rename(columns={'index': 'timestamp'}, inplace=True)
# df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat())
# json_data = df.to_json(orient='records', date_format='iso')
# data_points = json.loads(json_data)

# logging.info(data_points)
