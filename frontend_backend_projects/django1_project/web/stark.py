#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stark.service.v1 import site
from web.models import (School, Department, UserInfo, Course, ClassList, 
                        Customer, ConsultRecord, PaymentRecord, Student, 
                        ScoreRecord, CourseRecord)
from web.views.school import SchoolHandler
from web.views.depart import DepartmentHandler
from web.views.userinfo import UserInfoHandler
from web.views.course import CourseHandler
from web.views.class_list import ClassListHandler
from web.views.private_customer import PrivateCustomerHandler
from web.views.public_customer import PublicCustomerHandler
from web.views.consult_record import ConsultRecordHandler
from web.views.payment_record import PaymentRecordHandler
from web.views.check_payment_record import CheckPaymentRecordHandler
from web.views.student import StudentHandler
from web.views.score_record import ScoreRecordHandler
from web.views.course_record import CourseRecordHandler

# 模型和对应试图函数处理类注册
site.register(School, SchoolHandler)
site.register(Department, DepartmentHandler)
site.register(UserInfo, UserInfoHandler)
site.register(Course, CourseHandler)
site.register(ClassList, ClassListHandler)
site.register(Customer, PrivateCustomerHandler, 'priv')
site.register(Customer, PublicCustomerHandler, 'pub')
site.register(ConsultRecord, ConsultRecordHandler)
site.register(PaymentRecord, PaymentRecordHandler)
site.register(PaymentRecord, CheckPaymentRecordHandler, 'check')
site.register(Student, StudentHandler)
site.register(ScoreRecord, ScoreRecordHandler)
site.register(CourseRecord, CourseRecordHandler)
