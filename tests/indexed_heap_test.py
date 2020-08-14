import pytest

from indexed_heap import IndexedHeap, sort


def is_heap(items_to_check, start_position, compare_fn):
    """
    Determine if the collection is heap.

    Checks if `items_to_check[start_position:]` are in the heap-order
    according to relation defined by `compare_fn`

    Parameters
    ----------
    items_to_check : array_like
        array of items to check
    start_position : integer
        offset of items inside array to check
    compare_fn : callable
        comparator function defining order to check agains

    Returns
    -------
    boolean
        True if items are in heap order
    """
    left_child_index = start_position * 2 + 1
    right_child_index = start_position * 2 + 2

    is_heap_on_left = (
        is_heap(items_to_check, left_child_index, compare_fn)
        and compare_fn(
            items_to_check[start_position],
            items_to_check[left_child_index],
        )
    ) if left_child_index < len(items_to_check) else True

    is_heap_on_right = (
        is_heap(items_to_check, right_child_index, compare_fn)
        and compare_fn(
            items_to_check[start_position],
            items_to_check[right_child_index],
        )
    ) if right_child_index < len(items_to_check) else True

    return is_heap_on_left and is_heap_on_right


def test_utils_is_min_heap():
    items_to_check = [1, 2, 3, 4, 5, 6, 7, 8]
    assert is_heap(
        items_to_check,
        start_position=0,
        compare_fn=lambda first, second: first <= second,
    )


def test_utils_is_not_min_heap():
    items_to_check = [1, 2, 3, 4, 5, 6, 7, 2]
    assert not is_heap(
        items_to_check,
        start_position=0,
        compare_fn=lambda first,
        second: first <= second,
    )


def test_utils_single_item_is_min_heap():
    items_to_check = [1]
    assert is_heap(
        items_to_check,
        start_position=0,
        compare_fn=lambda first, second: first <= second,
    )


def are_sorted_heaps_equal(first_heap, second_heap):
    """
    Determine if the heaps produce identical sequences when heap-sorted.

    Applying sorting to two heaps and comparing output is the way to
    determine if two heaps are equivalent.

    As function continiously extracts elements from the heaps, the heaps
    will be emptied after function call

    Parameters
    ----------
    first_heap : IndexedHeap
        first heap to compare
    second_heap : IndexedHeap
        second heap to compare

    Returns
    -------
    bool
        True if two heaps produce identical sorted sequences
    """

    return [
        first_heap.pop_first() for _ in range(len(first_heap))
    ] == [
        second_heap.pop_first() for _ in range(len(second_heap))
    ]


def test_utils_are_sorted_heaps_equal():
    heap1 = IndexedHeap({1: 'A', 2: 'B'})
    heap2 = IndexedHeap({1: 'C', 2: 'D'})

    assert not are_sorted_heaps_equal(heap1, heap2)
    assert not list(heap1)
    assert not list(heap2)

    assert are_sorted_heaps_equal(
        IndexedHeap({1: 'A', 2: 'B'}),
        IndexedHeap({1: 'A', 2: 'B'}),
    )

    assert are_sorted_heaps_equal(
        IndexedHeap(),
        IndexedHeap(),
    )


def test_empty_heap_creation():
    heap = IndexedHeap()
    assert len(heap) == 0, 'The length should be equal to 0'
    assert len(heap) == len(heap.get_items(
    )), 'The length should be exact as the number of the stored elements'
    assert heap.pop_first() == (None, None), 'Pop oeration should return None'


def test_heap_len():
    heap = IndexedHeap()
    assert len(heap) == 0, 'Length of empty heap should be equal to 0'
    assert len(heap) == len(
        list(heap),
    ), 'The length should be exact the number of the stored elements'

    heap = IndexedHeap({1: 'A', 2: 'B'})
    assert len(heap) == 2, 'Heap length should be equal to 2'
    assert len(heap) == len(
        list(heap),
    ), 'The length should be exact the number of the stored elements'


def test_heap_check_key():
    test_values = {1: 'A', 2: 'B', 3: 'C'}
    heap = IndexedHeap(test_values)

    assert all(
        key in heap for key in test_values
    ), 'In operator should provide valid results'

    assert 6 not in heap, 'Value with key 6 should not be found'


def test_heap_get_item_via_index():
    test_values = {1: 4, 2: 2, 3: 3, 4: 1, 5: 5}

    heap = IndexedHeap(test_values)

    assert (
        heap[1], heap[2], heap[3], heap[4], heap[5],
    ) == (
        4, 2, 3, 1, 5,
    ), 'Items should be accessible via keys'

