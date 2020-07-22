#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class heap(object):

    def __init__(self):
        self.data_list = []

    def get_parent_index(self, index):
        if index == 0 or index > len(self.data_list) - 1:
            return None
        else:
            return (index - 1) >> 1

    def swap(self, index_a, index_b):
        self.data_list[index_a], self.data_list[index_b] = self.data_list[index_b], self.data_list[index_a]

    def insert(self, data):
        self.data_list.append(data)
        index = len(self.data_list) - 1
        parent = self.get_parent_index(index)

        while parent is not None and self.data_list[parent] < self.data_list[index]:
            self.swap(parent, index)
            index = parent
            parent = self.get_parent_index(parent)

    def removeMax(self):
        remove_data = self.data_list[0]
        self.data_list[0] = self.data_list[-1]
        del self.data_list[-1]

        self.heapify(0)
        return remove_data

    def heapify(self, index):
        total_index = len(self.data_list) - 1
        while True:
            maxvalue_index = index
            if 2*index + 1 <= total_index and self.data_list[2*index + 1] > self.data_list[maxvalue_index]:
                maxvalue_index = 2*index + 1
            if 2*index + 2 <= total_index and self.data_list[2*index + 2] > self.data_list[maxvalue_index]:
                maxvalue_index = 2*index + 2
            if maxvalue_index == index:
                break
            self.swap(index, maxvalue_index)
            index = maxvalue_index


if __name__ == '__main__':
    myheap = heap()
    for i in range(10):
        myheap.insert(i+1)
    print('bulid heap: ', myheap.data_list)
    print('remove the top element of the heap: ', [myheap.removeMax() for _ in range(10)])

