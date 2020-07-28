#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def insert_search(sorted_sequence, target):
    left = 0
    right = len(sorted_sequence) - 1
    while (left <= right):
        midpoint = left + ((target-sorted_sequence[left])*(right-left))//(
                sorted_sequence[right]-sorted_sequence[left])
        if midpoint < 0 or midpoint >= len(sorted_sequence):
            return None
        current_item = sorted_sequence[midpoint]
        if current_item == target:
            return midpoint
        elif target < current_item:
            right = midpoint - 1
        else:
            left = midpoint + 1
    return None

