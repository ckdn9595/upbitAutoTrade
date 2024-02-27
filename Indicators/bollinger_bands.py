import pandas as pd

class bollinger:
    window = 19
    # data는 기간별 종가 리스트
    def _init__(self):
        self=self
        
    def calc_bolinger_day(self, days: pd, now_price, now_dateTime):
        last_day = days.loc[len(days)-1] # 마지막 정보 (하루 전날)
        ma20 = (last_day['da20'] * 19 + now_price) / 20  # 현재가추가한 ma20
        #현재 정보 추가
        days.loc[len(days)] = {"_time": now_dateTime, "close": now_price, "da20": ma20}
        #볼린저 상부하부점
        days['upper'] = days['da20'] + 2 * days['close'].rolling(self.window).std()
        days['lower'] = days['da20'] - 2 * days['close'].rolling(self.window).std()
        print(days)
    
    def calc_bolinger_hour(self, hours: pd, now_price, now_dateTime):
        
        # 현재 정보 추가
        hours.loc[len(hours)] = {"_time": now_dateTime, "close": now_price}
        # 추가된 마지막 20번째의 이평선
        hours["ma20"] = hours['close'].rolling(self.window).mean()
        # 볼린저 상부하부점
        hours['upper'] = hours['ma20'] + 2 * \
            hours['close'].rolling(self.window).std()
        hours['lower'] = hours['ma20'] - 2 * \
            hours['close'].rolling(self.window).std()
        print(hours)
        
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
        print(mins)

    