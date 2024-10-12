from stock_purchase import StockPurchase
from ledger_entry import LedgerEntry


class StockLedger:
    def __init__(self) -> None:  # required
        self.ledger_entries = []

    def __len__(self):
        return len(self.ledger_entries)
    
    def __getitem__(self, index) -> LedgerEntry:
        return self.ledger_entries[index]
    
    # def __eq__(self, other) -> bool:
    #     eq_bool = False
    #     if len(self) == len(other):
    #         for each_entry in self:
    #             if 
    
    def buy(self, stock_symbol, shares_bought, cost_per_share) -> None:  # required
        if not self.contains(stock_symbol):
            self.ledger_entries.append(LedgerEntry(stock_symbol))
            buy_entry = self.ledger_entries[-1]
        else:
            buy_entry = self.get_entry(stock_symbol)
        for share in range(shares_bought):
            buy_entry.add_purchase(StockPurchase(stock_symbol, cost_per_share))

    def buyOptimal(self, stock_symbol: str, shares_to_buy: int) -> None:
        pass

    def sell(self, stock_symbol, shares_sold, price_per_share) -> None:  # required
        sell_entry = self.get_entry(stock_symbol)
        stock_purchase = None
        if sell_entry is None:
            print("sell_entry is None: stock symbol not found")
        else:
            for share in range(shares_sold):
                stock_purchase = sell_entry.remove_purchase()
        return stock_purchase
    
    def sellOptimal(self, stock_symbol: str, shares_to_sell: int) -> None:
        pass

    def display_ledger(self) -> None:  # required
        print("----  Stock Ledger  ----")
        for each_entry in self.ledger_entries:
            each_entry.display_entry()

    def contains(self, stock_symbol) -> bool:  # required
        for each_entry in self.ledger_entries:
            if each_entry.symbol == stock_symbol:
                return True
        return False

    def get_entry(self, stock_symbol: str) -> LedgerEntry:  # required
        for each_entry in self.ledger_entries:
            if each_entry.symbol == stock_symbol:
                return each_entry
        return None
    
    def number_of_shares(self, stock_symbol: str) -> None|int:
        num_shares = 0
        if self.contains(stock_symbol):
            num_shares = len(self.get_entry(stock_symbol))
        return num_shares  # same behavior for stock symbols not found in ledger, and those of empty ledger entries