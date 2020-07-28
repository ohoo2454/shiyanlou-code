#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math


def merge_sort(sequence):
    if (len(sequence) < 2):
        return sequence
    mid = math.floor(len(sequence)/2)
    left, right = sequence[0:mid], sequence[mid:]
    return merge(merge_sort(left), merge_sort(right))


def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


if __name__ == '__main__':
    sequence = [12, 27, 46, 16, 25, 37, 22, 29, 15, 47, 48, 34]
    print(sequence)
    print(merge_sort(sequence))

