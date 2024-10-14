from stock_ledger import StockLedger
# from stock_sale import StockSale

class TradingBot:  # TradingFirm ?
    """Has methods to determine behavior as a function of inputs, but these
    behaviors occur through execution of public methods, so this also works
    for tabulation of a given sequence of buy and sell operations."""
    def __init__(self, initial_balance: float, operating_cost: float =0) -> None:  # TODO Bot shouldn't have balance, or operating cost, Firm should though
        self.stock_ledger = StockLedger()
        self.stock_sales_list = []
        self.balance = initial_balance
        self.balance_over_transactions = [initial_balance]
        self.profit_per_sell = []

    def buy(self, stock_symbol: str, quantity: int, price: float) -> None:
        self.stock_ledger.buy(stock_symbol, quantity, price)
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)
    
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

    def report_profit(self):
        return sum([stock_sale.get_profit() for stock_sale in self.stock_sales_list])
    
    def report_last_profit(self):
        if len(self.stock_sales_list) > 0:
            # return 10  # displays as 10, so it's getting to here.
            return self.stock_sales_list[-1].get_profit()
        else:
            return 0

