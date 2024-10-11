class LinkedDeque:
    def __init__(self) -> None:  # required
        pass

    def add_to_back(self, new_entry) -> None:  # required
        pass

    def add_to_front(self, new_entry) -> None:  # required
        pass

    def get_back(self) -> any:  # required
        pass

    def get_front(self) -> any:  # required
        pass

    def remove_front(self) -> None:  # required
        pass

    def remove_back(self) -> None:  # required
        pass

    def clear(self) -> None:  # required
        pass

    def is_empty(self) -> bool:  # required
        pass

    def display(self) -> None:  # required
        pass

    class DLNode:
        def __init__(self, previous_node=None, data_portion=None, next_node=None) -> None:  # required
            pass

        def get_data(self) -> any:  # required
            pass

        def set_data(self, data: any) -> None:  # required
            pass

        def get_next_node(self):  # -> DLNode  # required
            pass

        def set_next_node(self, next_node) -> None:  # required
            pass

        def get_previous_node(self):  # -> DLNode  # required
            pass

        def set_previous_node(self, previous_node) -> None:  # required
            pass