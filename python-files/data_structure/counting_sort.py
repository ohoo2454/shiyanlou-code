#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import random


def counting_sort(sequence):
    if sequence == []:
        return []
    sequence_len = len(sequence)
    sequence_max = max(sequence)
    sequence_min = min(sequence)
    counting_arr_length = sequence_max - sequence_min + 1
    counting_arr = [0] * counting_arr_length
    for number in sequence:
        counting_arr[number-sequence_min] += 1
    for i in range(1, counting_arr_length):
        counting_arr[i] = counting_arr[i] + counting_arr[i-1]
    ordered = [0] * sequence_len
    for i in range(sequence_len-1, -1, -1):
        ordered[counting_arr[sequence[i]-sequence_min]-1] = sequence[i]
        counting_arr[sequence[i]-sequence_min] -= 1
    return ordered


if __name__ == '__main__':
    sequence = [random.randint(1, 10000) for i in range(50)]
    print(sequence)
    print(counting_sort(sequence))

