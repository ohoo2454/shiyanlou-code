#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def function(num):
    mylist = [num]
    while num != 1:
        if num % 2 == 1:
            num = 3*num + 1
            mylist.append(num)
        else:
            num = num // 2
            mylist.append(num)
    return mylist, len(mylist) - 1


print(function(43))

