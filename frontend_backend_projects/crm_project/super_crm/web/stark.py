#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stark.service.v1 import site
from web.models import (School, Department, UserInfo, Course, ClassList, 
        Customer, ConsultRecord)
from web.views.school import SchoolHandler
from web.views.depart import DepartmentHandler
from web.views.userinfo import UserInfoHandler
from web.views.course import CourseHandler
from web.views.class_list import ClassListHandler
from web.views.private_customer import PrivateCustomerHandler
from web.views.public_customer import PublicCustomerHandler
from web.views.consult_record import ConsultRecordHandler

# 模型和对应试图函数处理类注册
site.register(School, SchoolHandler)
site.register(Department, DepartmentHandler)
site.register(UserInfo, UserInfoHandler)
site.register(Course, CourseHandler)
site.register(ClassList, ClassListHandler)
site.register(Customer, PrivateCustomerHandler, 'priv')
site.register(Customer, PublicCustomerHandler, 'pub')
site.register(ConsultRecord, ConsultRecordHandler)
