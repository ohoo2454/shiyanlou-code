#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def fibo(num):
    if num == 1:
        return 1
    elif num == 2:
        return 1
    elif num > 2:
        return fibo(num-1) + fibo(num-2)
    else:
        print("False")


l = [fibo(i) for i in range(1, 5)]
print(l)

