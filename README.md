# indexed_heap

Python implelemtation of the binary heap supporting modification of the stored values

The component can be used as a priority queue in a range of tasks such as Dijkstra shortest path
algorithm 

## Introduction

The component provides functionality of the binary heap with an extension such as 
all items are referenced by the unique key (similar to dictionary). 
The heap can be constructed from a dictionary in a way that dictionary keys will be
used to reference items and the dictionary values will be used as keys for sorting in the heap.

The set of operations similar to those in dictionary (subscript, len, del, update)
is supported.

```python
# without provided key functor the dictionary values are used as keys for sorting
# as the reverse flag is not set the Min-heap will be constructed 
heap = IndexedHeap({1:4, 2:2, 3:3, 4:1, 5:5})
# the element with dictionary key 5 will be modified
heap[5] = 0
# value with key 4 will be updated and with the key 7 inserted (semantics similar to dictionary)
heap.update({4:10, 7:11})

# the item with minimum heap key (dictionary value will be extracted)
top_item = heap.pop_first()
```

The way how the key should be derived from the value can be controlled via optional
predecate that can be specified during heap creation.

```python
# the custom key function is used
class Value:
def __init__(self, key):
    self.key = key
    
heap = IndexedHeap({1:Value(1), 2:Value(2), 3:Value(3), 4:Value(4), 5:Value(5)}, key=lambda i: i.key)

```

Or with the help of the attrgetter or itemgetter from operator module

```python

from operator import attrgetter

heap = IndexedHeap({1:Value(1), 2:Value(2), 3:Value(3), 4:Value(4), 5:Value(5)}, key=attrgetter('key'))

```