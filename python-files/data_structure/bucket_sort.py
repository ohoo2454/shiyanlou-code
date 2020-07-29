#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math
import random
DEFAULT_BUCKET_SIZE = 5


def insertion_sort(sequence):
    for index in range(1, len(sequence)):
        while (index>0 and sequence[index-1]>sequence[index]):
            sequence[index], sequence[index-1] = sequence[index-1], sequence[index]
            index = index - 1
    return sequence


def bucket_sort(sequence, bucketSize=DEFAULT_BUCKET_SIZE):
    if (len(sequence) == 0):
        return []
    minValue = sequence[0]
    maxValue = sequence[0]
    for i in range(0, len(sequence)):
        if sequence[i] < minValue:
            minValue = sequence[i]
        elif sequence[i] > maxValue:
            maxValue = sequence[i]
    bucketCount = math.floor((maxValue-minValue)/bucketSize) + 1
    buckets = []
    for i in range(0, bucketCount):
        buckets.append([])
    for i in range(0, len(sequence)):
        buckets[math.floor((sequence[i]-minValue)/bucketSize)].append(sequence[i])

    sortedArray = []
    for i in range(0, len(buckets)):
        insertion_sort(buckets[i])
        for j in range(0, len(buckets[i])):
            sortedArray.append(buckets[i][j])
    return sortedArray


if __name__ == '__main__':
    sequence = [random.randint(1, 10000) for i in range(50)]
    print(sequence)
    print(bucket_sort(sequence))

