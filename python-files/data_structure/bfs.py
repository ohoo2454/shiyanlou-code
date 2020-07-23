#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def bfs(graph, start):
    explored, queue = [], [start]
    explored.append(start)
    while queue:
        v = queue.pop(0)
        for w in graph[v]:
            if w not in explored:
                explored.append(w)
                queue.append(w)
    return explored

G = {'0': ['1', '2'],
     '1': ['2', '3'],
     '2': ['3', '5'],
     '3': ['4'],
     '4': [],
     '5': []}

print(bfs(G, '0'))

