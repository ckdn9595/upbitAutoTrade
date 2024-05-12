class buysell:
    def __init__(self, start_cash):
        self.fee = 0.005

        self.start_cash = start_cash  # 시작 자산
        self.current_cash = start_cash  # 현재 자산
        self.highest_cash = start_cash  # 자산 최고점
        self.lowest_cash = start_cash  # 자산 최저점
        
        self.buy_price = 0 # 평균 매수가, 0이면 보유하지 않은 상태, 값이 있으면 매수 상태
        self.holding_numbers = 0 # 코인 보유 개수
        
        self.accumulated_ror = 1  # 누적 수익률

        self.trade_count = 0  # 거래횟수 매수-매도 까지 이루어졌을 때 하나의 거래라고 본다.
        self.win_count = 0  # 승리횟수

    # 현재는 분할매수 안됨
    # price : 주문가
    def buy(self, price):
        if (self.current_cash is 0):
            print("잔액 부족") # 추후 최소 주문금액으로 0 값을 변경해야함.
            return
        order_quantity = self.current_cash/price  # 매수 수량
        oq_exclude_fee = order_quantity * (1 - self.fee/100) # 수수료 제외 매수 수량
        
        self.buy_price = (self.holding_numbers *
                          self.buy_price + oq_exclude_fee * price) / (self.holding_numbers + oq_exclude_fee)
        self.holding_numbers += oq_exclude_fee # 코인 보유개수 추가
        self.current_cash = 0
    #현재는 분할매도 안됨
    def sell(self, price):
        if(self.holding_numbers is 0):
            print("보유 코인 없음")
            return
        
        ror = 1 + (price - self.buy_price) / self.buy_price
         # 승리 횟수 계산
        self.win_count += 1 if ror > 1 else 0
        self.trade_count += 1
        # 누적 수익률 계산
        self.accumulated_ror *= ror
        # 수수료 제외 매도 금액
        self.current_cash = self.holding_numbers * price * (1 - self.fee/100)
        # 자산 최고점 갱신
        self.highest_cash = max(self.highest_cash, self.current_cash)
        # 자산 최저점 갱신
        self.lowest_cash = min(self.lowest_cash, self.current_cash)
        
        self.holding_numbers = 0

    def print (self):
        print(f"시작 자산, {self.start_cash}!") # 시작 자산
        print(f"현재 자산, {self.current_cash}!")
        print(f"자산 최고점, {self.highest_cash}!")
        print(f"자산 최저점, {self.lowest_cash}!")
        print(f"누적 수익률, {self.accumulated_ror}!")
        print(f"총거래 횟수, {self.trade_count}!")
        print(f"승리 횟수, {self.win_count}!")
        
