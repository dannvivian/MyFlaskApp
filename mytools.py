#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zty
# !/usr/bin/python3
import pymysql
import xlrd,xlwt
import datetime


def islogin(xname,xpasswd):
        # 打开数据库连接
        db = pymysql.connect("98.142.139.32", "wordpress", "TY0812MYSQL", "testdb")

        # 使用cursor()方法获取操作游标
        cur = db.cursor()

        # 1.查询操作
        # 编写sql 查询语句  user 对应我的表名
        sql = "select * from user"
        try:
            cur.execute(sql)  # 执行sql语句

            results = cur.fetchall()  # 获取查询的所有记录
            # print("name", "passwd")
            # 遍历结果
            for row in results:
                name = row[0]
                password = row[1]
                # print(name, password)
                if xname==name and xpasswd ==password :
                    return True
            return False
        except Exception as e:
            raise e
        finally:
            db.close()  # 关闭连接


def uploadExcel(filename,excelname):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name("Sheet1")
    conn = pymysql.connect(
        host='98.142.139.32',
        user='wordpress',
        passwd='TY0812MYSQL',
        db='uploadfiles',
        port=3306,
        charset='utf8'
    )
    # 获得游标
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS {0} (`id` VARCHAR(50) NOT NULL,`steps` VARCHAR(500) NOT NULL)""".format(excelname))
    # 创建插入SQL语句
    query = 'insert into {0} (id,steps) values (%s, %s)'.format(excelname)
    # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
    for r in range(1, sheet.nrows):
        id = sheet.cell(r, 0).value
        steps = sheet.cell(r, 1).value
        values = (id,steps)
        # 执行sql语句
        cur.execute(query, values)
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    times = now+'x'
    cur.execute(
        """insert into history (tablename,times) values ('{0}','{1}')""".format(excelname,now))
    cur.close()
    conn.commit()
    conn.close()
    columns = str(sheet.ncols)
    rows = str(sheet.nrows)
    # print("导入 " + columns + " 列 " + rows + " 行数据到MySQL数据库!")
    return '文件上传成功'


if __name__ == '__main__':
    # x=islogin('demo','demo')
    # print(x)
    name1='myname.xlsx'

    x= uploadExcel("01.xlsx",'examplesss')

# @app.route('/temp',methods=['POST'])
# def myreg():
#     if request.method=='POST':
#         username = request.form['name']
#         passwd = request.form['passwd']
#         db = pymysql.connect("localhost", "root", "Mysql123", "TESTDB")
#
#         # 使用cursor()方法获取操作游标
#         cur = db.cursor()
#         cursor = cur.execute("SELECT id, name, password, school from user")
#         flag = True
#         for row in cursor:
#             if row[1] == username:
#                 flag = False
#                 break
#         if flag:
#             insert_password(name, password, school)
#             return '''注册成功!
#                 <a href="http://127.0.0.1:5000">重新登陆</a>'''
#         else:
#             return '该用户已经注册过了'





