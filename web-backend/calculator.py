#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from functools import reduce


def exp_format(exp):

    exp = exp.replace("--", "+")
    exp = exp.replace("-+", "-")
    exp = exp.replace("++", "+")
    exp = exp.replace("+-", "-")
    return exp


def cal_mul_div(atom_exp):

    if "*" in atom_exp:
        num_1, num_2 = atom_exp.split("*")
        res = float(num_1) * float(num_2)
        return res
    else:
        num_1, num_2 = atom_exp.split("/")
        res = float(num_1) / float(num_2)
        return res


def cal_add_sub(exp):

    res = re.findall("[+-]?\d+(?:\.\d+)?", exp)
    res = reduce(lambda num_1, num_2: float(num_1) + float(num_2), res)
    return res


def match_mul_div(exp):

    com = re.compile("\d+(\.\d+)?[*/]-?\d+(\.\d+)?")
    while True:
        obj = com.search(exp)
        if obj:
            atom_obj = obj.group()
            res = cal_mul_div(atom_obj)
            exp = exp.replace(atom_obj, str(res))
        else:
            break
    return exp


if __name__ == "__main__":

    exp = input(">>>").strip()
    exp.replace(' ', '')
    sub_exp = match_mul_div(exp)
    sub_exp = exp_format(sub_exp)
    res = cal_add_sub(sub_exp)
    print(res)
