# IndexedHeap

Python implementation of the binary heap supporting random access and
modification of the stored values.

The component can be used as a priority queue in various applications
such as scheduling or Dijkstra shortest path algorithm.

## Introduction

The container maintains a binary heap of the elements with an extension
such that each heap element has an associated unique key that is used for
referencing the element.
The ordering in the heap is defined only by the values of the heap
elements either by default comparison or user provided predicate.
To access the heap items using keys the set of operations similar to
those in the dictionary (subscript, len, del, update) is supported.

The heap can be constructed from a dictionary directly in a way that
dictionary values will be used as heap elements and dictionary keys will
be used to reference heap items.


```python
# without user-provided key functor the dictionary values are used as
# keys for sorting
# if the 'reverse' flag is not set the Min-heap will be constructed
heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})
# the element with dictionary key 5 will be modified and heap will be
# reordered
heap[5] = 0
# value with key 4 will be updated and with the key 7 inserted
# (semantics similar to dictionary)
heap.update({4:10, 7:11})

# the item with minimum heap key will be extracted
# here the item with value 0 and dictionary key 5
top_item = heap.pop_first()
```

The way how the heap key should be derived from the value can
be specified via optional predicate passed during heap initialization.

```python
# the custom key function should be used
class Value:
    def __init__(self, key):
        self.key = key
    
heap = IndexedHeap(
        { 1:Value(1), 2:Value(2), 3:Value(3), 4:Value(4), 5:Value(5) }, 
        key=lambda i: i.key,
    )

```

Or with the help of the attrgetter or itemgetter from operator module.

```python

from operator import attrgetter

heap = IndexedHeap(
        { 1:Value(1), 2:Value(2), 3:Value(3), 4:Value(4), 5:Value(5) }, 
        key=attrgetter('key'),
    )

```