#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib


def md5(arg):
    md5_pwd = hashlib.md5(bytes('abd', encoding='utf-8'))
    md5_pwd.update(bytes(arg, encoding='utf-8'))
    return md5_pwd.hexdigest()


def log(user, pwd):
    with open('db', 'r', encoding='utf-8') as f:
        for line in f:
            u, p = line.strip().split('|')
            if u == user and p == md5(pwd):
                return True


def register(user, pwd):
    with open('db', 'a', encoding='utf-8') as f:
        temp = user + '|' + md5(pwd)
        f.write(temp)


i = input('1-login, 2-register')
if i == '2':
    user = input('username: ')
    pwd = input('password: ')
    register(user, pwd)
elif i == '1':
    user = input('username: ')
    pwd = input('password: ')
    r = log(user, pwd)
    if r == True:
        print('login successfully!')
    else:
        print('login failed!')
else:
    print('the user is not exist!')

