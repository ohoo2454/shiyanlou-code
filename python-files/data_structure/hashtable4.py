#!/usr/bin/env python3
#-*- coding: utf-8 -*-


class hashtable(object):

    def __init__(self):
        self.capacity = 10
        self.hash_table = [[None, None] for i in range(self.capacity)]
        self.num = 0
        self.load_factor = 0.75

    def hash(self, k, i):
        h_value = (k+i) % self.capacity
        if self.hash_table[h_value][0] == k:
            return h_value
        if self.hash_table[h_value][0] != None:
            i += 1
            h_value = self.hash(k, i)
        return h_value

    def resize(self):
        self.capacity = self.num * 2
        temp = self.hash_table[:]
        self.hash_table = [[None, None] for i in range(self.capacity)]
        for i in temp:
            if (i[0] != None):
                hash_v = self.hash(i[0], 0)
                self.hash_table[hash_v][0] = i[0]
                self.hash_table[hash_v][1] = i[1]

    def put(self, k, v):
        hash_v = self.hash(k, 0)
        self.hash_table[hash_v][0] = k
        self.hash_table[hash_v][1] = v
        self.num = self.num + 1
        if (self.num/len(self.hash_table) > self.load_factor):
            self.resize()

    def get(self, k):
        hash_v = self.hash(k, 0)
        return self.hash_table[hash_v][1]


table = hashtable()
for i in range(1, 13):
    table.put(i, i)
print(table.get(3))
print(table.hash_table)

