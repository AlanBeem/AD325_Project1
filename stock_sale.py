from stock_purchase import StockPurchase


class StockSale:
    def __init__(self, stock_symbol: str, shares_sold: list[StockPurchase], sale_price: float) -> None:
        self.symbol = stock_symbol
        self.shares = shares_sold
        self.price = sale_price

    def get_quantity(self):
        return len(self.shares)

    def get_profit_loss(self):
        return self.get_quantity() * self.price - sum([share.cost for share in self.shares])