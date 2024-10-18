from collections.abc import Iterable


class LinkedDeque:
    def __init__(self, initial_data: Iterable|None =None, front_or_back: str ='Front') -> None:  # required
        # self.front = None
        # self.back = None  # In Java one might use self.clear [this centralizes methods to decrease size of testing path]
        self.clear()  # Works, here, no warnings, in PyCharm, I think this would result in linting for use of self.var not declared in init
        if initial_data is not None:
            if front_or_back.lower() == 'front':
                for each_datum in initial_data:
                    self.add_to_front(each_datum)
            elif front_or_back.lower() == 'back':
                for each_datum in initial_data:
                    self.add_to_front(each_datum)

    def __len__(self) -> int:  # O(N)
        got_length = 0
        current_len_node = self.front  # front (1 node visited)
        while current_len_node is not None:  # unless front is None
            got_length += 1
            current_len_node = current_len_node.get_next_node()
        return got_length

    def __getitem__(self, index: int):
        item = self.front.data  # .copy? deepcopy (for objects) ? I guess it depends.
        for g in range(len(self)):  # recursive traversal for index?
            if g == index % len(self):
                item = self.front.data
            self.front_to_back()
        return item
    
    def _items_data_list(self) -> list:  # self.var.__class__ ?
        data_list = []
        current_data_node = self.front  # front (1 node visited)
        while current_data_node is not None:  # unless front is None
            data_list.append(current_data_node.data)
            current_data_node = current_data_node.get_next_node()
        return data_list

    def __eq__(self, other) -> bool:  # O(N^2) = O(N^2) = O(N^2) + O(N) * intersection of sets of data portions (self, other)
        # Calling this method results in a cascade of __eq__ methods from LinkedDeque through DLNode, including data_portion
        """This assumes that differently ordered deques (of otherwise identical items) are different deques,
        that is, deques are considered (circular) sequences, not (multi)sets.
        and puts self back as was before equals operation."""
        if isinstance(other, self.__class__):
            eq_s_items = self._items_data_list()
            eq_o_items = other._items_data_list()
            eq_bool = True
            if len(eq_s_items) == len(eq_o_items):
                for s_e in range(len(eq_s_items)):
                    for s_o in range(len(eq_o_items)):
                        incremented_o_items = z
            else:
                eq_bool = False
            return eq_bool
    def add_to_back(self, new_entry) -> None:  # required
        if new_entry is not None:  # These handle null entries so that methods in client classes can send null entries w/o adding DLNode(data_portion=None)
            if not isinstance(new_entry, LinkedDeque.DLNode):
                new_node = LinkedDeque.DLNode(data_portion=new_entry)
            else:
                new_node = new_entry
            if self.back is None:
                self.back = new_node
                self.front = self.back
            else:
                new_node.set_previous_node(self.back)
                self.back.set_next_node(new_node)
                self.back = new_node

    def add_to_front(self, new_entry) -> None:  # required
        if new_entry is not None:  # These handle null entries so that methods in client classes can send null entries w/o adding DLNode(data_portion=None)
            # TODO Take this out, and solve client-side to this, it doesn't make sense to prevent client code from being able to add a null node
            if not isinstance(new_entry, LinkedDeque.DLNode):
                new_node = LinkedDeque.DLNode(data_portion=new_entry)
            else:
                new_node = new_entry
            if self.front is None:
                self.front = new_node
                self.back = self.front
            else:
                new_node.set_next_node(self.front)
                self.front.set_previous_node(new_node)
                self.front = new_node

    def get_back(self) -> any:  # required
        return self.back.get_data()

    def get_front(self) -> any:  # required
        if self.front is not None:
            return self.front.get_data()  # TODO make this return data rather than DLNode

    def remove_front(self) -> None:  # required
        front_node = self.front
        if self.front.get_next_node() is None:
            self.clear()
        else:
            self.front = self.front.get_next_node()
            self.front.set_previous_node(None)
            front_node.set_next_node(None)  # Bug fix 10/11/2024  # tabbed in 10/13/2024
        return front_node.get_data()

    def remove_back(self) -> None:  # required
        back_node = self.back
        if self.back.get_previous_node() is None:
            self.clear()
        else:
            self.back = self.back.get_previous_node()
            self.back.set_next_node(None)
            back_node.set_previous_node(None)  # Bug fix 10/11/2024  # tabbed in 10/13/2024
        return back_node.get_data()

    def clear(self) -> None:  # required
        self.front = None
        self.back = None

    def is_empty(self) -> bool:  # required
        return self.front is None and self.back is None

    def front_to_back(self) -> None:
        self.add_to_back(self.remove_front())

    def back_to_front(self) -> None:
        self.add_to_front(self.remove_back())

    def display(self) -> None:  # required
        # make interactive deque display, and report stats on it  # Ask
        pass

    def get_lambda_data_portion(self, func):
        """returns the data_portion of the first data_portion in the deque that satisfies the expression (func)"""
        front_was = self.front
        lambdaest = None
        if len(self) > 1 and not func(front_was):  # O(N)
            current = self.front
            for l in range(len(self)):
                if not func(self.get_front()):
                    self.front_to_back()
                else:
                    lambdaest = current
                    break
            while self.front is not front_was:
                self.front_to_back()
        return lambdaest.get_data()
    # later, activation function of including stocks

    class DLNode:
        def __init__(self, previous_node=None, data_portion=None, next_node=None) -> None:  # required
            self.data = data_portion
            self.previous = previous_node
            self.next = next_node

        def get_data(self) -> any:  # required
            return self.data

        def set_data(self, data: any) -> None:  # required
            self.data = data

        def get_next_node(self):  # -> DLNode  # required
            return self.next

        def set_next_node(self, next_node) -> None:  # required
            self.next = next_node

        def get_previous_node(self):  # -> DLNode  # required
            return self.previous

        def set_previous_node(self, previous_node) -> None:  # required
            self.previous = previous_node