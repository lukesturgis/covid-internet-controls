 
class AdjNode:
    def __init__(self, data):
        self.vertex = data
        self.next = None


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V

    # Add edges
    def add_edge(self, src, dest):
        node = AdjNode(dest)
        node.next = self.graph[src]
        self.graph[src] = node

#        node = AdjNode(src)
#        node.next = self.graph[dest]
#        self.graph[dest] = node

    # Print the graph
    def print_graph(self):
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i))
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex))
                temp = temp.next
            print(" \n")


as_array = []

with open("20200501_as_rel.txt") as fp: 
    V = 400000
    # Create graph and edges
    graph = Graph(V)

    for line in fp: 

	as_array = line.split('|')

	if as_array[2] == "-1\n": 
		graph.add_edge(int(as_array[0]), int(as_array[1]))

    graph.print_graph()

#ToDo:
#heavy hitter
#verfication of 90% internet is covered from heavy_hitter file


