import datetime
import pymysql
nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(nowtime)
conn = pymysql.connect(
        host='98.142.139.32',
        user='wordpress',
        passwd='TY0812MYSQL',
        db='uploadfiles',
        port=3306,
        charset='utf8'
    )
cur = conn.cursor()
name = "xxxx111"
# cur.execute("""insert into history (tablename,times) values ("test","xxx")""")
# cur.execute()
cur.execute("""insert into history(tablename,times) values("xxx","{0}")""".format(nowtime))
conn.commit()

conn.close()