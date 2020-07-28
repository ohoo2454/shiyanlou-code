#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def shell_sort(sequence):
    gap = len(sequence)
    while gap > 1:
        gap = gap // 2
        for i in range(gap, len(sequence)):
            for j in range(i%gap, i, gap):
                if sequence[i] < sequence[j]:
                    sequence[i], sequence[j] = sequence[j], sequence[i]
    return sequence

