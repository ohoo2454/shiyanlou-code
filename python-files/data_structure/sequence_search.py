#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def sequencesearch(sequence, target):
    for i in range(len(sequence)):
        if target == sequence[i]:
            return i
    return None


if __name__ == '__main__':
    sequence = [99, 12, 33, 74, 521, 13, 14]
    target = 521
    i = sequencesearch(sequence, target)
    print(i)

