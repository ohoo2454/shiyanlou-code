#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def fibo(num):
    if num == 1:
        return [1]
    elif num == 2:
        return [1, 1]
    l = [1, 1]
    for i in range(2, num):
        l.append(l[-2] + l[-1])
    return l


print(fibo(4))

