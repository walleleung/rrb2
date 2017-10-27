from flask import Blueprint
import pymysql
main = Blueprint('main', __name__)

conn =pymysql.connect(host='127.0.0.1',user='root',password='mysql',db='bj',charset="utf8")
cur=conn.cursor()
print('xxxxxxxxxxxxxxxxxxxxxxxxxx')

from . import login, pay_view  #views, bjgs_view, admin_view, user_view