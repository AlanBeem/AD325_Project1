from linked_deque import LinkedDeque
from stock_purchase import StockPurchase

class LedgerEntry:
    def __init__(self, stock_symbol: str) -> None:  # required
        self._linked_deque = LinkedDeque()
        self.symbol = stock_symbol

    def __len__(self) -> int:
        return len(self._linked_deque)

    def add_purchase(self, new_purchase: StockPurchase) -> None:  # required
        # add to the back
        if new_purchase.symbol == self.symbol:
            self._linked_deque.add_to_back(new_purchase)  # TODO diagram out how changing this to add to front, remove from back, would effect other methods (use diagram of dependency)

    def peek(self) -> StockPurchase:
        return self._linked_deque.get_front()
    
    def increment_entry(self) -> None:
        self._linked_deque.front_to_back()

    def remove_purchase(self) -> StockPurchase:  # required
        # remove from the front
        return self._linked_deque.remove_front()#.get_data()  # DLNode is designed as a private inner class of LedgerEntry, so this doesn't return DLNode objects, instead it returns their data portion
        # TODO find and replace all _data with _data_portion (maybe do in textedit)
        # make a branch for it? don't screenshot it though ? or do. I dunno.
    
    def __eq__(self, other):  # O(N) = O(N) + O(N) + ... + O(N)
        equal_bool = False    # where N is the lesser of the deques sizes
        if isinstance(other, self.__class__):
            equal_bool = self._linked_deque == other._linked_deque
        return equal_bool
    
    def equals(self, other) -> bool:  # required  # can be used to compare ledger entries after various strategies (ledgers, for the same inputs, should be the same)
        # return self == other  # O(N)
        if isinstance(other, self.__class__):
            return self.symbol == other.symbol and len(self._linked_deque) == len(other._linked_deque)  # same symbol, same length: equal

    def display_entry(self) -> None:  # required
        if self._linked_deque.is_empty():
            print(f"{self.symbol}: None")
        else:
            price_list = []
            quantity_list = []
            # price_quantity_dict = dict()
            front_ledger_item = self._linked_deque.remove_front()
            self._linked_deque.add_to_back(front_ledger_item)
            price_list.append(front_ledger_item.cost)
            quantity_list.append(1)
            # price_quantity_dict.update({front_ledger_item: 1})  # Alternative, but see below regarding caution about using an object that requires a hashable key
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
                # if current_ledger_item not in price_quantity_dict:
                #     price_quantity_dict.update({current_ledger_item: 1})
                # else:
                #     price_quantity_dict.update({current_ledger_item: price_quantity_dict.get(current_ledger_item) + 1})
                # But, the dictionary might not be in order. Seems as of Python 3.7 they are ordered: https://www.w3schools.com/python/python_dictionaries.asp#:~:text=Ordered%20or%20Unordered%3F,that%20order%20will%20not%20change.
            ledger_string = ''
            for each_price, each_quantity in zip(price_list, quantity_list):
                # ledger_string += str(f" {each_price:.1f} ({each_quantity} shares)")
                ledger_string += str(each_price) + " (" + str(each_quantity) + " shares)   "
            print(self.symbol + ': ' + ledger_string)