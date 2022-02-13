from pickle import FALSE
from app import app
import mysql.connector
import yaml
db1 = yaml.load(open('db.yaml'))
db = mysql.connector.connect(host = db1['mysql_host'],
                             user = db1['mysql_user'], 
                             passwd = db1['mysql_password'],
                             database = db1['mysql_db'],
                             raw = False
                             )
cur = db.cursor(dictionary = True)


