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


def three_gcd(a, b, c):
    t1 = gcd(a, b)
    t2 = gcd(t1, c)
    return t2


def three_lcm(a, b, c):
    t1 = lcm(a, b)
    t2 = lcm(t1, c)
    return t2


def main():
    a = 2
    b = 7
    c = 6
    print("a: ", a)
    print("b: ", b)
    print("c: ", c)
    print("gcd(", a, ", ", b, ", ", c, "): ", three_gcd(a, b, c))
    print("lcm(", a, ", ", b, ", ", c, "): ", three_lcm(a, b, c))


if __name__ == '__main__':
    main()

