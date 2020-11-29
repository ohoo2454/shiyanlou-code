#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from conf.settings import register_path
from lib.common import auth


status_dic = {
    "username": None,
    "status": False,
}

flag = True


def login():

    count = 0
    with open(register_path, mode="r", encoding="utf-8") as f:
        dic = {i.strip().split("|")[0]: i.strip().split("|")[1] for i in f}
    while count < 3:
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        if username in dic and dic[username] == password:
            print("登录成功")
            status_dic["username"] = username
            status_dic["status"] = True
            return True
        else:
            print("用户名或密码错误，请重新登录")
            count += 1


def register():

    with open(register_path, mode="r", encoding="utf-8") as f:
        dic = {i.strip().split("|")[0]: i.strip().split("|")[1] for i in f}
    while True:
        print("\033[1;45m 欢迎来到注册页面 \033[0m")
        username = input("请输入用户名：").strip()
        if not username.isalnum():
            print("\033[1;31;40m 用户名有非法字符，请重新输入 \033[0m")
            continue
        if username in dic:
            print("\033[1;31;40m 用户名已存在，请重新输入 \033[0m")
            continue
        password = input("请输入密码：").strip()
        if 6 <= len(password) <= 14:
            with open(register_path, mode="a", encoding="utf-8") as f:
                f.write("{}|{}\n".format(username, password))
            status_dic["username"] = username
            status_dic["status"] = True
            print("\033[1;32;40m 恭喜您，注册成功！已帮您成功登录~ \033[0m")
            return True
        else:
            print("\033[1;31;40m 密码长度超出范围，请重新输入 \033[0m")


@auth
def article():

    print("\033[1;32;40m 欢迎{}访问文章页面\033[0m".format(status_dic['username']))


@auth
def diary():

    print("\033[1;32;40m 欢迎{}访问日记页面\033[0m".format(status_dic['username']))


@auth
def comment():

    print("\033[1;32;40m 欢迎{}访问评论页面\033[0m".format(status_dic['username']))


@auth
def enshrine():

    print("\033[1;32;40m 欢迎{}访问收藏页面\033[0m".format(status_dic['username']))


def logout():

    status_dic["username"] = None
    status_dic["status"] = False
    print("\033[1;32;40m 注销成功 \033[0m")


def exit_program():

    global flag
    flag = False
    return flag


def run():

    choice_dict = {
    1: login,
    2: register,
    3: article,
    4: diary,
    5: comment,
    6: enshrine,
    7: logout,
    8: exit_program,
}

    while flag:
        print("""
        欢迎来到博客园首页
        1: 请登录
        2: 请注册
        3: 文章页面
        4: 日记页面
        5: 评论页面
        6: 收藏页面
        7: 注销
        8: 退出程序""")

        choice = input("Please enter your choice: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(choice_dict):
                choice_dict[choice]()
            else:
                print("\033[1;31;40m 您输入的超出范围，请重新输入 \033[0m")
        else:
            print("\033[1;31;40m 您输入的选项有非法字符，请重新输入 \033[0m")
