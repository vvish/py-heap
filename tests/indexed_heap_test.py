import pytest
from indexed_heap import IndexedHeap, sort

def is_heap(items, start_position, compare_fn):
    """
    Helper function to check if `items[start_position:]` are in the heap-order according to relation defined by `compare_fn`
    """
    left_child_index = start_position * 2 + 1
    right_child_index = start_position * 2 + 2

    is_heap_on_left = is_heap(items, left_child_index, compare_fn) and compare_fn(
        items[start_position], items[left_child_index]) if left_child_index < len(items) else True
    is_heap_on_right = is_heap(items, right_child_index, compare_fn) and compare_fn(
        items[start_position], items[right_child_index]) if right_child_index < len(items) else True

    return is_heap_on_left and is_heap_on_right

def test_utils_is_min_heap():
    items = [1, 2, 3, 4, 5, 6, 7, 8]
    assert is_heap(items, start_position=0, compare_fn = lambda first, second: first <= second)

def test_utils_is_not_min_heap():
    items = [1, 2, 3, 4, 5, 6, 7, 2]
    assert not is_heap(items, start_position=0, compare_fn = lambda first, second: first <= second)

def test_utils_single_item_is_min_heap():
    items = [1]
    assert is_heap(items, start_position=0, compare_fn = lambda first, second: first <= second)

def test_empty_heap_creation():
    heap = IndexedHeap()
    assert len(heap) == len(heap.items()) and len(heap) == 0, "The length should be exact as the number of the stored elements, and be equal to 0"
    assert heap.pop_first() == (None, None), "Pop oeration should return None"

def test_heap_created_with_default_parameters_items_added_via_update():
    heap = IndexedHeap()
    heap.update({1:4, 2:2, 3:3, 4:1, 5:5})
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 3 and heap[4] == 1 and heap[5] == 5, "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(4, 1), (2, 2), (3, 3), (1, 4), (5, 5)], "The items should be poped in sorted order"

def test_heap_created_with_default_parameters_items_added_via_subscript():
    heap = IndexedHeap()
    
    heap[1] = 4
    heap[2] = 2
    heap[3] = 3
    heap[4] = 1
    heap[5] = 5
        
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 3 and heap[4] == 1 and heap[5] == 5, "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(4, 1), (2, 2), (3, 3), (1, 4), (5, 5)], "The items should be poped in sorted order"


def test_heap_created_with_default_parameters_and_items_specified_in_init():
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 3 and heap[4] == 1 and heap[5] == 5, "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(4, 1), (2, 2), (3, 3), (1, 4), (5, 5)], "The items should be poped in sorted order"

def test_heap_created_with_reversed_orders_and_items_specified_in_init():
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5}, reverse=True)
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] >= second[1]),  "Max heap should be created"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 3 and heap[4] == 1 and heap[5] == 5, "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(5, 5), (1, 4), (3, 3), (2, 2), (4, 1)], "The items should be poped in sorted order"

def test_heap_item_is_updated_via_subscript_heap_reordered():
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})
    heap[4] = 10
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 3 and heap[4] == 10 and heap[5] == 5, "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(2, 2), (3, 3), (1, 4), (5, 5), (4, 10)], "The items should be poped in sorted order"

def test_heap_items_are_updated_via_update_heap_reordered():
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})
    heap.update({4:10, 3:11})
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 11 and heap[4] == 10 and heap[5] == 5, "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(2, 2), (1, 4), (5, 5), (4, 10), (3, 11)], "The items should be poped in sorted order"

def test_heap_item_is_updated_via_subscript_key_decreased_heap_reordered():
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})
    heap[5] = 0
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 3 and heap[4] == 1 and heap[5] == 0, "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(5, 0), (4, 1), (2, 2), (3, 3), (1, 4)], "The items should be poped in sorted order"

def test_heap_created_item_delete():
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == 4 and heap[2] == 2 and heap[3] == 3 and heap[4] == 1 and heap[5] == 5, "Items should be accessible via keys"
    
    del heap[3]

    assert len(heap) == len(heap.items()) and len(heap) == 4, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1] <= second[1]),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert 3 not in heap, "Key `3` should not be in the heap"
    assert heap[1] == 4 and heap[2] == 2 and heap[4] == 1 and heap[5] == 5, "Items should be accessible via keys"
    
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(4, 1), (2, 2), (1, 4), (5, 5)], "The items should be poped in sorted order"

def test_heap_created_with_custom_key_second_value_used_as_key():
    class Value:
        def __init__(self, key):
            self.key = key
        def __eq__(self, other):
            return self.key == other.key
        
    heap = IndexedHeap({1:Value(1), 2:Value(2), 3:Value(3), 4:Value(4), 5:Value(5)}, key=lambda i: i.key)
    
    assert len(heap) == len(heap.items()) and len(heap) == 5, "The length should be exact as the number of the stored elements"
    assert is_heap(heap.items(), start_position=0, compare_fn = lambda first, second: first[1].key <= second[1].key),  "Min heap should be created by default"
    assert 1 in heap and 2 in heap and 3 in heap and 4 in heap and 5 in heap, "In operator should provide valid results"
    assert heap[1] == Value(1) and heap[2] == Value(2) and heap[3] == Value(3) and heap[4] == Value(4) and heap[5] == Value(5), "Items should be accessible via keys"
    assert [heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first(), heap.pop_first()] == [(1, Value(1)), (2, Value(2)), (3, Value(3)), (4, Value(4)), (5, Value(5))], "The items should be poped in sorted order"

def test_sort():
    heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})

    assert list(sort(heap)) == [(4, 1), (2, 2), (3, 3), (1, 4), (5, 5)]
