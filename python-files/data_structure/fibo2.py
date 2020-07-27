#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def fibo(num):
    a, b = 1, 1
    l = []
    for _ in range(num):
        l.append(a)
        a, b = b, a + b
    return l


print(fibo(4))

