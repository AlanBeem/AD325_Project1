# from stock_ledger import StockLedger
# from trading_bot import TradingBot
# from stock_purchase import StockPurchase
# from stock_sale import StockSale
# from random import SystemRandom

# # Sell functions don't put the deque back as it was
# # Sell functions assume that fill quantity is less than len(ledger_entry)
# class SellFunction:  # O(fill quantity)
#     def sf(self, trading_bot: TradingBot, sale: StockSale, fill_quantity: int|None =0) -> None:
#         # if fill_quantity is None:  # and isinstance(sale, StockSale):
#         #     fill_quantity = sale.quantity - len(sale)
#         for s_i in range(fill_quantity):
#             sale.add_sale(trading_bot.stock_ledger.sell(sale.symbol, sale.shares, sale.price))


# class SellRandom(SellFunction):  # O(fill quantity)
#     def sf(self, trading_bot: TradingBot, sale: StockSale, fill_quantity: int) -> None:
#         ledger_entry = trading_bot.stock_ledger.get_entry(sale.symbol)
#         ledger_entry_length = len(ledger_entry)
#         for s_i in range(fill_quantity):  # O(fill quantity)
#             for s_j in range(SystemRandom().randint(0, ledger_entry_length * 17) % len(ledger_entry_length)):  # O(N)
#                 ledger_entry._linked_deque.add_to_back(ledger_entry._linked_deque.remove_front())  # O(1)  # this could go in either direction
#             sale.add_sale(ledger_entry.remove_purchase())  # removes from front


# def get_ledger_entry_median_data(stock_ledger: StockLedger, stock_symbol: str) -> StockPurchase:  # O(N)
#     # ledger_entry = stock_ledger.get_entry(stock_symbol)
#     # for m_i in range(len(ledger_entry) // 2):
#     #     ledger_entry._linked_deque.add_to_back(ledger_entry._linked_deque.remove_front())
#     # median_data_portion = ledger_entry._linked_deque.get_front().get_data()
#     # for m_j in range(len(ledger_entry) // 2):
#     #     ledger_entry._linked_deque.add_to_front(ledger_entry._linked_deque.remove_back())
#     # return median_data_portion  # Not sorted! but if it were... 
#     # could also adjust bounds in a search assuming linearity between least and greatest prices # if that's important, could make it true
#     ledger_entry = stock_ledger.get_entry(stock_symbol)
#     ledger_length = len(ledger_entry)  # O(N)
#     current = ledger_entry._linked_deque.get_front()
#     data_list = []
#     for m_i in range(ledger_length):
#         data_list.append(current.get_data())
#         current = current.get_next_node()
#     return sorted(data_list)[len(data_list) // 2]
    

# # def Sell

# # class SellFunction:
# #         def __init__(self, trading_bot: TradingBot) -> None:
# #             self.trading_bot = trading_bot
        
# #         def sell_f(self, sell_stock: StockSale) -> None:
# #             while 

# # class SellStrategy:  # can aim multiple of these at the same StockLedger, and mix sales between them
# #     # can also partially fill with one strategy, and then use another (this might be more relevant where strategies decide whether or not to buy and/or sell)
# #     def __init__(self, sell_function: SellFunction) -> None:
# #         self.sell_function = sell_function(trading_bot)
# # Had commented out whole file, before finishing SellFunction, but, thought maybe I didn't need it, it's needed because I don't want to define a bunch of different methods in cgh helper methods

# # 10-12-2024 I think I won't need this file, instead using staticmethods of TradingBot that default to sell_function

