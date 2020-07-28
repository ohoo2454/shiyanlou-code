#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def insertion_sort(sequence):
    for index in range(1, len(sequence)):
        while (index>0 and sequence[index-1]>sequence[index]):
            sequence[index], sequence[index-1] = sequence[index-1], sequence[index]
            index = index - 1
    return sequence

