#!/usr/bin/env python3
#-*- coding: utf-8 -*-


class hashtable(object):

    def __init__(self):
        self.items = [None] * 100

    def hash(self, a):
        return a*1 + 1

    def put(self, k, v):
        self.items[self.hash(k)] = v

    def get(self, k):
        hashcode = self.hash(k)
        return self.items[hashcode]

