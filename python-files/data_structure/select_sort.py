#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def select_sort(sequence):
    for i in range(len(sequence)-1):
        minIndex = i
        for j in range(i+1, len(sequence)):
            if sequence[j] < sequence[minIndex]:
                minIndex = j
        sequence[minIndex], sequence[i] = sequence[i], sequence[minIndex]
    return sequence

