from ledger_entry import LedgerEntry
from stock_purchase import StockPurchase
from stock_sale import StockSale
from random import SystemRandom
# TODO Once all working, design taking StockSale out of this Class, and handling at some more main level


class StockLedger:
    def __init__(self) -> None:  # required
        self.ledger_entries = []
        self.stock_sales_list = []

    def __len__(self):
        return len(self.ledger_entries)
    
    def __getitem__(self, index) -> LedgerEntry:
        return self.ledger_entries[index]
    
    # def __eq__(self, other) -> bool:
    #     eq_bool = False
    #     if len(self) == len(other):
    #         for each_entry in self:
    #             if 

    def equals(self, other) -> bool:
        equals_bool = True
        if not isinstance(other, self.__class__):
            equals_bool = False
        else:
            if len(self.ledger_entries) != len(other.ledger_entries):
                equals_bool = False
            else:
                for each_entry in self.ledger_entries:
                    if each_entry != other.get_entry(each_entry.symbol):
                        equals_bool = False
                        break
        return equals_bool
    
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

    def sell(self, stock_symbol: str, quantity: int) -> StockSale:  # required  # O(N)
        sale = StockSale(stock_symbol, quantity)
        sell_entry = self.get_entry(stock_symbol)  # O(N)
        if sell_entry is None:
            print(f"Stock symbol not found for {quantity} shares of {stock_symbol}")  # maybe instead of these, have client side code making sense of returned values including some error code
            return None
        elif quantity > len(sell_entry):  # O(len(sell_entry))
            print(f"Cannot fill quantity of sale: {quantity} shares of {stock_symbol}. len(sell_entry) == {len(sell_entry)}")
            return None
        else:
            for s_i in range(quantity):  # O(quantity)
                sale.add_sale(sell_entry.remove_purchase())  # O(1)
        return sale

    def sellRandom(self, stock_symbol: str, quantity: int) -> StockSale:  # O(N)
        sale = StockSale(stock_symbol, quantity)
        sell_entry = self.get_entry(sale.symbol)  # O(N)
        sell_entry_length = len(sell_entry)  # O(N)
        if sell_entry is None:
            print(f"Stock symbol not found for {quantity} shares of {stock_symbol}")  # maybe instead of these, have client side code making sense of returned values including some error code
        elif quantity > len(sell_entry):  # O(len(sell_entry)) # O(N)
            print(f"Cannot fill quantity of sale: {quantity} shares of {stock_symbol}. len(sell_entry) == {len(sell_entry)}")
        else:
            # O(N)
            for s_i in range(quantity):  # O(quantity)
                for s_j in range(SystemRandom().randint(0, sell_entry_length * 17) % (sell_entry_length - s_i)):  # O(N)
                    sell_entry.increment_entry()
                sale.add_sale(sell_entry.remove_purchase())  # removes from front  # O(1)
        return sale

    def sellOptimal(self, stock_symbol: str, quantity, optimal_selection_int: int=1, expression=None) -> None:
        """optimal_selection_int\n\n1: Sell lowest priced share first"""
        if expression is not None:
            pass
        else:
            sale = StockSale(stock_symbol, quantity)  # Alternatively keep StockSale to whatever has StockLedger, and return a list or tuple of StockPurchases
            sell_entry = self.get_entry(stock_symbol)  # O(N)
            sell_entry_length = self.number_of_shares(stock_symbol)  # O(N)
            if sell_entry is None:
                print(f"Stock symbol not found for {quantity} shares of {stock_symbol}")  # maybe instead of these, have client side code making sense of returned values including some error code
            elif quantity > sell_entry_length:  # O(1)
                print(f"Cannot fill quantity of sale: {quantity} shares of {stock_symbol}. len(sell_entry) == {len(sell_entry)}")
            else:
                # assert: quantity is less than or equal to number of shares (sale can be filled)
                if optimal_selection_int == 1:  # fill with lowest cost shares
                    while not sale.is_filled():  # O(N) = O(N) * quantity  # fill the sale
                        if sale.quantity - len(sale) == self.number_of_shares(stock_symbol):
                            for s_i in range(self.number_of_shares(stock_symbol)):
                                sale.add_sale(sell_entry.remove_purchase())
                                # if the currently required quantity is equal to the number of shares, all must be sold
                        else:
                            lowest_cost_share = sell_entry._linked_deque.get_front()  # O(1), gets a StockPurchase, in this case
                            index_from_front = 0  # this value will be overwritten at some point, unless the code below cannot run  ### used to decide which direction to go
                            entry_length = len(sell_entry)
                            # locate a lowest cost share  ### alternative: position deque such that front is less than sale price (but this method doesn't know the price)
                            for so_i in range(entry_length):  # O(len(sell_entry)) setup, O(N)
                                sell_entry.increment_entry()  # TODO Replace this syntax with a call to a method of LedgerEntry that does front to back
                                if sell_entry._linked_deque.get_front() < lowest_cost_share:
                                    lowest_cost_share = sell_entry._linked_deque.get_front()
                                    index_from_front = so_i     # switching the order of these causes indefinite while loop
                            # position the Deque according to index_from_front  # TODO replace with 'lambda_position' ? or fill_below ?
                            if index_from_front + 1 <= len(sell_entry) - index_from_front - 1:
                                for so_j in range(index_from_front + 1):  # O(N) = O(N/2) = O(index_from_front)
                                    sell_entry.increment_entry()
                                # print(f"front after deque-positioning: {sell_entry._linked_deque.get_front()}")
                                # print(lowest_cost_share)
                            else:
                                for so_k in range(len(sell_entry) - index_from_front - 1):  # O(N) = O(N/2)
                                    sell_entry._linked_deque.back_to_front()
                                # print(f"front after deque-positioning: {sell_entry._linked_deque.get_front()}")
                                # print(lowest_cost_share)
                            # add sales of current lowest cost
                            # print(sell_entry._linked_deque.get_front() == lowest_cost_share)
                            while not sale.is_filled() and sell_entry._linked_deque.get_front().cost == lowest_cost_share.cost:
                                # print("Entered fill loop")
                                sale.add_sale(sell_entry.remove_purchase())
                        # Code Before:
                        # loop_bool = True
                        # while loop_bool:
                        #     lowest_cost_share = sell_entry._linked_deque.get_front().get_data()  # O(1)
                        #     index_from_front = -1  # this value will be overwritten at some point, unless the code below cannot run  ### used to decide which direction to go
                        #     for so_i in range(len(sell_entry)):  # O(len(sell_entry)) setup, O(N)
                        #         sell_entry.increment_entry()
                        #         lowest_cost_share = sell_entry._linked_deque.get_front().get_data()\
                        #             if sell_entry._linked_deque.get_front().get_data() < lowest_cost_share\
                        #                 else lowest_cost_share
                        #         if lowest_cost_share is sell_entry._linked_deque.get_front():
                        #             index_from_front = so_i
                        #     # print("Point B")
                        #     # position the Deque
                        #     if index_from_front + 1 <= len(sell_entry) - index_from_front - 1:
                        #         # print("Point B1")
                        #         for so_j in range(index_from_front + 1):  # O(N) = O(N/2) = O(index_from_front)
                        #             sell_entry.increment_entry()
                        #         # print('went from front')
                        #         # print('lowest_cost_share:' + str(lowest_cost_share))
                        #         # print('front: ' + str(sell_entry._linked_deque.get_front().get_data()))
                        #     else:
                        #         # print("Point B2")
                        #         for so_k in range(len(sell_entry) - index_from_front - 1):  # O(N) = O(N/2)
                        #             sell_entry._linked_deque.back_to_front()
                        #         while sell_entry._linked_deque.get_front().get_data() == sell_entry._linked_deque.get_back().get_data():
                        #             sell_entry._linked_deque.back_to_front()
                        #         # print('went from back')
                        #         # print('lowest_cost_share:' + str(lowest_cost_share))
                        #         # print('front: ' + str(sell_entry._linked_deque.get_front().get_data()))
                        #     # print("Point C")
                        #     # add sales of current lowest price
                        #     while sell_entry._linked_deque.get_front().get_data() == lowest_cost_share and len(sale) < quantity:
                        #         sale.add_sale(sell_entry.remove_purchase())
                        #     # print("Point C1")
                        #     if sale.quantity == len(sale):
                        #         loop_bool = False
                        # # print("Point D")
                if optimal_selection_int == 2:
                    # print("Point A")
                    while not sale.is_filled():  # see assertion above, this loop will not run indefinitely (number of shares >= quantity)
                        # get current median cost and ledger length
                        # print("Point B")
                        current_median, current_length = self.get_ledger_entry_median_data(stock_symbol)  # tuple(float, int)
                        for t_j in range(current_length):  # must visit up to each data_portion
                            # print("Point C")
                            if sale.is_filled():  # order is filled
                                break  #                    #
                            # current_purchase = sell_entry.remove_purchase()  # examine a purchase (removes from front)
                            if sell_entry.peek().cost <= current_median:
                                # print("Point D")
                            # if current_purchase.cost <= current_median:           #
                                sale.add_sale(sell_entry.remove_purchase())                 # add to sale,
                            else:                                               #
                                # sell_entry.add_purchase(current_purchase)       # or add to back of deque
                                sell_entry.increment_entry()
        return sale

    def display_ledger(self) -> None:  # required
        print("----  Stock Ledger  ----")
        for each_entry in self.ledger_entries:
            each_entry.display_entry()
    
    def display_total_shares(self) -> None:
        print("Total shares:")
        for each_entry in self.ledger_entries:
            print(f"{each_entry.symbol}: {self.number_of_shares(each_entry.symbol)} shares")

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
        return num_shares  # same behavior for stock symbols not found in ledger and those of empty ledger entries
    
    def get_ledger_entry_median_data(self, stock_symbol: str) -> tuple[float, int]:  # O(N)
        ledger_entry = self.get_entry(stock_symbol)
        ledger_length = len(ledger_entry)  # O(N)
        current_data = ledger_entry._linked_deque.get_front()  # a StockPurchase
        data_list = []  # this gets sorted, deque remains in order
        for m_i in range(ledger_length):
            data_list.append(current_data.cost)
            ledger_entry.increment_entry()
            current_data = ledger_entry._linked_deque.get_front()  # ledger entry returns a StockPurchase
        return sorted(data_list)[len(data_list) // 2], ledger_length