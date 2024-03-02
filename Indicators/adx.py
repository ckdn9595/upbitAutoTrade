import pandas as pd
import numpy as np


class adx:
    window = 14

    def __init__(self):
        self = self

    def calc_adx(self, days, now_price):
        days.loc[len(days)] = {"high": now_price, "low": now_price}
        self.calc_pdm(days)
        self.calc_mdm(days)
        self.calc_tr(days)
        days['pdi'] = (days['pdm14'] / days['tr14']) * 100
        days['mdi'] = (days['mdm14'] / days['tr14']) * 100
        days['dx'] = (np.abs(days['pdi'] - days['mdi']) /
                      (days['pdi'] + days['mdi'])) * 100
        days['adx14'] = days['dx'].rolling(self.window).mean() #다짜긴 했는데 날짜가 적어서 안되는듯 검증은 필요하다.
        print(days[['_time', 'high', 'low','pdm','mdm','pdm14','mdm14','pdi','mdi','dx', 'adx14']])

    def calc_pdm(self, days):
        days['pdm'] = (days['high'] - days['high'].shift(1)).clip(lower=0)
        days["pdm14"] = days['pdm'].rolling(self.window).mean()

    def calc_mdm(self, days):
        days['mdm'] = (days['low'].shift(1) - days['low']).clip(lower=0)
        days["mdm14"] = days['mdm'].rolling(self.window).mean()
        
    def calc_tr(self, days):
        days['tr'] = np.maximum.reduce([
            days['high'] - days['low'],
            np.abs(days['high'] - days['close'].shift(1)),
            np.abs(days['low'] - days['close'].shift(1))
        ])
        days['tr14'] = days['tr'].rolling(self.window).mean()
