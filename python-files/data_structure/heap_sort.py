#!/usr/bin/env python3
#-*- utf-8 -*-

import random


def heap_sort(sequence):

    def heap_adjust(parent):
        child = 2*parent + 1
        while child < len(heap):
            if child+1 < len(heap):
                if heap[child+1] > heap[child]:
                    child = child + 1
            if heap[parent] >= heap[child]:
                break
            heap[parent], heap[child] = \
                heap[child], heap[parent]
            parent, child = child, 2*child + 1

    heap, sequence = sequence.copy(), []
    for i in range(len(heap)//2, -1, -1):
        heap_adjust(i)
    while len(heap) != 0:
        heap[0], heap[-1] = heap[-1], heap[0]
        sequence.insert(0, heap.pop())
        heap_adjust(0)
    return sequence


if __name__ == '__main__':
    sequence = [random.randint(1, 10000) for i in range(50)]
    print(sequence)
    print(heap_sort(sequence))

