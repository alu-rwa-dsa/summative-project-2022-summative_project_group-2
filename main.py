import math
import sys
import streamlit as st

class PriorityQueue:
    """
    Priority queue class where the array is sorted based on priority
    """

    def __init__(self):
        """
        Method/function for initializing the current size, creating
        array list and storing the position of the node in the array
        """
        self.current_size = 0
        self.array = []
        self.position = {}

    def isEmpty(self):
        """
        Method/function for a situation whereby the current size of the array is zero.
         i.e empty list/no info provided by the user
        :return: the current size as zero
        """
        return self.current_size == 0

    def min_heapify(self, element):
        """
        method of complete binary tree in which the value in each internal node is smaller than
        or equal to the values in the children of that node.
        :param element:
        :return:
        """
        leftChild = self.left(element)
        rightChild = self.right(element)
        if leftChild < self.current_size and self.array(leftChild)[0] < self.array(element)[0]:
            smallest = leftChild
        else:
            smallest = element
        if rightChild < self.current_size and self.array(rightChild)[0] < self.array(smallest)[0]:
            smallest = rightChild
        if smallest != element:
            self.swap(element, smallest)
            self.min_heapify(smallest)

    def insert(self, node):
        """
        method to insert node inside the priority queue
        :param node: node to be inserted
        :return:
        """
        self.position[node[1]] = self.current_size
        self.current_size += 1
        self.array.append((sys.maxsize, node[1]))
        self.decrease_key((sys.maxsize, node[1]), node[0])

    def extract_min(self):
        """

        :return: the minimum element at the top priority of the queue
        """
        min_node = self.array[0][1]
        self.array[0] = self.array[self.current_size - 1]
        self.current_size -= 1
        self.min_heapify(1)
        del self.position[min_node]
        return min_node

    def left(self, i):
        """

        :param i: index of the child node
        :return: the index of the left child node
        """
        return 2 * i + 1

    def right(self, i):
        """

        :param i: index of the child node
        :return: the index of the right child node
        """
        return 2 * i + 2

    def par(self, i):
        """

        :param i:
        :return: the index of the parent
        """
        return math.floor(i / 2)

    def swap(self, i, j):
        """
        excahnge the array elements at the indices
        :param i: first index
        :param j: second index
        :return: an updated position
        """
        self.position[self.array[i][1]] = j
        self.position[self.array[j][1]] = i
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp

    def decrease_key(self, node, new_d):
        element = self.position[node[1]]
        self.array[element] = (new_d, node[1])
        while element > 0 and self.array[self.par(element)][0] > self.array[element][0]:
            self.swap(element, self.par(element))
            element = self.par(element)


class Graph:
    def __init__(self, num):
        """
        function to store the graph that will be displayed and also store the distance from the vertices
        :param num: number of nodes in the graph
        """
        self.adjList = {}
        self.num_nodes = num
        self.dist = [0] * self.num_nodes
        self.par = [-1] * self.num_nodes  # To store the path

    def add_edge(self, u, v, w):
        """
        Function to add edge, its neighbor and weight. It also check if a node is already in the graph or not.
        Assumptions based on if the graph os directed or not is made in the last iteration
        :param u: starting edge
        :param v: destination edge
        :param w: weight, which will in this case considered as cost
        :return:
        """
        if u in self.adjList.keys():
            self.adjList[u].append((v, w))
        else:
            self.adjList[u] = [(v, w)]

        if v in self.adjList.keys():
            self.adjList[v].append((u, w))
        else:
            self.adjList[v] = [(u, w)]

    def show_graph(self):
        """
        Function to display the graph, from source node to its destination
        :return: print function is used in this case
        """
        for u in self.adjList:
            st.write( u, "->", " -> ".join(str(f"{v}({w})") for v, w in self.adjList[u]))

    def dijkstra(self, source_node):
        """
        shortest path considering the weight using dijkstra algorithm.
        0 is the distance from the source node(NB)
        Update the distance of all the neighbours of u and
        if their previous distance was INFINITY then push them in the Priority queue
        :param source_node: source node
        :return: Returns node with the minimum distance from source
        """
        self.par = [-1] * self.num_nodes
        self.dist[source_node] = 0
        Q = PriorityQueue()
        Q.insert((0, source_node))
        for u in self.adjList.keys():
            if u != source_node:
                self.dist[u] = sys.maxsize  # Infinity
                self.par[u] = -1

        while not Q.isEmpty():
            u = Q.extract_min()
            for v, w in self.adjList[u]:
                new_dist = self.dist[u] + w
                if self.dist[v] > new_dist:
                    if self.dist[v] == sys.maxsize:
                        Q.insert((new_dist, v))
                    else:
                        Q.decrease_key((self.dist[v], v), new_dist)
                    self.dist[v] = new_dist
                    self.par[v] = u

        self.show_distances(source_node)

    def show_distances(self, source_node):
        print(f"Distance from node: {source_node}")
        for u in range(self.num_nodes):
            print( f"Node {u} has distance: {self.dist[u]}")

    def show_path(self, source_node, dest):
        """
        Show shortest path from the source to destination. This is used after calling the dijkstra
        :param source_node:
        :param dest: destination node
        :return:
        """
        path = []
        cost = 0
        temp = dest
        # checking previous node
        while self.par[temp] != -1:
            path.append(temp)
            if temp != source_node:
                for v, w in self.adjList[temp]:
                    if v == self.par[temp]:
                        cost += w
                        break
            temp = self.par[temp]
        path.append(source_node)
        path.reverse()

        st.header(f"Shortest path from {source_node} to {dest}")
        for u in path:
            st.write(f"{u}", end=" ")
            if u != dest:
                st.write("↓", end="")

        return f"The minimal cost to transport data from {source_node} to {dest} is:  {cost}"

