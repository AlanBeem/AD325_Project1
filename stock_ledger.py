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

    def __str__(self) -> str:
        out_string = "Total shares:"
        for each_entry in self.ledger_entries:
            out_string += f"\n{each_entry.symbol}: {self.number_of_shares(each_entry.symbol)} shares"  # for equals, can compare whether these are the same
        return out_string

    def equals(self, other) -> bool:
        # equals_bool = True
        # if not isinstance(other, self.__class__):
        #     equals_bool = False
        # else:
        #     if len(self.ledger_entries) != len(other.ledger_entries):
        #         equals_bool = False
        #     else:
        #         for each_entry in self.ledger_entries:
        #             if each_entry != other.get_entry(each_entry.symbol):
        #                 equals_bool = False
        #                 break
        # return equals_bool
        return str(self) == str(other)
    
    def buy(self, stock_symbol, shares_bought, cost_per_share) -> None:  # required  # O(shares_bought)
        if not self.contains(stock_symbol):
            self.ledger_entries.append(LedgerEntry(stock_symbol))
            buy_entry = self.ledger_entries[-1]
        else:
            buy_entry = self.get_entry(stock_symbol)
        for share in range(shares_bought):
            buy_entry.add_purchase(StockPurchase(stock_symbol, cost_per_share))

    def buyRandom(self, stock_symbol: str, shares_to_buy: int, cost_per_share: float) -> None:
        if not self.contains(stock_symbol):
            self.ledger_entries.append(LedgerEntry(stock_symbol))
            buy_entry = self.ledger_entries[-1]
        else:
            buy_entry = self.get_entry(stock_symbol)
        for s_i in range(shares_to_buy):  # O(shares_to_buy) * O(len(buy_entry))
            for s_j in range(SystemRandom().randint(0, len(buy_entry) * 17) % (len(buy_entry) - s_i)):  # O(N)
                buy_entry.increment_entry()
            buy_entry.add_purchase(StockPurchase(stock_symbol, cost_per_share))

    def buyOptimal(self, stock_symbol: str, shares_to_buy: int, cost_per_share: float, optimal_selection_int: int =1) -> None:
        if not self.contains(stock_symbol):
            self.ledger_entries.append(LedgerEntry(stock_symbol))
            buy_entry = self.ledger_entries[-1]
        else:
            buy_entry = self.get_entry(stock_symbol)
        # increment_entry() until at position of ascending order ## The last one for which it's greater
        # sellRandom:
        # for s_i in range(shares_to_buy):  # O(shares_to_buy) * O(len(buy_entry))
        #     for s_j in range(SystemRandom().randint(0, len(buy_entry) * 17) % (len(buy_entry) - s_i)):  # O(N)
        #         buy_entry.increment_entry()
        #     buy_entry.add_purchase(StockPurchase(stock_symbol, cost_per_share))

    def sell(self, stock_symbol: str, quantity: int, price: float) -> StockSale:  # ~required  # O(N)
        sale = StockSale(stock_symbol, quantity, price)
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

    def sellRandom(self, stock_symbol: str, quantity: int, price: float) -> StockSale:  # O(N)
        sale = StockSale(stock_symbol, quantity, price)
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

    def sellOptimal(self, stock_symbol: str, quantity: int, price: float, optimal_selection_int: int=1) -> None:  # O(f(optimal selection_int))
        """optimal_selection_int\n\n1: Sell lowest priced share first"""
        sale = StockSale(stock_symbol, quantity, price)  # Alternatively keep StockSale to whatever has StockLedger, and return a list or tuple of StockPurchases
        sell_entry = self.get_entry(stock_symbol)  # O(len(self.ledger_entries))
        sell_entry_length = self.number_of_shares(stock_symbol)  # O(N)
        if sell_entry is None:
            print(f"Stock symbol not found for {quantity} shares of {stock_symbol}")  # maybe instead of these, have client side code making sense of returned values including some error code
        elif quantity > sell_entry_length:  # O(1)
            print(f"Cannot fill quantity of sale: {quantity} shares of {stock_symbol}. len(sell_entry) == {len(sell_entry)}")
        else:
            # assertion: quantity is less than or equal to number of shares
            if optimal_selection_int == 1:  # fill with lowest cost shares  # O()
                while not sale.is_filled():  # O(N) = O(N) * quantity  # fill the sale
                    if sale.quantity - len(sale) == self.number_of_shares(stock_symbol):
                        for s_i in range(self.number_of_shares(stock_symbol)):
                            sale.add_sale(sell_entry.remove_purchase())
                    else:
                        lowest_cost_share = sell_entry._linked_deque.get_front()  # O(1), gets a StockPurchase, in this case
                        index_from_front = 0
                        entry_length = len(sell_entry)
                        # locate a lowest cost share
                        for so_i in range(entry_length):  # O(len(sell_entry)) setup, O(N)
                            sell_entry.increment_entry()                                    ##
                            if sell_entry._linked_deque.get_front() < lowest_cost_share:    ##
                                lowest_cost_share = sell_entry._linked_deque.get_front()    #    switching the order of these causes indefinite while loop
                                index_from_front = so_i                                     #
                        # position the Deque according to index_from_front  # TODO replace with 'lambda_position' ? or fill_below ?
                        if index_from_front + 1 <= len(sell_entry) - index_from_front - 1:
                            for so_j in range(index_from_front + 1):  # O(N) = O(N/2) = O(index_from_front)
                                sell_entry.increment_entry()
                        else:
                            for so_k in range(len(sell_entry) - index_from_front - 1):  # O(N) = O(N/2)
                                sell_entry._linked_deque.back_to_front()
                        while not sale.is_filled() and sell_entry._linked_deque.get_front().cost == lowest_cost_share.cost:
                            sale.add_sale(sell_entry.remove_purchase())
            if optimal_selection_int == 2:  # O()
                while not sale.is_filled():  # see assertion above, number of shares >= quantity: this loop will not run indefinitely
                    current_median, current_length = self.get_ledger_entry_median_data(stock_symbol)  # tuple(float, int)  # O(len(sell_entry))
                    for t_j in range(current_length):  # must visit up to each data_portion (per while iteration)
                        if sale.is_filled():
                            break
                        if sell_entry.peek().cost <= current_median:
                            sale.add_sale(sell_entry.remove_purchase())
                        else:
                            sell_entry.increment_entry()
        return sale

    def display_ledger(self) -> None:  # required
        print("----  Stock Ledger  ----")
        for each_entry in self.ledger_entries:
            each_entry.display_entry()
    
    def display_total_shares(self) -> None:
        print(self)

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
    
    # TODO Make this work like codestepbystep exercise for median in a stack
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