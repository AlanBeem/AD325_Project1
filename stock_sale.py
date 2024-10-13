from stock_purchase import StockPurchase


class StockSale:
    def __init__(self, stock_symbol: str, quantity: int, sale_price: float|None=None, shares_sold: list[StockPurchase] =[]) -> None:
        self.symbol = stock_symbol
        self.shares = shares_sold
        self.price = sale_price
        self.quantity = quantity

    def __len__(self):
        return len(self.shares)
    
    def __str__(self) -> str:
        out_string_list = [f"---- Stock Sale: {self.symbol} ----"]
        out_string_list.append('Cost        Price')
        for each_share in self.shares:
            out_string_list.append(f"{each_share.cost}        {self.price}")
        out_string_list.append('- - - - - Total - - - - -')
        return '\n'.join(out_string_list)

    def add_sale(self, stock: StockPurchase) -> None:
        self.shares.append(stock)

    def total_cost(self) -> float:
        total = 0
        for each_share in self.shares:
            total += each_share.cost
        return total

    def get_profit(self):
        if self.price is None:
            print(f"self.price == {self.price}")
            raise RuntimeError
        return self.quantity * self.price - self.total_cost()