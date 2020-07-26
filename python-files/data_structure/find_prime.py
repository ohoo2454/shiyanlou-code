#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def find_prime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                print(num, "is not prime number")
                print(i, "*", num//i, "=", num)
                break
        else:
            print(num, "is prime number")
    else:
        print(num, "is not prime number")

num = int(input("please enter one number: "))
find_prime(num)

