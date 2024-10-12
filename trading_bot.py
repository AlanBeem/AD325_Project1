from stock_ledger import StockLedger
from stock_sale import StockSale
# from sell_strategy import SellFunction


class TradingBot:  # TradingFirm ?
    """Has methods to determine behavior as a function of inputs, but these
    behaviors occur through execution of public methods, so this also works
    for tabulation of a given sequence of buy and sell operations."""
    def __init__(self, initial_balance: float, operating_cost: float =0) -> None:
        self.stock_ledger = StockLedger()
        self.stock_sales_list = []
        self.balance = initial_balance
        self.balance_over_transactions = [initial_balance]
        self.profit_per_sell = []
        # self.operating_cost = operating_cost  # must cover this cost from sales of stocks
        # self.debt = 0  # could be deques as well, later (loans, at particular interest rates, look at market of these; gets at connection between financial markets) [good exercise to Monte Carlo a loan repayment schedule and encode as deque movements]
        # self.interest_rate = 0  # (could look at change in interest rate and changes in prices, probably a change in slope of something) (can look up effect of interest rates on stock price dynamics, statics)

    def fill_stock_sale(self, sale_to_fill: StockSale,
                        sell_function,  # : function,
                        fill_portion: int|None =0) -> None:
        ledger_entry = self.stock_ledger.get_entry(sale_to_fill.symbol)
        if ledger_entry is not None:  # O(N)
            # assumes fill_portion is not greater th
            if (sale_to_fill.quantity <= len(ledger_entry) or
                 (fill_portion is not None and fill_portion <= len(ledger_entry))):  # don't fill portions that cannot be fulfilled
                if fill_portion is None:
                    fill_portion = sale_to_fill.quantity - len(sale_to_fill)
                sell_function(self, sale_to_fill, fill_portion)

    def buy(self, stock_symbol: str, quantity: int, price: float) -> None:
        self.stock_ledger.buy(stock_symbol, quantity, price)
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)
    
    def sell(self, stock_symbol: str, quantity: int, price: float, sell_function, fill_portion: int|None =None) -> None:
        self.stock_sales_list.append(StockSale(stock_symbol, quantity, price))
        self.fill_stock_sale(self.stock_sales_list[-1], sell_function, fill_portion)  # O(f(N))
        self.balance += quantity * price
        self.balance_over_transactions.append(self.balance)
        self.profit_per_sell.append(self.stock_sales_list[-1].get_profit())

    def report_profit(self):
        return sum([stock_sale.get_profit() for stock_sale in self.stock_sales_list])

