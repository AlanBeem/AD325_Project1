from ledger_entry import LedgerEntry
from stock_purchase import StockPurchase
from stock_sale import StockSale
from random import SystemRandom


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
        elif quantity > len(sell_entry):  # O(len(sell_entry))
            print(f"Cannot fill quantity of sale: {quantity} shares of {stock_symbol}. len(sell_entry) == {len(sell_entry)}")
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
                    sell_entry._linked_deque.front_to_back()
                sale.add_sale(sell_entry.remove_purchase())  # removes from front  # O(1)
        return sale

    def sellOptimal(self, stock_symbol: str, quantity, optimal_selection_int: int=1, expression=None) -> None:
        """optimal_selection_int\n\n1: Sell lowest priced share first"""
        if expression is not None:
            pass
        else:
            sale = StockSale(stock_symbol, quantity)
            sell_entry = self.get_entry(stock_symbol)  # O(N)
            sell_entry_length = self.number_of_shares(stock_symbol)  # O(N)
            if sell_entry is None:
                print(f"Stock symbol not found for {quantity} shares of {stock_symbol}")  # maybe instead of these, have client side code making sense of returned values including some error code
            elif quantity > sell_entry_length:  # O(1)
                print(f"Cannot fill quantity of sale: {quantity} shares of {stock_symbol}. len(sell_entry) == {len(sell_entry)}")
            else:
                # assert: quantity is less than or equal to number of shares
                # if optimal_selection_int == 0:
                #     while len(sale) < quantity:
                #         if sell_entry._linked_deque.get_front().get_data().cost < 
                if optimal_selection_int == 1:
                    # for each share to sell, sell the lowest priced one possible  ### O(N) = O(N) + O(N)
                    if sell_entry_length == 1 and quantity == 1:  # I Think this second condition is redundant
                        sale.add_sale(sell_entry.remove_purchase())
                    else:
                        # print("Point A")
                        # while len(sale) < quantity:  # O(N) = O(N) * quantity
                        while sale.quantity > len(sale):
                            entry_length = len(sell_entry)
                            lowest_cost_share = sell_entry._linked_deque.get_front().get_data()  # O(1)
                            index_from_front = -1  # this value will be overwritten at some point, unless the code below cannot run  ### used to decide which direction to go
                            # locate a lowest cost share  ### alternative: position deque such that front.cost is less than sale price (but this method doesn't know the price)
                            for so_i in range(len(sell_entry)):  # O(len(sell_entry)) setup, O(N)
                                sell_entry._linked_deque.front_to_back()
                                # lowest_cost_share = sell_entry._linked_deque.get_front().get_data()\
                                #     if sell_entry._linked_deque.get_front().get_data().cost < lowest_cost_share.cost\
                                #         else lowest_cost_share
                                if sell_entry._linked_deque.get_front().get_data().cost < lowest_cost_share.cost:
                                    lowest_cost_share = sell_entry._linked_deque.get_front().get_data()
                                    index_from_front = so_i
                                # if lowest_cost_share is sell_entry._linked_deque.get_front():
                                #     index_from_front = so_i  # These are equivalent, it seems: TODO Uncomment and use conditional assignment
                            # print("Point B")
                            # position the Deque 
                            if index_from_front + 1 <= len(sell_entry) - index_from_front - 1:
                                # print("Point B1")
                                for so_j in range(index_from_front + 1):  # O(N) = O(N/2) = O(index_from_front)
                                    sell_entry._linked_deque.front_to_back()
                                # print('went from front')
                                # print('lowest_cost_share:' + str(lowest_cost_share))
                                # print('front: ' + str(sell_entry._linked_deque.get_front().get_data()))
                            else:
                                # print("Point B2")
                                for so_k in range(len(sell_entry) - index_from_front - 1):  # O(N) = O(N/2)
                                    sell_entry._linked_deque.back_to_front()
                                # while sell_entry._linked_deque.get_front().get_data().cost == sell_entry._linked_deque.get_back().get_data().cost:
                                #     sell_entry._linked_deque.back_to_front()  ### This loop runs indefinitely for a sale against all shares of same cost
                                # print('went from back')
                                # print('lowest_cost_share:' + str(lowest_cost_share))
                                # print('front: ' + str(sell_entry._linked_deque.get_front().get_data()))
                            # print("Point C")
                            # add sales of current lowest price
                            while sell_entry._linked_deque.get_front().get_data().cost == lowest_cost_share.cost and len(sale) < quantity:
                                sale.add_sale(sell_entry.remove_purchase())
                            # print("Point C1")
                        # print("Point D")
                        # Code Before:
                        # loop_bool = True
                        # while loop_bool:
                        #     lowest_cost_share = sell_entry._linked_deque.get_front().get_data()  # O(1)
                        #     index_from_front = -1  # this value will be overwritten at some point, unless the code below cannot run  ### used to decide which direction to go
                        #     for so_i in range(len(sell_entry)):  # O(len(sell_entry)) setup, O(N)
                        #         sell_entry._linked_deque.front_to_back()
                        #         lowest_cost_share = sell_entry._linked_deque.get_front().get_data()\
                        #             if sell_entry._linked_deque.get_front().get_data().cost < lowest_cost_share.cost\
                        #                 else lowest_cost_share
                        #         if lowest_cost_share is sell_entry._linked_deque.get_front():
                        #             index_from_front = so_i
                        #     # print("Point B")
                        #     # position the Deque
                        #     if index_from_front + 1 <= len(sell_entry) - index_from_front - 1:
                        #         # print("Point B1")
                        #         for so_j in range(index_from_front + 1):  # O(N) = O(N/2) = O(index_from_front)
                        #             sell_entry._linked_deque.front_to_back()
                        #         # print('went from front')
                        #         # print('lowest_cost_share:' + str(lowest_cost_share))
                        #         # print('front: ' + str(sell_entry._linked_deque.get_front().get_data()))
                        #     else:
                        #         # print("Point B2")
                        #         for so_k in range(len(sell_entry) - index_from_front - 1):  # O(N) = O(N/2)
                        #             sell_entry._linked_deque.back_to_front()
                        #         while sell_entry._linked_deque.get_front().get_data().cost == sell_entry._linked_deque.get_back().get_data().cost:
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
                            # position Deque such that front is less than median, then sell from it until it is greater than median; repeat
                            pass
        return sale

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
    
    def get_ledger_entry_median_data(self, stock_symbol: str) -> StockPurchase:  # O(N)
        ledger_entry = self.get_entry(stock_symbol)
        ledger_length = len(ledger_entry)  # O(N)
        current = ledger_entry._linked_deque.get_front()
        data_list = []
        for m_i in range(ledger_length):
            data_list.append(current.get_data())
            current = current.get_next_node()
        return sorted(data_list)[len(data_list) // 2]