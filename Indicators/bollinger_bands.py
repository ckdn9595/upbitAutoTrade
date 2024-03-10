import pandas as pd
from pandas import Timestamp

class bollinger:
    window = 19
    # data는 기간별 종가 리스트
    def _init__(self):
        self=self
        
    def calc_bolinger_day(self, days: pd, now_price, now_dateTime):
        time_list = days.index.tolist()
        days['ma20'] = days['close'].rolling(self.window).mean()
        last_day = days.loc[time_list[len(time_list)-1]] # 마지막 정보 (하루 전날)
        ma20 = (last_day['ma20'] * 19 + now_price) / 20  # 현재가추가한 ma20
        new_row = pd.DataFrame({
            "close": now_price, "ma20": ma20, 'open': -1, 'high': -1, 'low': -1, 'volume': -1, 'value': -1
        }, index=[0])
        #현재 정보 추가
        days = pd.concat([days, new_row], ignore_index=True)
        #볼린저 상부하부
        days['upper'] = days['ma20'] + 2 * days['close'].rolling(self.window).std()
        days['lower'] = days['ma20'] - 2 * days['close'].rolling(self.window).std()
    
    def calc_bolinger_hour(self, hours: pd):
        # 추가된 마지막 20번째의 이평선
        hours["ma20"] = hours['close'].rolling(self.window).mean()
        # 볼린저 상부하부점
        hours['upper'] = hours['ma20'] + 2 * \
            hours['close'].rolling(self.window).std()
        hours['lower'] = hours['ma20'] - 2 * \
            hours['close'].rolling(self.window).std()
        
    def calc_bolinger_min(self, mins: pd, now_price, now_dateTime):
        # 현재 정보 추가
        mins.loc[len(mins)] = {"_time": now_dateTime, "close": now_price}
        # 추가된 마지막 20번째의 이평선
        mins["ma20"] = mins['close'].rolling(self.window).mean()
        # 볼린저 상부하부점
        mins['upper'] = mins['ma20'] + 2 * \
            mins['close'].rolling(self.window).std()
        mins['lower'] = mins['ma20'] - 2 * \
            mins['close'].rolling(self.window).std()

    