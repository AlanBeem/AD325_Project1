class LinkedDeque:
    def __init__(self) -> None:  # required
        # self.front = None
        # self.back = None  # In Java one might use self.clear
        self.clear()

    def add_to_back(self, new_entry) -> None:  # required
        new_node = LinkedDeque.DLNode(data_portion=new_entry)
        if self.back is None:
            self.back = new_node
            self.front = self.back
        else:
            new_node.set_previous_node(self.back)
            self.back.set_next_node(new_node)
            self.back = new_node

    def add_to_front(self, new_entry) -> None:  # required
        new_node = LinkedDeque.DLNode(data_portion=new_entry)
        if self.front is None:
            self.front = new_node
            self.back = self.front
        else:
            new_node.set_next_node(self.front)
            self.front.set_previous_node(new_node)
            self.front = new_node

    def get_back(self) -> any:  # required
        return self.back

    def get_front(self) -> any:  # required
        return self.front

    def remove_front(self) -> None:  # required
        front_node = self.get_front()
        if self.front.get_next_node() is None:
            self.clear()
        else:
            self.front = self.front.get_next_node()
            self.front.set_previous_node(None)
        return front_node

    def remove_back(self) -> None:  # required
        back_node = self.get_back()
        if self.back.get_previous_node() is None:
            self.clear()
        else:
            self.back = self.back.get_previous_node()
            self.back.set_next_node(None)
        return back_node

    def clear(self) -> None:  # required
        self.front = None
        self.back = None

    def is_empty(self) -> bool:  # required
        return self.front is None and self.back is None

    def display(self) -> None:  # required
        pass

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