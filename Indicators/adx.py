import pandas as pd
import numpy as np


class adx:
    window = 14

    def __init__(self):
        self = self

    def calc_adx(self, days):
        self.calc_dm(days)
        self.calc_tr(days)
        days['pdi'] = (days['pdm14'] / days['tr14']) * 100
        days['mdi'] = (days['mdm14'] / days['tr14']) * 100
        days['dx'] = (np.abs(days['pdi'] - days['mdi']) /
                      (days['pdi'] + days['mdi'])) * 100
        self.calc_smma(days, 'dx')
        return days
        #days['adx14'] = days['dx'].rolling(self.window).mean() #다짜긴 했는데 날짜가 적어서 안되는듯 검증은 필요하다.
        

    def calc_dm(self, days):
        days['pdm'] = (days['high'] - days['high'].shift(1)).clip(lower=0)
        days['mdm'] = (days['low'].shift(1) - days['low']).clip(lower=0)
        days['pdm'] = np.where((days['pdm'] > 0) & (days['mdm'] > 0), np.where(days['pdm'] < days['mdm'], 0, days['pdm']), days['pdm'])
        days['mdm'] = np.where((days['pdm'] > 0) & (days['mdm'] > 0), np.where(days['mdm'] < days['pdm'], 0, days['mdm']), days['mdm'])
        self.calc_smma(days, 'pdm')
        self.calc_smma(days, 'mdm')
        # days["pdm14"] = days['pdm'].rolling(self.window).mean()
        # days["mdm14"] = days['mdm'].rolling(self.window).mean()
        
       

    def calc_tr(self, days):
        days['tr'] = pd.concat([
            days['high'] - days['low'],
            abs(days['high'] - days['close'].shift(1)),
            abs(days['low'] - days['close'].shift(1))
        ], axis=1).max(axis=1)
        self.calc_smma(days, 'tr')
        
    def find_iloc(self, data, column_name):
        return data[column_name].first_valid_index()
    
    def calc_smma(self, data, type):
        iloc_num = self.find_iloc(data, f'{type}') + 13
        # pdm과 mdm의 초기 14일 SMA 계산
        initial_sma = data[f'{type}'].rolling(
            window=self.window).mean().iloc[iloc_num]

        # 초기 SMA 값을 설정
        data[f'{type}14'] = np.nan
        data.at[iloc_num, f'{type}14'] = initial_sma

        # 이후 값들에 대해 SMMA 계산
        for i in range(iloc_num+1, len(data)):
            data.loc[i, f'{type}14'] = (
                data.loc[i-1, f'{type}14'] * (self.window - 1) + data.loc[i, f'{type}']) / self.window
