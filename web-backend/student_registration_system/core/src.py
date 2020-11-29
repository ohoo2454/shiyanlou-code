#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from conf import settings


flag = True


class Student(object):

    def __init__(self, name, password="123456", selected_courses=[]):

        self.name = name
        self.password = password
        self.selected_courses = selected_courses

    def get_all_courses(self):

        course_name_list = []
        with open(settings.course_info_path, mode="r", encoding="utf-8") as f:
            print("name\tprice\tperiod\tteacher")
            for line in f:
                course_info_list = line.strip().split("|")
                course_name_list.append(course_info_list[0])
                for course_info_item in course_info_list:
                    print(course_info_item, end="\t")
                print()
        return tuple(course_name_list)

    def select_course(self):

        course_name_list = self.get_all_courses()
        while True:
            course_name = input("请输入你选择的课程名：").strip()
            if course_name.upper() == 'Q':
                with open(settings.student_info_path, mode="a", 
                        encoding="utf-8") as f:
                    f.write(self.name)
                    for course in self.selected_courses:
                        f.write("|" + course)
                    f.write("\n")
                return
            if course_name in course_name_list:
                self.selected_courses.append(course_name)
                print("\033[1;32;40m 选择课程 {} 成功 \033[0m".format(course_name))
            else:
                print("\033[1;31;40m 课程名称有误，请重新输入 \033[0m")
                continue

    def get_selected_courses(self):

        with open(settings.student_info_path, mode="r", encoding="utf-8") as f:
            for line in f:
                stu_info_list = line.strip().split("|")
                if stu_info_list[0] == self.name:
                    for course in stu_info_list[1:]:
                        print(course)

    def exit_system(self):

        print('Bye~')
        global flag
        flag = False
    
    def show_method_list(self):

        method_dic = {
            1: self.get_all_courses,
            2: self.select_course,
            3: self.get_selected_courses,
            4: self.exit_system,
        }

        while flag:
            print("""
                1. 查看所有课程
                2. 选择课程
                3. 查看已选课程
                4. 退出
            """)
            choice = input("请输入你的选择：").strip()
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(method_dic):
                    method_dic[choice]()
                else:
                    print("\033[1;31;40m 输入有误，请重新输入 \033[0m")
            else:
                print("\033[1;31;40m 输入非法，请重新输入 \033[0m")


class Administrator(object):

    def __init__(self, name):

        self.name = name

    def create_course(self):

        course_info_path = "srs/course_info.txt"
        course_name = input("Please enter the name " + 
                "of the course: ").strip()
        course_price = input("Please enter the price " +
                "of the course: ").strip()
        course_period = input("Please enter the period " +
                "of the course: ").strip()
        course_teacher = input("Please enter the teacher " +
                "of the course: ").strip()
        course_obj = Course(course_name, course_price, course_period, 
                course_teacher)
        with open(settings.course_info_path, mode="a", encoding="utf-8") as f:
            f.write(course_obj.name + "|" + course_obj.price + "|"
                    + course_obj.period + "|" + course_obj.teacher + "\n")
        print("\033[1;32;40m 课程创建成功 \033[0m")
        return course_obj

    def create_student(self):

        student_name = input("Please enter the name " +
                "of the student: ").strip()
        student_obj = Student(student_name)
        with open(settings.student_register_path, mode="a", encoding="utf-8") as f:
            f.write(student_obj.name + "|" + student_obj.password + "\n")
        print("\033[1;32;40m 学生创建成功 \033[0m")
        return student_obj

    def get_all_courses(self):

        with open(settings.course_info_path, mode="r", encoding="utf-8") as f:
            print("name\tprice\tperiod\tteacher")
            for line in f:
                course_info_list = line.strip().split("|")
                for course_info_item in course_info_list:
                    print(course_info_item + "\t", end="")
                print()

    def get_all_students(self):

        with open(settings.student_register_path, mode="r", encoding="utf-8") as f:
            print("name")
            for line in f:
                print(line.strip().split("|")[0])

    def get_all_students_info(self):

        with open(settings.student_info_path, mode="r", encoding="utf-8") as f:
            for line in f:
                line_info_list = line.strip().split("|")
                for line_info_item in line_info_list:
                    print(line_info_item, end=" ")

    def exit_system(self):

        print('Bye~')
        global flag
        flag = False

    def show_method_list(self):

        method_dic = {
            1: self.create_course,
            2: self.create_student,
            3: self.get_all_courses,
            4: self.get_all_students,
            5: self.get_all_students_info,
            6: self.exit_system,
        }

        while flag:
            print("""
                1. 创建课程
                2. 创建学生
                3. 查看所有课程
                4. 查看所有学生
                5. 查看所有学生选课信息
                6. 退出
            """)
            choice = input("请输入你的选择：").strip()
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(method_dic):
                    method_dic[choice]()
                else:
                    print("\033[1;31;40m 输入有误，请重新输入 \033[0m")
            else:
                print("\033[1;31;40m 输入非法，请重新输入 \033[0m")
        return


class Course(object):

    def __init__(self, name, price, period, teacher):

        self.name = name
        self.price = price
        self.period = period
        self.teacher = teacher


def login(path, user_id):

    with open(path, mode="r", encoding="utf-8") as f:
        dic = {i.strip().split("|")[0]: i.strip().split("|")[1] for i in f}
    count = 0
    while count < 3:
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        if username in dic and dic[username] == password:
            print("登陆成功")
            if user_id == 0:
                admin_obj = Administrator(username)
                admin_obj.show_method_list()
                return
            else:
                stu_obj = Student(username)
                stu_obj.show_method_list()
                return
        else:
            print("用户名或密码错误，请重新输入")
            count += 1
    global flag
    flag = False
    return


def run():

    user_dic = {
        1: (login, settings.admin_register_path, 0),
        2: (login, settings.student_register_path, 1),
    }

    while flag:
        print("""
            欢迎使用学生选课系统：
            1. Administrator
            2. Student
        """)
        choice = input("请选择你的身份：").strip()
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(user_dic):
                user_dic[choice][0](user_dic[choice][1], user_dic[choice][2])
            else:
                print("\033[1;31;40m 身份不存在，请重新输入 \033[0m")
                continue
        else:
            print("\033[1;31;40m 输入非法字符，请重新输入 \033[0m")
            continue
