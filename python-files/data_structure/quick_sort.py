#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def quick_select(sequence):

    def recursive(begin, end):
        if begin > end:
            return
        left, right = begin, end
        pivot = sequence[left]
        while left < right:
            while left < right and sequence[right] > pivot:
                right = right - 1
            while left < right and sequence[left] <= pivot:
                left = left + 1
            sequence[left], sequence[right] = sequence[right], sequence[left]
            # print(sequence)
        sequence[left], sequence[begin] = pivot, sequence[left]
        # print(sequence)
        # print(sequence[begin])
        # print(sequence[left])
        # print(begin)
        # print(left)
        recursive(begin, left-1)
        recursive(right+1, end)

    recursive(0, len(sequence)-1)
    return sequence


if __name__ == '__main__':
    sequence = [1, 3, 2, 1, 4, 0, 9, 6, 5, 3, 10]
    print(sequence)
    print(quick_select(sequence))

