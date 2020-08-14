import copy

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


def test_empty_heap_creation():
    heap = IndexedHeap()
    assert len(heap) == 0, 'The length should be equal to 0'
    assert len(heap) == len(heap.get_items(
    )), 'The length should be exact as the number of the stored elements'
    assert heap.pop_first() == (None, None), 'Pop oeration should return None'


def test_heap_eq_neq():
    empty_heap1 = IndexedHeap()
    empty_heap2 = IndexedHeap()
    not_empty_heap1 = IndexedHeap({1: 2})
    not_empty_heap2 = IndexedHeap({1: 2, 3: 4})

    assert empty_heap1 is not empty_heap2, 'Two heaps are not the same object'
    assert empty_heap1 == empty_heap2, 'Two empty heaps should be equal'
    assert empty_heap1 != not_empty_heap1, 'Two heaps are not equal'
    assert not_empty_heap1 != not_empty_heap2, 'Two heaps are not equal'


class DefaultHeapFixture(object):
    test_values = {1: 4, 2: 2, 3: 3, 4: 1, 5: 5}

    def validate(self, heap):
        self.validate_default_length(heap)
        self.validate_items_presense(heap)
        self.validate_default_order(heap)

        heap_copy = copy.deepcopy(heap)
        self.validate_default_extraction(heap_copy)

    def validate_default_length(self, heap):
        assert len(heap) == 5, 'The length should be equal to 5'
        assert len(heap) == len(heap.get_items(
        )), 'The length should be exact as the number of the stored elements'

    def validate_items_presense(self, heap):
        assert all(
            key in heap for key in self.test_values.keys()
        ), 'In operator should provide valid results'
        assert (
            heap[1], heap[2], heap[3], heap[4], heap[5],
        ) == (
            4, 2, 3, 1, 5,
        ), 'Items should be accessible via keys'

    def validate_default_order(self, heap):
        assert is_heap(
            heap.get_items(),
            start_position=0,
            compare_fn=lambda first, second: first[1] <= second[1],
        ), 'Min heap should be created by default'

    def validate_reversed_order(self, heap):
        assert is_heap(
            heap.get_items(),
            start_position=0,
            compare_fn=lambda first, second: first[1] >= second[1],
        ), 'Max heap should be created'

    def validate_default_extraction(self, heap):
        assert (
            heap.pop_first(),
            heap.pop_first(),
            heap.pop_first(),
            heap.pop_first(),
            heap.pop_first(),
        ) == (
            (4, 1), (2, 2), (3, 3), (1, 4), (5, 5),
        ), 'The items should be poped in sorted order'


@pytest.fixture
def default_heap_fixture():
    return DefaultHeapFixture()


def test_heap_items_added_via_update(default_heap_fixture):
    heap = IndexedHeap()
    heap.update(default_heap_fixture.test_values)

    default_heap_fixture.validate(heap)


def test_heap_items_added_via_subscript(default_heap_fixture):
    heap = IndexedHeap()

    for k, v in default_heap_fixture.test_values.items():
        heap[k] = v

    default_heap_fixture.validate(heap)


def test_heap_items_specified_in_init(default_heap_fixture):
    heap = IndexedHeap(default_heap_fixture.test_values)
    default_heap_fixture.validate(heap)


def test_heap_reversed_and_items_specified_in_init(default_heap_fixture):
    heap = IndexedHeap(default_heap_fixture.test_values, reverse=True)

    default_heap_fixture.validate_default_length(heap)
    default_heap_fixture.validate_items_presense(heap)

    default_heap_fixture.validate_reversed_order(heap)

    assert (
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
    ) == (
        (5, 5), (1, 4), (3, 3), (2, 2), (4, 1),
    ), 'The items should be poped in sorted order'


