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
        self.sell_times = []
        self.buy_times = []

    def buy(self, stock_symbol: str, quantity: int, price: float) -> None:
        buy_time_start = time.time()
        if self.buy_setting == 1:
            pass
        elif self.buy_setting == 2:
            pass
        elif self.buy_setting == 3:
            pass
        elif self.buy_setting == 4:
            pass
    
    # sell:
    # def buy(self, stock_symbol: str, quantity: int, price: float) -> None:
    #     buy_time_start = time.time()
    #     if self.buy_setting == 1:
    #         pass
    #     elif self.buy_setting == 2:
    #         pass
    #     elif self.buy_setting == 3:
    #         pass
    #     elif self.buy_setting == 4:
    #         pass

    def buy(self, stock_symbol: str, quantity: int, price: float) -> None:
        self.stock_ledger.buy(stock_symbol, quantity, price)
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)
    
    def buyRandom(self, stock_symbol: str, quantity: int, price: float) -> None:
        self.stock_ledger.buyRandom(stock_symbol, quantity, price)
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)
    
    def buyOptimal(self, stock_symbol: str, quantity: int, price: float) -> None:
        self.stock_ledger.buyOptimal(stock_symbol, quantity, price)
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)    
    
# TODO Make all sell methods the same one, switch behavior by settings

    def sell(self, stock_symbol: str, quantity: int, price: float) -> None:  # TODO add argument allowing partially filling sales (oh, then you'd need to be able to put them back, if the sale did not complete (should add them to some segments of same price) (increasing the complexity, could use a deck of mixed stock symbols)
        # TODO have these pass in a StockSale object to be filled by the ledger (After bug is fixed, with design)
        self.stock_sales_list.append(self.stock_ledger.sell(stock_symbol, quantity))
        if self.stock_sales_list[-1] is None:
            self.stock_sales_list.remove(None)
        else:
            self.stock_sales_list[-1].price = price
            self.balance += quantity * price
            self.profit_per_sell.append(self.report_last_profit())
    
    def sellRandom(self, stock_symbol: str, quantity: int, price: float) -> None:
        self.stock_sales_list.append(self.stock_ledger.sellRandom(stock_symbol, quantity))
        self.stock_sales_list[-1].price = price
        self.balance += quantity * price
        self.profit_per_sell.append(self.report_last_profit())
    
    def sellOptimal(self, stock_symbol: str, quantity: int, price: float, optimal_selection_int: int=1) -> None:
        self.stock_sales_list.append(self.stock_ledger.sellOptimal(stock_symbol, quantity, optimal_selection_int))
        self.stock_sales_list[-1].price = price
        self.balance += quantity * price
        self.profit_per_sell.append(self.report_last_profit())

    def report_profit(self) -> float:
        return sum([stock_sale.get_profit() for stock_sale in self.stock_sales_list])
    
    def report_accumulated_profit(self) -> list[float]:
        accumulated_profits = [0]
        while len(accumulated_profits) < len(self.profit_per_sell):
            current_accumulation = 0
            for ap_i in range(len(accumulated_profits)):
                current_accumulation += self.profit_per_sell[ap_i]
            accumulated_profits.append(current_accumulation)
        return accumulated_profits
    
    def report_revenue(self) -> float:
        return sum([each_sale.quantity * len(each_sale.shares) for each_sale in self.stock_sales_list])
    
    def report_last_profit(self):
        if len(self.stock_sales_list) > 0:
            # return 10  # displays as 10, so it's getting to here.
            return self.stock_sales_list[-1].get_profit()
        else:
            return 0
    
    def report_total_times(self) -> tuple[float, float]:  # buy time, sell time
        return sum(self.buy_times), sum(self.sell_times)


def string_to_trading_bot(input_str: str, trading_bot: TradingBot, strategy_selection_int: int=1) -> tuple[list[int], list[float]]:  # O(1) or O(f(N))
    """strategy_selection_int:\n\n1: sell\n\n2: sellRandom\n\n3: sellOptimal() (sell lowest cost shares first)\n\n4: sellOptimal(optimal_selection_int=2) (sell below the median (per round of the deque))"""
    input_lines = input_str.split('\n')  #                       # O(f(N))
    plot_x = []
    plot_y = []
    for each_line in input_lines:  # O(N=len(input_lines))
        # plot_x.append(len(plot_x))  # on list, O(1)
        # plot_y.append(trading_bot.report_profit())
        each_split_line = each_line.split()  # splits on spaces
        if each_line.count('Display') == 0:
            price_string = each_split_line[-1].strip('.$')
        if each_split_line[0] == 'Buy':
            trading_bot.buy(each_split_line[4], int(each_split_line[1]), float(price_string))
        elif each_split_line[0] == 'Sell':
            if strategy_selection_int == 1:
                trading_bot.sell(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(1) * O(num shares)
            elif strategy_selection_int == 2:
                trading_bot.sellRandom(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(len(entry)) * O(num shares)
            elif strategy_selection_int == 3:
                trading_bot.sellOptimal(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(f(N))
            elif strategy_selection_int == 4:
                trading_bot.sellOptimal(each_split_line[4], int(each_split_line[1]), float(price_string), 2)  # O(f(N))
            plot_x.append(len(plot_x))  # O(N=len(list))  # track sales
            plot_y.append(trading_bot.report_last_profit())
    return plot_x, plot_y


