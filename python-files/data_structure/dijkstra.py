#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import heapq

def dijkstra(graph, start, end):
    heap = [(0, start)]
    visited = []
    while heap:
        (cost, u) = heapq.heappop(heap)
        if u in visited:
            continue
        visited.append(u)
        if u == end:
            return cost
        for v, c in G[u]:
            if v in visited:
                continue
            next = cost + c
            heapq.heappush(heap, (next, v))
    return (-1, -1)

G = {'0': [['1', 2], ['2', 5]],
     '1': [['0', 2], ['3', 3], ['4', 1]],
     '2': [['0', 5], ['5', 3]],
     '3': [['1', 3]],
     '4': [['1', 1], ['5', 3]],
     '5': [['2', 3], ['4', 3]]}
shortDistance = dijkstra(G, '4', '2')
print(shortDistance)

