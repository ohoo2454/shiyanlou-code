#!/usr/bin/env python3
#-*- coding: utf-8 -*-


class Graph(object):

    def __init__(self, vertex):
        self.vertex = vertex
        self.graph = [[0] * vertex for i in range(vertex)]

    def insert(self, u, v):
        self.graph[u-1][v-1] = 1
        self.graph[v-1][u-1] = 1

    def show(self):
        for i in self.graph:
            for j in i:
                print(j, end=' ')
            print(' ')


graph = Graph(5)
graph.insert(1, 4)
graph.insert(4, 2)
graph.insert(4, 5)
graph.insert(2, 5)
graph.insert(5, 3)
graph.show()

