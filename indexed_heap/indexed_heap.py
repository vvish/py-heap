"""Binary heap with items indexed by a key."""


class IndexedHeap(object):
    """
    Binary heap with support for stored values modifications.

    Creates a heap object constructed from `items_to_add` dictionary.
    The keys of the dictionary will be used to reference items of the
    heap for possible manipulation and the values will be used to derive
    keys for ordering inside the heap. The collection provides the set
    of operations similar to dictionary (subscript, len, del, update)

    The class can be used to build Max or Min heaps based on user
    provided `key` function and `reverse` flag.

    By default the Min-heap (where key-0 <= key-1 <= ... <= key-n) is
    build but if the `reverse` flag is set the Max-heap
    (key-0 >= key-1 >= ... >= key-n) will be constructed.

    """

    def __init__(self, items_to_add=None, key=None, reverse=False):
        """
        Initialize the new object.

        Parameters
        ----------
        items_to_add: dictionary
            dictionary to create a heap from

        key: callable
            operator to get a key from a heap item value (by default the
            value itself will be used as a key)

        reverse: bool
            flag to indicate if Max-heap should be build instead of Min-heap

        Examples
        --------
        # without provided key functor the dictionary values are used as
        # keys for sorting as the reverse flag is not set the Min-heap will
        # be constructed
        heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})

        # the element with dictionary key 5 will be modified
        heap[5] = 0

        # value with key 4 will be updated and with the key 7 inserted
        # semantics similar to dictionary
        heap.update({4:10, 7:11})

        # the item with minimum heap key (dictionary value will be extracted)
        top_item = heap.pop_first()


        # the custom key function is used
        class Value:
            def _init_(self, key):
                self.key = key

        heap = IndexedHeap({1:Value(1), 2:Value(2), 3:Value(3),
            4:Value(4), 5:Value(5)}, key=lambda i: i.key)
        """
        self._key = key or (lambda x: x)
        self._reverse = reverse

        self._heap_items = list(items_to_add.items()) if items_to_add else []
        self._handle_to_position_mapping = {
            heap_item[0]: idx for idx, heap_item in enumerate(self._heap_items)
        }

        self._create_heap()

    def __len__(self):
        """
        Return length (items count) of the heap.

        Returns
        -------
        int
            current items count
        """
        return len(self._heap_items)

    def __getitem__(self, key):
        """
        Return item by key (subscript operator).

        Parameters
        ----------
        key : key_type
            key of the heap item

        Returns
        -------
        value_type
            heap value
        """
        index = self._handle_to_position_mapping[key]
        return self._heap_items[index][1]

    def __setitem__(self, key, new_value):
        """
        Assign the new value to an item (via subscript operator).

        The new value will cause the heap reordering.

        Parameters
        ----------
        key : key_type
            key of te item
        new_value : vlaue_type
            item's new value
        """
        if key in self:
            self._modify(key, new_value)
        else:
            self._add_item(key, new_value)

    def __contains__(self, key):
        """
        Check if an item with the key is in the heap ('in' operator).

        Parameters
        ----------
        key : key_type
            key to check

        Returns
        -------
        bool
            indicates if the item was found
        """
        return key in self._handle_to_position_mapping

    def __delitem__(self, key):
        """
        Delete item from the heap (del operator).

        Parameters
        ----------
        key : key_type
            key of the item to remove
        """
        item_index = self._handle_to_position_mapping[key]
        self._swap(item_index, -1)

        del self._handle_to_position_mapping[key]
        del self._heap_items[-1]

        self._heapify_down(item_index)

    def __iter__(self):
        """
        Iterate items.

        Returns
        -------
        iterable
            object to iterate items
        """
        return (it for it in self.get_items())

    def get_items(self):
        """
        Return items contained in the Heap.

        Returns
        -------
        array_like
            List of tuples containing key/item in the heap order

        """
        return self._heap_items

    def pop_first(self):
        """
        Extract and return the first item in the heap.

        The heap order for remaining items is preserved

        Returns
        -------
        object
            The first item in the heap order

        """
        if not self._heap_items:
            return None, None

        top_item = self._heap_items[0]

        self._swap(0, -1)

        del self._handle_to_position_mapping[self._heap_items[-1][0]]
        del self._heap_items[-1]

        self._heapify_down(0)

        return top_item

    def update(self, new_items):
        """
        Update existing or insert new items.

        Method inserts or updates the items from `new_items` dictionary.
        The heap order will be recovered if the value modifications lead
        to the heap-keys update

        Parameters
        ----------
        new_items: dictionary
            The dictionary of the new items where the value should be
            compaitable with key extraction functor

        """
        for key, new_value in new_items.items():
            if key in self:
                self._modify(key, new_value)
            else:
                self._add_item(key, new_value)

    def _modify(self, item_handle, new_value):
        index = self._handle_to_position_mapping[item_handle]

        old_key, new_key = (
            self._key(self._heap_items[index][1]), self._key(new_value),
        )
        self._heap_items[index] = (item_handle, new_value)

        if self._are_keys_in_order(old_key, new_key):
            self._heapify_down(index)
        else:
            self._heapify_up(index)

    def _add_item(self, key, new_value):
        self._heap_items.append((key, new_value))
        self._handle_to_position_mapping[key] = len(self._heap_items) - 1
        self._heapify_up(len(self._heap_items) - 1)

    def _get_key_by_index(self, index):
        return self._key(self._heap_items[index][1])

    def _are_keys_in_order(self, first_key, second_key):
        return (
            first_key >= second_key
            if self._reverse else first_key <= second_key
        )

    def _are_items_in_order(self, first_index, second_index):
        return self._are_keys_in_order(
            self._get_key_by_index(first_index),
            self._get_key_by_index(second_index),
        )

    def _swap(self, first_index, second_index):
        (
            first_item,
            second_item,
        ) = self._heap_items[first_index], self._heap_items[second_index]

        self._handle_to_position_mapping[first_item[0]] = second_index
        self._handle_to_position_mapping[second_item[0]] = first_index

        self._heap_items[first_index] = second_item
        self._heap_items[second_index] = first_item

    def _heapify_down(self, index):
        left_child = index * 2 + 1
        right_child = index * 2 + 2

        swap_position = (
            left_child if left_child < len(self._heap_items)
            and self._are_items_in_order(left_child, index)
            else index
        )

        swap_position = (
            right_child if right_child < len(self._heap_items)
            and self._are_items_in_order(right_child, swap_position)
            else swap_position
        )

        if swap_position != index:
            self._swap(index, swap_position)
            self._heapify_down(swap_position)

    def _heapify_up(self, item_index):
        parent = (item_index - 1) // 2
        while item_index > 0 and self._are_items_in_order(item_index, parent):
            self._swap(item_index, parent)
            item_index = parent
            parent = (item_index - 1) // 2

    def _create_heap(self):
        for it in reversed(range(0, len(self._heap_items) // 2)):
            self._heapify_down(it)


def sort(heap):
    """
    Perform heapsort.

    Auxiliary function that extracts top element from the heap
    and yields it. The sort order is defined by the order in the heap.

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
