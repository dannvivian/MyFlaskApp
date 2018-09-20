from flask import Flask, session, redirect, url_for, escape
from flask import request
import sqlite3
# import pymysql

app = Flask(__name__, static_url_path='')
app.secret_key = '123456'
count = 1
# 数据库
DATABASE_URI = "test.db"  # 一个.db文件内可以包含多个table


# 创建表格、插入数据
@app.before_first_request  # 第一个视图函数被执行前执行(可以有不止一个这种东西)
def create_db():
    # 连接
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()  # 获取光标
    # 创建表
    c.execute('''DROP TABLE IF EXISTS user''')  # 本来就存在user表则删除之
    c.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, school TEXT)''')
    # 执行SQL语句
    # 数据格式：用户名,密码
    # 提交！！！
    conn.commit()
    # 关闭
    conn.close()


def judge_if_in(username, password):
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()
    cursor = c.execute("SELECT id, name, password, school from user")
    for row in cursor:
        if row[1] == username and row[2] == password:
            conn.close()
            return True
    conn.close()
    return False


def insert_password(name, password, school):
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()
    c.execute("INSERT INTO user (name, password, school)VALUES (? ,? ,?)", (name, password, school))
    conn.commit()
    conn.close()


# 根目录
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return '欢迎%s来访问！' % escape(session['username'])
    return '''<form action="/signin" method="post">
                  <p>用户名：<input name="username"></p>
                  <p>密码：  <input name="password" type="password"></p>
                  <p><button type="submit">登陆</button></p>
                  <a href="http://127.0.0.1:5000/signup">注册</a>
                  </form>
                '''


# 注册界面
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return '''<form action="/temp" method="post">
                  <p>用户名：<input name="username"></p>
                  <p>密码：  <input name="password" type="password"></p>
                  <p>学校：  <input name="school" type="username"></p>
                  <p><button type="submit">登陆</button></p>
                  </form>
            '''


# 处理注册
@app.route('/temp', methods=['POST'])
def temp():
    name = request.form['username']
    password = request.form['password']
    school = request.form['school']
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()
    cursor = c.execute("SELECT id, name, password, school from user")
    flag = True
    for row in cursor:
        if row[1] == name:
            flag = False
            break
    if flag:
        insert_password(name, password, school)
        return '''注册成功!
        <a href="http://127.0.0.1:5000">重新登陆</a>'''
    else:
        return '该用户已经注册过了'


# 登陆界面
@app.route('/signin', methods=['POST'])
def signin():
    if judge_if_in(request.form['username'], request.form['password']):
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return '用户名不存在或者密码不对！'


@app.route('/logout')
def logout():
    # remove the username from the session if it's there # #
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/listall')
def listall():
    conn = sqlite3.connect(DATABASE_URI)
    c = conn.cursor()
    i = 1
    s = ''
    cursor = c.execute("SELECT id, name, password, school from user")
    for row in cursor:
        s = s + str(row[0]) + ':' + row[1] + ':' + row[2] + ':' + row[3] + '<br>'
    return ('<body>' + s + '</body>')


if __name__ == '__main__':
    app.run()