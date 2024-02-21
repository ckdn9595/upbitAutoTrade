import pyupbit
from pyupbit import WebSocketManager
import logging

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


#Quotation API
#Websocker connection 5times/sec 100times/min
#종목, 캔들, 체결, 티커, 호가 API 10times/sec 600times/min
# 캔들 : 주식이나 다른 금융 상품의 가격 움직임을 시각적으로 표현한 것입니다. 
# 각 캔들은 일정 기간 동안의 시가(시작 가격), 종가(마감 가격), 고가(최고 가격), 저가(최저 가격) 정보를 담고 있습니다. 
# 티커 : 주식이나 금융 상품의 거래 정보를 실시간으로 보여주는 알파벳이나 숫자의 조합입니다. 
# 티커는 주식의 가격 변동, 거래량 등의 정보를 빠르게 전달하기 위해 사용


#get_tickers 함수는 업비트가 지원하는 모든 암호화폐 목록을 얻어옵니다.
#print(pyupbit.get_tickers())

#(fiat)에 매매가 가능한 목록만 얻어올 수 있습니다. KRW/BTC/USDT 시장을 조회
#print(pyupbit.get_tickers(fiat="KRW"))

#get_current_price 함수는 암호화폐의 현재가를 얻어옵니다. 함수로 티커를 넣어줘야 합니다.
print(pyupbit.get_current_price("KRW-BTC"))

#리스트에 여러 개의 티커를 입력해 한 번에 현재가를 조회,  get_current_price 함수는 최대 100개의 암호화폐를 조회 100회 이상일 경우 반복 조회
#print(pyupbit.get_current_price(["KRW-BTC", "KRW-XRP"]))

#get_ohlcv 함수는 고가/시가/저가/종가/거래량을 DataFrame으로 반환
#count 제거시 default는 200이고, 이는 한 요청의 최대치임.
#따라서 200이상의 데이터를 요청 시 0.1(defalt)주기로 데이터를 수집
#다른 API와 함께 사용하면 period를 늘려야함. 최대 요청량을 초과하기 때문
#df = pyupbit.get_ohlcv("KRW-BTC", count=2)
#df = pyupbit.get_ohlcv("KRW-BTC", count=600, period=1)
#print(df)

#interval 파라미터는 조회단위를 지정합니다. 파라미터에는 다음 값을 지정할 수 있습니다.
#day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month
#print(pyupbit.get_ohlcv("KRW-BTC", interval="minute1"))
# df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=2243580)
# print(df.tail())
#종료 일자를 지정하고 싶으면 to를 사용
#print(pyupbit.get_ohlcv("KRW-BTC",interval="minute1" , to="202402091700"))

#매수/매도 호가
#print(pyupbit.get_orderbook(ticker="KRW-BTC"))
#print(pyupbit.get_orderbook(ticker=["KRW-BTC", "KRW-XRP"]))


######### Exchange API
#주문은 초당 8회, 분당 200회 / 주문 외 요청은 초당 30회, 분당 900회 사용 가능
access = "yP4VFpEg9oZpLUQv91sekaljOxZgkAPybCcTxOnh"          # 본인 값으로 변경
secret = "0Jmi6p8JvKjScD30DZSZK14nsqxZHMfJozH4Vp6d"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

#잔고 조회
#get_balance 메서드는 입력받은 티커의 보유 수량 정보를 조회합니다.
#print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
#print(upbit.get_balance("KRW"))   
#print(upbit.get_balances()) #보유중인 모든 티커 정보 조회

# 매도 지정가
# print(upbit.sell_limit_order("KRW-XRP", 600, 20)) #원화 시장에 리플을 600원에 20개 매도
# 매수 지정가
# print(upbit.buy_limit_order("KRW-XRP", 613, 10))  #리플을 613원에 10개 매수

#주문 정보가 딕셔너리로 반환됩니다. uuid는 주문에 대한 고윳값으로 이를 사용해 추후 주문을 취소하거나 정정할 수 있음
# {'uuid': '0bcf0916-a7f5-49ed-80a9-a45e9e190cd3',
#  'side': ('ask' 'bid'), 매도/매수 
#  'ord_type': 'limit',
#  'price': '600.0',
#  'state': 'wait',
#  'market': 'KRW-XRP',
#  'created_at': '2021-03-21T15:24:11+09:00',
#  'volume': '20.0',
#  'remaining_volume': '20.0',
#  'reserved_fee': '0.0',
#  'remaining_fee': '0.0',
#  'paid_fee': '0.0',
#  'locked': '20.0',
#  'executed_volume': '0.0',
#  'trades_count': 0}


#시장가 매수/매도 주문
#시장가 매수는 최우선 매도호가에 즉시 매수합니다. 
#buy_market_order 메서드로 티커와 매수 금액만을 입력
# 매수 금액은 수수료를 제외한 금액
# 다음 예제에서 주문한 10000원은 수수료가 제외된 금액
# 수수료가 0.05%라면 수수료를 포함한 10005원의 현금을 보유하고 있어야 함.

# 시장가 매수
# print(upbit.buy_market_order("KRW-XRP", 10000))
# 시장가 매도
# print(upbit.sell_market_order("KRW-XRP", 30)) #리플 30개를 시장가 매도, 매도대금이 총 10000원이라면 수수료를 제외한 금액이 입금


#미체결 주문 조회
#upbit.get_order("KRW-LTC")

#state 파라미터를 사용하면 완료된 주문들을 조회
#print(upbit.get_order("KRW-LTC", state="done"))

#uuid를 사용해서 특정 주문을 상세 조회, uuid를 사용하면 다른 파라미터는 무시
#order = upbit.get_order('50e184b3-9b4f-4bb0-9c03-30318e3ff10a')
#print(order)

#매수/매도 주문 취소
#print(upbit.cancel_order('50e184b3-9b4f-4bb0-9c03-30318e3ff10a'))

    
    
# if __name__ == "__main__":
#     try:
#         logging.info("웹소켓 연결 시도 중...")
#         wm = WebSocketManager("ticker", ["KRW-BTC"])

#         for i in range(10):
#             data = wm.get()
#             if data:
#                 logging.info(f"수신된 데이터: {data}")
#             else:
#                 logging.debug("데이터 수신 대기중...")
#     except Exception as e:
#         logging.error(f"웹소켓 연결 또는 데이터 수신 중 오류 발생: {e}")
#     finally:
#         wm.terminate()
#         logging.info("웹소켓 연결 종료")