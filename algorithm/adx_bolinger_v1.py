# v.1.1
# 나의 첫 매수 매도 알고리즘
# ADX와 볼린저밴드만을 활용해서 한다.

# 상태는 3가지가 있다. 
# 상승 판단 매수, 하락 판단 매도, 볼린저에 따른 매수 매도
from enum import Enum
import pandas as pd
from scipy.stats import linregress
import numpy as np

# Status Enum 정의
class BuyorSell(Enum):
    NULL = 0
    BUY = 1
    SELL = 2

class AdxStatus(Enum):
    NULL = 0
    UP = 1
    DOWN = 2
    NONE = 3
    
class Status(Enum):
    NULL = 0
    BULL = 1 #상승장
    BEAR = 2 #하락장
# 사용 예시
#if now_status == Status.BUY:
    #print("Buying mode")
class adx_bollinger:
    now_adx_status = AdxStatus.NULL #adx 상태
    before_status = Status.NULL # 직전 상태를 저장한다. 상승이었는지 하락이었는지
    adx_values = None # adx 모음
    data = None
    now = None
    before = None
    
    #매수 판단 경우
    def buy_sell_algo(self, data):
        self.data = data
        self.now = data.iloc[-1]
        self.before = data.iloc[-2]
        self.adx_values = data.dx14
        return self.state_based_selection() # 선택을 반환한다.
    
    
    # 시뮬레이션 기초 설계를 마치자. (수수료를 적용한 실제 분단위 판정 매수매도 시뮬레이션 돌려보기.)
    def state_based_selection(self):
        pdi = self.now.pdi
        mdi = self.now.mdi
        beforePdi = self.before.pdi
        beforeMdi = self.before.mdi
        adx = self.adx_values.iloc[-1]
        isPlus = pdi > mdi
        higherAdx20 = adx >= 20
        now_adx_status = AdxStatus.UP if adx > self.adx_values.iloc[-2] else AdxStatus.DOWN
        sharp_decline = ((beforePdi - beforeMdi) - (pdi - mdi)) >= 15
        sharp_rise = ((beforeMdi - beforePdi) - (mdi - pdi)) >= 15
        
        #상승 추세
        isBull = isPlus and higherAdx20
        #매수 1 상승 추세 강해짐
        isBuy = isBull and (now_adx_status is AdxStatus.UP)
        #매수 2 골드크로스 예측
        isBuy2 = self.before_status is Status.BEAR and sharp_rise
        #하락 상태
        isBear = not isPlus and higherAdx20
        #매도 1
        isSell = isBear and (now_adx_status is AdxStatus.UP)
        #매도 2 데드크로스 예측
        isSell2 = self.before_status is Status.BULL and sharp_decline
        #볼린저 매수매도 조건
        isBolinger = not higherAdx20 and abs(pdi - mdi) < 20
        #상태 기록
        if (isBull):
            self.before_status = Status.BULL
        elif (isBear):
            self.before_status = Status.BEAR
        #조건에 따른 매수매도상태 종합
        choice = BuyorSell.NULL
        if(isSell or isSell2):
            choice = BuyorSell.SELL
        elif(isBuy or isBuy2):
            choice = BuyorSell.BUY
        elif(isBolinger):
            choice = self.bolinger()
        return choice
    
    def bolinger(self):
        if self.now.close >= self.now.upper:
            return BuyorSell.SELL
        elif self.now.close <= self.now.lower:
            return BuyorSell.BUY
        else:
            return BuyorSell.NULL

# 아래는 선형회귀 방식의 일부분이다. 필요 시 사용한다.
# def judge_trend_regression(column):
#     # 인덱스를 x축 값으로 사용
#     x = np.arange(len(column))
#     slope, intercept, r_value, p_value, std_err = linregress(x, column)

#     if slope > 0:
#         return "상승"
#     elif slope < 0:
#         return "하락"
#     else:
#         return "변동 없음"


# # 결측값을 제거하고 예시 사용 (선형 회귀 분석을 위해)
# trend = judge_trend_regression(df['A'].dropna())
# print(f"열 'A'의 추세: {trend}")
