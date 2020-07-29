#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def brute_force_match(t, p):
    tlen = len(t)
    plen = len(p)
    for i in range(tlen):
        j = 0
        while t[i+j]==p[j] and j<plen:
            j = j+1
            if j == plen:
                return i
    return -1

