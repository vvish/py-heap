class IndexedHeap:
    """
    Class provides functionality of the binary heap data structure along with the ability
    to modify stored values.

    IndexedHeap(self, items={}, key=lambda x: (x,), reverse=False)

    Creates a heap object constructed from `items` dictionary. The keys of the dictionary will be
    used to reference items of the heap for possible manipulation and the values will be used to derive
    keys for ordering inside the heap. The collection provides the set of operations similar to 
    dictionary (subscript, len, del, update)

    The class can be used to build Max or Min heaps based on user provided `key` function and 
    `reverse` flag.

    By default the Min-heap (where key-0 <= key-1 <= ... <= key-n) is build but if the `reverse` 
    flag is set the Max-heap (key-0 >= key-1 >= ... >= key-n) will be constructed.

    Parameters
    ----------
    items: dictionary
        dictionary to create a heap from

    key: callable
        operator to get a key from a heap item value (by default the value itself will be used as a key)

    reverse: bool
        flag to indicate if Max-heap should be build instead of Min-heap

    Examples
    --------
    # without provided key functor the dictionary values are used as keys for sorting
    # as the reverse flag is not set the Min-heap will be constructed 
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})

    # the element with dictionary key 5 will be modified
    heap[5] = 0

    # value with key 4 will be updated and with the key 7 inserted (semantics similar to dictionary)
    heap.update({4:10, 7:11})

    # the item with minimum heap key (dictionary value will be extracted)
    top_item = heap.pop_first()


    # the custom key function is used
    class Value:
    def __init__(self, key):
        self.key = key

    heap = IndexedHeap({1:Value(1), 2:Value(2), 3:Value(3), 4:Value(4), 5:Value(5)}, key=lambda i: i.key)

    """

    def __init__(self, items={}, key=lambda x: x, reverse=False):

        self.__key = key
        self.__reverse = reverse

        self.__items = list(items.items())
        self.__handle_to_position_mapping = {
            item[0]: i for i, item in enumerate(self.__items)}

        self.__create_heap()

    def __len__(self):
        return len(self.__items)

    def __getitem__(self, key):
        index = self.__handle_to_position_mapping[key]
        return self.__items[index][1]

    def __setitem__(self, key, value):
        if key in self:
            self.__modify(key, value)
        else:
            self.__add_item(key, value)

    def __contains__(self, key):
        return key in self.__handle_to_position_mapping

    def __delitem__(self, key):
        item_index = self.__handle_to_position_mapping[key]
        self.__swap(item_index, -1)

        del self.__handle_to_position_mapping[key]
        del self.__items[-1]

        self.__heapify_down(item_index)

    def __iter__(self):
        return (i for i in self.items())


    def items(self):
        """
        Method return items contained in the Heap

        Returns
        -------
        array_like
            List of tuples containing key/item in the heap order

        """
        return self.__items

    def pop_first(self):
        """
        Method extracts and returns the first item in the heap
        The heap order for remaining items is preserved

        Returns
        -------
        object
            The first item in the heap order

        """

        if len(self.__items) == 0:
            return None, None

        top_item = self.__items[0]

        self.__swap(0, -1)

        del self.__handle_to_position_mapping[self.__items[-1][0]]
        del self.__items[-1]

        self.__heapify_down(0)

        return top_item

    def update(self, new_items):
        """
        Method inserts or updates the items from `new_items` dictionary. 
        The heap order will be recovered if the value modifications lead to the heap-keys update 

        Parameters
        ----------
        new_items: dictionary
            The dictionary of the new items where the value should be compaitable with key extraction functor

        """

        for k, v in new_items.items():
            if k in self:
                self.__modify(k, v)
            else:
                self.__add_item(k, v)

    def __modify(self, handle, new_value):
        index = self.__handle_to_position_mapping[handle]

        old_key, new_key = self.__key(
            self.__items[index][1]), self.__key(new_value)
        self.__items[index] = (handle, new_value)

        if self.__are_keys_in_order(old_key, new_key):
            self.__heapify_down(index)
        else:
            self.__heapify_up(index)

    def __add_item(self, key, value):
        self.__items.append((key, value))
        self.__handle_to_position_mapping[key] = len(self.__items) - 1
        self.__heapify_up(len(self.__items) - 1)

    def __parent(self, index):
        return index // 2

    def __left_child(self, index):
        return index * 2 + 1

    def __right_child(self, index):
        return index * 2 + 2

    def __get_key_by_index(self, index):
        return self.__key(self.__items[index][1])

    def __are_keys_in_order(self, first_key, second_key):
        return first_key <= second_key if not self.__reverse else first_key >= second_key

    def __are_items_in_order(self, first_index, second_index):
        return self.__are_keys_in_order(self.__get_key_by_index(
            first_index), self.__get_key_by_index(second_index))

    def __swap(self, first_index, second_index):
        self.__handle_to_position_mapping[self.__items[first_index][0]
                                          ], self.__handle_to_position_mapping[self.__items[second_index][0]] = second_index, first_index

        self.__items[first_index], self.__items[second_index] = self.__items[second_index], self.__items[first_index]

    def __heapify_down(self, index):
        left = self.__left_child(index)
        right = self.__right_child(index)

        swap_position = left if left < len(
            self.__items) and self.__are_items_in_order(left, index) else index

        if right < len(self.__items) and self.__are_items_in_order(right, swap_position):
            swap_position = right

        if swap_position != index:
            self.__swap(index, swap_position)
            self.__heapify_down(swap_position)

    def __heapify_up(self, item):
        parent = self.__parent(item)
        while item > 0 and self.__are_items_in_order(item, parent):
            self.__swap(item, parent)
            item = parent
            parent = self.__parent(item)

    def __create_heap(self):
        for i in reversed(range(0, len(self.__items) // 2)):
            self.__heapify_down(i)


def sort(heap):
    """
    Function implements heapsort

    Auxiliary function that extracts top element from a 
    heap and yields it. The sort order is defined by the 
    order in the heap.

    Parameters
    ----------
    heap: Heap object
        The heap object used in algorithm

    Yields
    -------
    object
        Next item in the sorted order            

    """

    k, v = heap.pop_first()
    while k is not None:
        yield k, v
        k, v = heap.pop_first()
