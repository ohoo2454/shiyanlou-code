#!/usr/bin/env python3
#-*- coding: utf-8 -*-


class hashtable(object):

    def __init__(self):
        self.items = []

    def put(self, k, v):
        self.items.append((k, v))

    def get(self, k):
        for key, value in self.items:
            if (k == key):
                return value

