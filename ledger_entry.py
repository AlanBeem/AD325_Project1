from linked_deque import LinkedDeque
from stock_purchase import StockPurchase

class LedgerEntry:
    def __init__(self, stock_symbol: str) -> None:  # required
        self._linked_deque = LinkedDeque()
        self.symbol = stock_symbol

    def add_purchase(self, new_purchase: StockPurchase) -> None:  # required
        if new_purchase.symbol == self.symbol:
            self._linked_deque.add_to_back(new_purchase)

    def remove_purchase(self) -> None:  # required
        return self._linked_deque.remove_front()

    def __eq__(self, other):
        equal_bool = False
        # if isinstance(other, type(self)):  # TODO testing new syntax, here
        if isinstance(other, self.__class__):
            if self._linked_deque == other._linked_deque:
                equal_bool = True
        return equal_bool
    
    def equals(self, other) -> bool:  # required
        equals_bool = False
        # if isinstance(other, type(self)):  # TODO testing new syntax, here
        if isinstance(other, self.__class__):
            equals_bool = self.symbol == other.symbol
        return equals_bool

    def display_entry(self) -> None:  # required
        if len(self._linked_deque) == 0:
            print(f"{self.symbol}: None")
        else:
            price_list = []
            quantity_list = []
            # price_quantity_dict = dict()
            front_ledger_item = self._linked_deque.remove_front()
            self._linked_deque.add_to_back(front_ledger_item)
            price_list.append(front_ledger_item.cost)
            quantity_list.append(1)
            # price_quantity_dict.update({front_ledger_item.cost: 1})
            current_ledger_item = self._linked_deque.remove_front()
            self._linked_deque.add_to_back(current_ledger_item)
            while current_ledger_item is not front_ledger_item:
                if current_ledger_item.cost not in price_list:
                    price_list.append(current_ledger_item.cost)
                    quantity_list.append(1)
                else:
                    quantity_list[price_list.index(current_ledger_item.cost)] += 1
                current_ledger_item = self._linked_deque.remove_front()
                self._linked_deque.add_to_back(current_ledger_item)
                # if current_ledger_item.cost not in price_quantity_dict:
                #     price_quantity_dict.update({current_ledger_item.cost: 1})
                # else:
                #     price_quantity_dict.update({current_ledger_item.cost: price_quantity_dict.get(current_ledger_item.cost) + 1})
                # But, the dictionary might not be in order. Seems as of Python 3.7 they are ordered: https://www.w3schools.com/python/python_dictionaries.asp#:~:text=Ordered%20or%20Unordered%3F,that%20order%20will%20not%20change.
            ledger_string = ''
            for each_price, each_quantity in zip(price_list, quantity_list):
                ledger_string += f"{each_price:.1f} ({each_quantity} shares)"
            print(self.symbol + ': ' + ledger_string)