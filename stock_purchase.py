class StockPurchase:
    def __init__(self, stock_symbol, cost_per_share) -> None:  # required
        self.symbol = stock_symbol
        self.cost = cost_per_share
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.symbol == other.symbol and self.cost == other.cost
        return False
    
    def __str__(self) -> str:
        return f"{self.symbol}: ${self.cost}"