class UpdatedHeapFixture(DefaultHeapFixture):
    updated_values = {4: 10, 3: 11}

    def validate_updated(self, heap):
        self.validate_default_length(heap)
        self.validate_default_order(heap)

        assert all(
            key in heap for key in self.test_values.keys()
        ), 'In operator should provide valid results'

        assert (
            heap[1], heap[2], heap[3], heap[4], heap[5],
        ) == (
            4, 2, 11, 10, 5,
        ), 'Items should be accessible via keys'

        assert (
            heap.pop_first(),
            heap.pop_first(),
            heap.pop_first(),
            heap.pop_first(),
            heap.pop_first(),
        ) == (
            (2, 2), (1, 4), (5, 5), (4, 10), (3, 11),
        ), 'The items should be poped in sorted order'


@pytest.fixture
def update_test_fixture():
    return UpdatedHeapFixture()


def test_heap_item_is_updated_via_subscript(update_test_fixture):
    heap = IndexedHeap(update_test_fixture.test_values)

    for k, v in update_test_fixture.updated_values.items():
        heap[k] = v

    update_test_fixture.validate_updated(heap)


def test_heap_is_updated_via_update_heap_reordered(update_test_fixture):
    heap = IndexedHeap(update_test_fixture.test_values)
    heap.update(update_test_fixture.updated_values)

    update_test_fixture.validate_updated(heap)


def test_heap_is_updated_via_subscript_key_decreased(default_heap_fixture):
    heap = IndexedHeap({1: 4, 2: 2, 3: 3, 4: 1, 5: 5})
    heap[5] = 0

    default_heap_fixture.validate_default_length(heap)
    default_heap_fixture.validate_default_order(heap)

    assert all(
        key in heap for key in default_heap_fixture.test_values.keys()
    ), 'In operator should provide valid results'

    assert (
        heap[1], heap[2], heap[3], heap[4], heap[5],
    ) == (
        4, 2, 3, 1, 0,
    ), 'Items should be accessible via keys'

    assert (
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
    ) == (
        (5, 0), (4, 1), (2, 2), (3, 3), (1, 4),
    ), 'The items should be poped in sorted order'


def test_heap_item_delete(default_heap_fixture):
    heap = IndexedHeap(default_heap_fixture.test_values)

    del heap[3]

    assert len(heap) == 4, 'The length after delete should be equal to 5'
    assert len(heap) == len(heap.get_items(
    )), 'The length should be exact as the number of the stored elements'

    default_heap_fixture.validate_default_order(heap)

    assert all(
        key in heap for key in (1, 2, 4, 5)
    ), 'In operator should provide valid results'
    assert 3 not in heap, 'Key `3` should not be in the heap'

    assert (
        heap[1], heap[2], heap[4], heap[5],
    ) == (
        4, 2, 1, 5,
    ), 'Items should be accessible via keys'

    assert (
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
    ) == (
        (4, 1), (2, 2), (1, 4), (5, 5),
    ), 'The items should be poped in sorted order'

    assert len(heap) == 0, 'The length after poping items should be equal to 5'


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

    assert len(heap) == 5, 'The length should be equal to 5'
    assert len(heap) == len(heap.get_items(
    )), 'The length should be exact as the number of the stored elements'
    assert is_heap(
        heap.get_items(),
        start_position=0,
        compare_fn=lambda first, second: first[1].key <= second[1].key
    ), 'Min heap should be created by default'

    assert all(
        key in heap for key in (1, 2, 3, 4, 5)
    ), 'In operator should provide valid results'

    assert (
        heap[1], heap[2], heap[3], heap[4], heap[5],
    ) == (
        Value(1), Value(2), Value(3), Value(4), Value(5),
    ), 'Items should be accessible via keys'

    assert (
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
        heap.pop_first(),
    ) == (
        (1, Value(1)),
        (2, Value(2)),
        (3, Value(3)),
        (4, Value(4)),
        (5, Value(5)),
    ), 'The items should be poped in sorted order'


def test_sort():
    heap = IndexedHeap({1: 4, 2: 2, 3: 3, 4: 1, 5: 5})

    assert list(sort(heap)) == [(4, 1), (2, 2), (3, 3), (1, 4), (5, 5)]


def test_iterator():
    heap = IndexedHeap({1: 4, 2: 2, 3: 3, 4: 1, 5: 5})

    iterated_items = [it for it in heap]

    assert iterated_items == heap.get_items(
    ), 'Iteration should be performed over all items in the heap order'
