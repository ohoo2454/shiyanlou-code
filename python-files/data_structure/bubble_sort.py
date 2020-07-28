#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def bubble_sort(sequence):
    for i in range(1, len(sequence)):
        for j in range(0, len(sequence)-i):
            if sequence[j] > sequence[j+1]:
                sequence[j], sequence[j+1] = sequence[j+1], sequence[j]
    return sequence


if __name__ == '__main__':
    sequence = [12, 27, 46, 16, 25, 37, 22, 29, 15, 47, 48, 34]
#    for i in bubble_sort(sequence):
#        print(i)
    print(bubble_sort(sequence))

