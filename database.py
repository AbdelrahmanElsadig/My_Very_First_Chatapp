from pickle import FALSE
from app import app
import mysql.connector
import yaml
db1 = yaml.load(open('db.yaml'))
db = mysql.connector.connect(host = 'bjsqk1ojkibcchfv9y3h-mysql.services.clever-cloud.com',
                             user = 'u2bdsf11zbwizsfx', 
                             passwd = 'tzxS4zjfxp8B86kSUGYM',
                             database = 'bjsqk1ojkibcchfv9y3h',
                             raw = False
                             )
cur = db.cursor(dictionary = True)