def test_heap_default_order():
    test_values = {1: 4, 2: 2, 3: 3, 4: 1, 5: 5}

    heap = IndexedHeap(test_values)
    assert is_heap(
        heap.get_items(),
        start_position=0,
        compare_fn=lambda first, second: first[1] <= second[1],
    ), 'Min heap should be created by default'

    assert (
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
    ) == (
        (4, 1), (2, 2), (3, 3), (1, 4), (5, 5),
    ), 'The items should be poped in sorted order'

def test_heap_reversed_order():
    test_values = {1: 4, 2: 2, 4: 1, 5: 5}
    heap = IndexedHeap(test_values, reverse=True)

    assert is_heap(
        heap.get_items(),
        start_position=0,
        compare_fn=lambda first, second: first[1] >= second[1],
    ), 'Max heap should be created'

    assert (
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
    ) == (
        (5, 5), (1, 4), (2, 2), (4, 1)  
    ), 'The items should be poped in sorted order'


def test_heap_update():
    test_values = {1: 'A', 2: 'B', 3: 'C'}

    heap = IndexedHeap()
    heap.update(test_values)
    assert are_sorted_heaps_equal(
        heap,
        IndexedHeap(test_values),
    ), 'Two heaps should be equal'

    heap.update(test_values)
    heap.update({3: 'X', 4: 'Z'})
    assert are_sorted_heaps_equal(
        heap,
        IndexedHeap({1: 'A', 2: 'B', 3: 'X', 4: 'Z'}),
    ), 'Two heaps should be equal'


def test_set_item_via_index():
    heap = IndexedHeap()
    heap[1] = 'A'
    heap[2] = 'B'
    heap[3] = 'C'
    assert are_sorted_heaps_equal(
        heap,
        IndexedHeap({1: 'A', 2: 'B', 3: 'C'}),
    ), 'Two heaps should be equal'

    heap[1] = 'A'
    heap[2] = 'B'
    heap[3] = 'C'
    heap[3] = 'X'
    assert are_sorted_heaps_equal(
        heap,
        IndexedHeap({1: 'A', 2: 'B', 3: 'X'}),
    ), 'Two heaps should be equal'

def test_heap_update_item_key_decreased():
    heap = IndexedHeap({1: 4, 2: 2, 3: 3, 4: 1, 5: 5})
    heap[5] = 0

    assert is_heap(
        heap.get_items(),
        start_position=0,
        compare_fn=lambda first, second: first[1] <= second[1],
    ), 'Min heap should be created by default'

    list(
        sort(heap),
    ) == [
        (5, 0), (4, 1), (2, 2), (3, 3), (1, 4),
    ], 'The items should be poped in sorted order'

def test_heap_delete_item():
    heap = IndexedHeap({1: 4, 2: 2, 3: 3, 4: 1, 5: 5})

    del heap[3]
    assert 3 not in heap, 'Key `3` should not be in the heap'
    assert are_sorted_heaps_equal(
        heap,
        IndexedHeap({1: 4, 2: 2, 4: 1, 5: 5}),
    ), 'Two heaps should be equal'


def test_heap_created_with_custom_key_second_value_used_as_key():
    class Value:
        def __init__(self, key):
            self.key = key

        def __eq__(self, other):
            return self.key == other.key

    heap = IndexedHeap(
        {
            1: Value(1),
            2: Value(2),
            3: Value(3),
            4: Value(4),
            5: Value(5),
        },
        key=lambda i: i.key,
    )

    assert is_heap(
        heap.get_items(),
        start_position=0,
        compare_fn=lambda first, second: first[1].key <= second[1].key
    ), 'Min heap should be created by default'

    assert (
        heap[1], heap[2], heap[3], heap[4], heap[5],
    ) == (
        Value(1), Value(2), Value(3), Value(4), Value(5),
    ), 'Items should be accessible via keys'

    list(
        sort(heap),
    ) == [
        (1, Value(1)),
        (2, Value(2)),
        (3, Value(3)),
        (4, Value(4)),
        (5, Value(5)),
    ], 'The items should be poped in sorted order'


def test_heap_sort():
    heap = IndexedHeap({1: 4, 2: 2, 3: 3, 4: 1, 5: 5})

    assert list(sort(heap)) == [(4, 1), (2, 2), (3, 3), (1, 4), (5, 5)]


def test_heap_iterator():
    heap = IndexedHeap({1: 4, 2: 2, 3: 3, 4: 1, 5: 5})

    iterated_items = [it for it in heap]

    assert iterated_items == heap.get_items(
    ), 'Iteration should be performed over all items in the heap order'
