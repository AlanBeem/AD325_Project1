from linked_deque import LinkedDeque
from stock_purchase import StockPurchase

class LedgerEntry:
    def __init__(self, stock_symbol: str) -> None:  # required
        self._linked_deque = LinkedDeque()
        self.symbol = stock_symbol

    # def __str__(self) -> str:
    #     pass

    def add_purchase(self, new_purchase: StockPurchase) -> None:  # required
        if new_purchase.symbol == self.symbol:
            self._linked_deque.add_to_back(new_purchase)

    def remove_purchase(self) -> None:  # required
        self._linked_deque.remove_front()

    def equals(self, other) -> bool:  # required
        equal_bool = False
        if not isinstance(other, type(self)):  # TODO testing new syntax, here
            equal_bool = False
        else:
            if self._linked_deque == other._linked_deque:
                equal_bool = True
        return equal_bool

    def display_entry(self) -> None:  # required
        print(f"{str(self)}\n{str(self._linked_deque)}")