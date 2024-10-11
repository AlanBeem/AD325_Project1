from stock_purchase import StockPurchase
from ledger_entry import LedgerEntry


class StockLedger:
    def __init__(self) -> None:  # required
        self.ledger_entries = []

    def __len__(self):
        return len(self.ledger_entries)
    
    def get_entry(self, stock_symbol: str) -> LedgerEntry:
        for each_entry in self.ledger_entries:
            if each_entry.symbol == stock_symbol:
                return each_entry
        return None

    def buy(self, stock_symbol, shares_bought, cost_per_share) -> None:  # required
        buy_entry = self.get_entry(stock_symbol)
        if buy_entry is None:
            self.ledger_entries.append(LedgerEntry(stock_symbol))
            buy_entry = self.ledger_entries[-1]
        for share in range(shares_bought):
            buy_entry.add_purchase(StockPurchase(stock_symbol, cost_per_share))

    def sell(self, stock_symbol, shares_sold, price_per_share) -> None:  # required
        sell_entry = self.get_entry(stock_symbol)
        if sell_entry is None:
            print("sell_entry is None: stock symbol not found")
        else:
            for share in range(shares_sold):
                sell_entry.remove_purchase()

    def display_ledger(self) -> None:  # required
        pass

    def contains(self, stock_symbol) -> bool:  # required
        pass

    def get_entry(self, stock_symbol) -> LedgerEntry:  # required
        pass