#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import random


def partition(sequence, left, right, pivot_index):
    pivot_value = sequence[pivot_index]
    sequence[pivot_index], sequence[right] = sequence[right], sequence[pivot_index]
    store_index = left
    for i in range(left, right):
        if sequence[i] < pivot_value:
            sequence[store_index], sequence[i] = sequence[i], sequence[store_index]
            store_index = store_index + 1
    sequence[store_index], sequence[right] = sequence[right], sequence[store_index]
    return store_index


def quick_search(sequence, left, right, k):
    if left == right:
        return sequence[left]
    pivot_index = left + random.randint(0, right-left+1)
    pivot_index = partition(sequence, left, right, pivot_index)
    if k == pivot_index:
        return sequence[k]
    elif k < pivot_index:
        return quick_search(sequence, left, pivot_index-1, k)
    else:
        return quick_search(sequence, pivot_index+1, right, k)


if __name__ == '__main__':
    sequence = [12, 1, 21, 34, 25, 15, 35, 13, 45, 100, 234, 521, 345, 16, 1314]
    left = 0
    right = len(sequence) - 1
    k = int(input("Find the k'th smallest number in sequence, k=")) - 1
    value = quick_search(sequence, left, right, k)
    print("The %s'th smallest number in sequence is: %s" % (k+1, value))

