# A-Algorithm-
A* (pronounced "A-star") is a graph traversal and pathfinding algorithm, which is used in many fields of computer science due to its completeness, optimality, and optimal efficiency.[1] Given a weighted graph, a source node and a goal node, the algorithm finds the shortest path (with respect to the given weights) from source to goal.

One major practical drawback is its 
O(bd)
{\displaystyle O(b^{d})} space complexity where d is the depth of the solution (the length of the shortest path) and b is the branching factor (the average number of successors per state), as it stores all generated nodes in memory. Thus, in practical travel-routing systems, it is generally outperformed by algorithms that can pre-process the graph to attain better performance,[2] as well as by memory-bounded approaches; however, A* is still the best solution in many cases.[3]
