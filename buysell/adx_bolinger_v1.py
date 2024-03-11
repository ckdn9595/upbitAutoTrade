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
class Status(Enum):
    NULL = 0
    BUY = 1
    SELL = 2

class AdxStatus(Enum):
    NULL = 0
    UP = 1
    DOWN = 2
    NONE = 3
# 사용 예시
#if now_status == Status.BUY:
    #print("Buying mode")
class buysell:
    now_status = Status.NULL
    now_adx_status = AdxStatus.NULL
    pdi = None
    mdi = None
    adx = None
    adx_values = None
    data = None
    now = None
    
    #매수 판단 경우
    def buy_sell_algo(self, data):
        self.data = data
        self.now = data.iloc[-1]
        self.pdi = self.now.pdi
        self.mdi = self.now.mdi
        self.adx_values = data.dx14
        self.adx = self.adx_values.iloc[-1]
        self.now_adx_status = self.adx_values.iloc[-1] > self.adx_values.iloc[-2] if AdxStatus.UP else AdxStatus.DOWN
    
    #TODO : 내일은 정리한 상태를 바탕으로 3가지 상태로 판단을 완료한 뒤
    # 시뮬레이션 기초 설계를 마치자. (수수료를 적용한 실제 분단위 판정 매수매도 시뮬레이션 돌려보기.)
    
    def bolinger(self):
        if self.now.close >= self.now.upper:
            return Status.SELL
        elif self.now.close <= self.now.lower:
            return Status.BUY
        else:
            return Status.NULL

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
