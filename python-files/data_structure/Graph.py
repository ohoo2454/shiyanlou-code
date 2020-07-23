#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Graph(object):

    def __init__(self):
        self.nodes = []
        self.edge = {}

    def insert(self, a, b):
        if not(a in self.nodes):
            self.nodes.append(a)
            self.edge[a] = list()
        if not(b in self.nodes):
            self.nodes.append(b)
            self.edge[b] = list()
        self.edge[a].append(b)
        self.edge[b].append(a)

    def succ(self, a):
        return self.edge[a]

    def show_nodes(self):
        return self.nodes

    def show_edge(self):
        print(self.edge)


graph = Graph()
graph.insert('0', '1')
graph.insert('0', '2')
graph.insert('0', '3')
graph.insert('1', '3')
graph.insert('2', '3')
graph.show_edge()

