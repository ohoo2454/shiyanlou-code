#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math


def jumpsearch(sorted_sequence, target):
    n = len(sorted_sequence)
    step = int(math.floor(math.sqrt(n)))
    prev = 0
    while sorted_sequence[min(step, n)-1] < target:
        prev = step
        step = step + int(math.floor(math.sqrt(n)))
        if prev >= n:
            return None
    while sorted_sequence[prev] < target:
        prev = prev + 1
        if prev == min(step, n):
            return None
    if sorted_sequence[prev] == target:
        return prev
    else:
        return None


if __name__ == '__main__':
    sorted_sequence = [i for i in range(1, 10001, 2)]
    target = 521
    index = jumpsearch(sorted_sequence, target)
    print(index)

