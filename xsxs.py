#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zty
import datetime
import time
import mytools
# x=datetime.datetime.now()
# y = time.time()
# print(x)
# t=str(int(y))
# # t=t+'xxxxxx'
# pp='123'
# print(type(t))
# p = mytools.uploadExcel(u"01.xlsx",pp)
now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
nows = now+'x'
print(nows)