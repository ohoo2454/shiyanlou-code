#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import math

def find_prime_2(num):
    primes_bool = [False, False] + [True]*(num-1)
    for i in range(3, len(primes_bool)):
        if i%2 == 0:
            primes_bool[i] = False
    for i in range(3, int(math.sqrt(num))+1):
        if primes_bool[i] is True:
            for j in range(i+i, num+1, i):
                primes_bool[j] = False
    prims = []
    for i, v in enumerate(primes_bool):
        if v is True:
            prims.append(i)
    return prims

print(find_prime_2(100))

