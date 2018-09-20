from flask import Flask,render_template,request
import mytools
import pymysql
import os
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('login.html')
# 首页的函数


@app.route('/index',methods=['POST'])
def myindex():
    if request.method == 'POST':
        username = request.form['name']
        userpasswd = request.form['pass']
        if mytools.islogin(username,userpasswd):
            return render_template('index.html', email="欢迎"+username)
        else:
            return render_template('wrongpasswd.html')
            # return render_template('index.html', email='wrong')
# 欢迎页的函数


@app.route('/history')
def index():
    conn = pymysql.connect(host='98.142.139.32', user='wordpress', password='TY0812MYSQL', db='uploadfiles', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM history"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('history.html',u=u)


def insert_password(name, password, school):
    db = pymysql.connect("localhost", "root", "Mysql123", "TESTDB")
    c = db.cursor()
    cursor = c.execute("SELECT id, name, password, school from user")
    c.execute("INSERT INTO user (name, password, school)VALUES (? ,? ,?)", (name, password, school))
    c.commit()
    c.close()


@app.route('/upload')
def upload_file():
    return render_template('upload.html')
# 上传文件以及首页地址


@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        f = request.files['file']     #此处获取文件
        url = request.form['weburl']     #此处获取输入的网址
        # excelname = request.form['excelname']
        # print(f.filename)
        f.save(secure_filename(f.filename))
        mytools.uploadExcel(f.filename,'abc')
        os.remove(f.filename)      #存到本地之后再删除掉
        return f.filename
if __name__ == '__main__':
    app.run()
    # 返回上传结果
