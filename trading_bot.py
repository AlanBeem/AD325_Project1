import time
from stock_ledger import StockLedger
# from stock_sale import StockSale

class TradingBot:  # TradingFirm ?
    """Has methods to determine behavior as a function of inputs, but these behaviors occur through execution of public methods, so this also works for tabulation of a given sequence of buy and sell operations.
    \nbuy_setting:\n\n1: buy\n\n2: buyRandom\n\n3: buyOptimal\n\nsell_setting\n\n1: sell\n\n2: sellRandom\n\n3: sellOptimal(1)\n\n4: sellOptimal(2)\n\n5: sellOptimal(3)"""
    def __init__(self, initial_balance: float, operating_cost: float =0, buy_setting: int =1, sell_setting: int =1) -> None:  # TODO Bot shouldn't have balance, or operating cost, Firm should though
        self.stock_ledger = StockLedger()
        self.stock_sales_list = []
        self.balance = initial_balance
        self.balance_over_transactions = [initial_balance]
        self.profit_per_sell = []
        self.buy_setting = buy_setting
        self.sell_setting = sell_setting
        #
        self.sell_times = []
        self.buy_times = []
        self.per_share_sell_times = dict()
        self.per_share_buy_times = dict()

    def string_to_trading_bot(self, input_str: str) -> None:  # 
        input_lines = input_str.split('\n')
        for each_line in input_lines:  # O(N=len(input_lines))
            # plot_x.append(len(plot_x))  # on list, O(1)
            # plot_y.append(trading_bot.report_profit())
            each_split_line = each_line.split()  # splits on spaces
            if each_line.count('Display') == 0:
                price_string = each_split_line[-1].strip('.$')
            if each_split_line[0] == 'Buy':
                self.buy(each_split_line[4], int(each_split_line[1]), float(price_string))
            elif each_split_line[0] == 'Sell':
                self.sell(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(1) * O(num shares)

    def buy(self, stock_symbol: str, quantity: int, price: float) -> None:
        buy_time_start = time.time()
        if self.buy_setting == 1:
            self.stock_ledger.buy(stock_symbol, quantity, price)
        elif self.buy_setting == 2:
            self.stock_ledger.buyRandom(stock_symbol, quantity, price)
        elif self.buy_setting == 3:
            self.stock_ledger.buyOptimal(stock_symbol, quantity, price)
        elif self.buy_setting == 4:
            pass
        buy_time_end = time.time()
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)
        self.buy_times.append(buy_time_end - buy_time_start)
        if per_share_time := self.buy_times[-1] / quantity in self.per_share_buy_times:
            # average
            previous_sum = self.per_share_buy_times.get(price) * (len(self.buy_times) - 1)
            self.per_share_buy_times.update((previous_sum + per_share_time) / len(self.buy_times))
        else:
            self.per_share_buy_times.update({price : per_share_time})
    
    def sell(self, stock_symbol: str, quantity: int, price: float) -> None:
        sell_time_start = time.time()
        if self.sell_setting == 1:
            self.stock_sales_list.append(self.stock_ledger.sell(stock_symbol, quantity, price))
        elif self.sell_setting == 2:
            self.stock_sales_list.append(self.stock_ledger.sellRandom(stock_symbol, quantity, price))
        elif self.sell_setting == 3:
            self.stock_sales_list.append(self.stock_ledger.sellOptimal(stock_symbol, quantity, price))
        elif self.sell_setting == 4:
            self.stock_sales_list.append(self.stock_ledger.sellOptimal(stock_symbol, quantity, price))
        sell_time_end = time.time()
        self.stock_sales_list[-1].price = price
        self.balance += quantity * price
        self.profit_per_sell.append(self.report_last_profit())
        self.sell_times.append(sell_time_end - sell_time_start)
        if per_share_time := self.sell_times[-1] / quantity in self.per_shares_sell_times:
            # average
            previous_sum = self.per_share_sell_times.get(price) * (len(self.sell_times) - 1)
            self.per_share_sell_times.update((previous_sum + per_share_time) / len(self.sell_times))
        else:
            self.per_share_sell_times.update({price : per_share_time})
    
    # $ report methods:

    def profit(self) -> float:
        return sum([stock_sale.get_profit() for stock_sale in self.stock_sales_list])
    
    def last_profit(self):
        if len(self.stock_sales_list) > 0:
            return self.stock_sales_list[-1].get_profit()
        else:
            return 0

    def accumulated_profit(self) -> list[float]:
        accumulated_profits = [0]
        while len(accumulated_profits) < len(self.profit_per_sell):
            current_accumulation = 0
            for ap_i in range(len(accumulated_profits)):
                current_accumulation += self.profit_per_sell[ap_i]
            accumulated_profits.append(current_accumulation)
        return accumulated_profits
    
    def revenue(self) -> float:
        return sum([each_sale.quantity * len(each_sale.shares) for each_sale in self.stock_sales_list])
    
    def last_revenue(self) -> float:
        return self.stock_sales_list[-1].quantity * self.stock_sales_list[-1].price

    # complexity report methods:
    
    def report_total_times(self) -> tuple[float, float]:  # buy time, sell time
        return sum(self.buy_times), sum(self.sell_times)  # color-mix over strategies (Cartesian) (try with .imshow)

    # could do: # class data object (for normalization) (and would add to init.)

    def report_buy_time_per_dollar(self) -> None:  # price forms a binary relation from bought to sold
        # print("For the shares sold, per dollar of profit:")  # really, would want to display this averaged over a bunch of strings
        # print(f"Buy: ")
        average_buy_time = 0  # in theory, bot could have not purchased shares not included in sales, up to a point (then, you could sell in the order purchased and make the same returns)
        buy_n = 0
        for price in self.per_share_sell_times.keys():
            buy_n += 1
            average_buy_time = ((buy_n - 1) * average_buy_time + self.per_share_buy_times.get(price)) / buy_n
        return average_buy_time / self.accumulated_profit()
    
    def report_sell_time_per_dollar(self) -> None:
        average_sell_time = 0
        sell_n = 0
        for each_time in [self.per_share_buy_times.get(key_i) for key_i in list(self.per_share_buy_times)]:
            sell_n += 1
            average_sell_time = ((sell_n - 1) * average_sell_time + each_time) / sell_n
        return average_sell_time / self.accumulated_profit()
    
