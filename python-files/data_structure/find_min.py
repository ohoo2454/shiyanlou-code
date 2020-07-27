#!/usr/bin/env python3
#-*- coding: utf-8 -*-


def find_min(nums):
    min = nums[0]
    for x in nums:
        if x < min:
            min = x
    print(min)


def main():
    find_min([2, 4, 9, 7, 19, 94, 5])


if __name__ == '__main__':
    main()

