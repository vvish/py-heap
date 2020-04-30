from indexed_heap import IndexedHeap, sort

def add_symetric_edge(adj_list, node_from, node_to, weight):
    adj_list.setdefault(node_from, []).append((node_to, weight))
    adj_list.setdefault(node_to, []).append((node_from, weight))

def get_edges_from(adj_list, node_from):
    if node_from not in adj_list:
        return ()
    else:
        return ((e[0], e[1]) for e in adj_list[node_from])

def get_nodes(adj_list):
    nodes = set()
    
    for node, edges in adj_list.items():
        nodes.add(node)
        nodes.update([e[0] for e in edges])

    return list(nodes)

def dijkstra_shortest_paths(adj_list, node_from, infinity_value=0xFFFFFFFF):
    distances = {k: infinity_value for k in get_nodes(adj_list)}
    distances[node_from] = 0

    visit_queue = IndexedHeap(distances)
        
    next_edge, distance = visit_queue.pop_first()
    while next_edge is not None:
        for edge in get_edges_from(adj_list, next_edge):
            if edge[0] in visit_queue and (distances[edge[0]] > distance + edge[1]):
                distances[edge[0]] = distance + edge[1]
                visit_queue.update({edge[0]:distances[edge[0]]}) 
        next_edge, distance = visit_queue.pop_first()

    return distances

if __name__ == '__main__':

    #  Graph from https://commons.wikimedia.org/wiki/File:Dijkstra_graph0.PNG
    #  Distances are (1,2) = 7, (1,3) = 9, (1,4) = 20, (1,5) = 20, (1,6) = 11

    graph = {}
    add_symetric_edge(graph, 1, 2, 7)
    add_symetric_edge(graph, 1, 6, 14)
    add_symetric_edge(graph, 1, 3, 9)
    
    add_symetric_edge(graph, 2, 3, 10)
    add_symetric_edge(graph, 2, 4, 15)

    add_symetric_edge(graph, 3, 6, 2)
    add_symetric_edge(graph, 3, 4, 11)

    add_symetric_edge(graph, 5, 6, 9)
    add_symetric_edge(graph, 5, 4, 6)
  
    distances = dijkstra_shortest_paths(graph, 1)

    for d in distances.items():
        print ("d(1,{}) = {}".format(d[0], d[1]))