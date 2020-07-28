#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def ternary_search(sorted_sequence, target):
    left = 0
    right = len(sorted_sequence) - 1
    while (left <= right):
        Third1 = (right-left)//3 + left
        Third2 = 2*(right+left)//3 + left
        if (sorted_sequence[Third1] == target):
            return Third1
        elif (sorted_sequence[Third2] == target):
            return Third2
        elif (target < sorted_sequence[Third1]):
            right = Third1 - 1
        elif (target > sorted_sequence[Third2]):
            left = Third2 + 1
        else:
            left = Third1 + 1
            right = Third2 - 1
    return None

