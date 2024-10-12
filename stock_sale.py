from stock_purchase import StockPurchase


class StockSale:
    def __init__(self, stock_symbol: str, quantity: int, sale_price: float, shares_sold: list[StockPurchase] =[]) -> None:
        self.symbol = stock_symbol
        self.shares = shares_sold
        self.price = sale_price
        self.quantity = quantity

    def __len__(self):
        return len(self.shares)

    def add_sale(self, stock: StockPurchase) -> None:
        self.shares.append(stock)

    def get_profit(self):
        return len(self.shares) * self.price - sum([share.cost for share in self.shares])