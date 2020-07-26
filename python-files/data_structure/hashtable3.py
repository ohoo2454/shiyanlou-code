#!/usr/bin/env python3
#-*- coding: utf-8 -*-


class hashtable(object):

    def __init__(self):
        self.hash_table = [[None, None] for i in range(10)]

    def hash(self, k, i):
        h_value = (k+i) % 10
        if self.hash_table[h_value][0] == k:
            return h_value
        if self.hash_table[h_value][0] != None:
            i = i + 1
            h_value = self.hash(k, i)
        return h_value

    def put(self, k, v):
        hash_v = self.hash(k, 0)
        self.hash_table[hash_v][0] = k
        self.hash_table[hash_v][1] = v

    def get(self, k):
        hash_v = self.hash(k, 0)
        return self.hash_table[hash_v][1]

table = hashtable()
for i in range(9):
    table.put(i, i)
print(table.get(3))
print(table.hash_table)

