#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def intersection(function, start1, start2):
    x_n = start1
    x_n1 = start2
    while True:
        x_n2 = x_n1 - (function(x_n1) /
                        ((function(x_n1) - function(x_n)) / (x_n1-x_n)))
        if abs(x_n2 - x_n1) < 10**-5:
            return x_n2
        x_n = x_n1
        x_n1 = x_n2


def f(x):
    return (x**3) - 2*x - 5


if __name__ == '__main__':
    print(intersection(f, 3, 3.5))

