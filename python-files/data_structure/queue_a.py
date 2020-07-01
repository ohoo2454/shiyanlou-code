#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class Queue():
    def __init__(self):
        self.entries = []
        self.length = 0
        self.front = 0

    def enqueue(self, item):
        self.entries.append(item)
        self.length = self.length + 1

    def dequeue(self):
        self.length = self.length - 1
        dequeued = self.entries[self.front]
        self.front -= 1
        self.entries = self.entries[self.front:]
        return dequeued

    def peek(self):
        return self.entries[0]

