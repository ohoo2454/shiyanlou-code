#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def binarysearch(sorted_sequence, target):
    left = 0
    right = len(sorted_sequence) - 1
    while (left <= right):
        midpoint = (left+right) // 2
        current_item = sorted_sequence[midpoint]
        if current_item == target:
            return midpoint
        elif target < current_item:
            right = midpoint - 1
        else:
            left = midpoint + 1
    return None


if __name__ == '__main__':
    target = 521
    sequence = []
    for i in range(1, 1000):
        if i % 2 == 1:
            sequence.append(i)
    print(binarysearch(sequence, target))

