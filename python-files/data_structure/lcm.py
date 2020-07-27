#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def gcd(a, b):
    while b:
        r = a % b
        a = b
        b = r
    return a


def lcm(a, b):
    return a*b // gcd(a, b)

