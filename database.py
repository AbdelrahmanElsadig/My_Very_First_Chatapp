from pickle import FALSE
from wsgi import app
import mysql.connector
db = mysql.connector.connect(host = 'bjsqk1ojkibcchfv9y3h-mysql.services.clever-cloud.com',
                             user = 'u2bdsf11zbwizsfx', 
                             passwd = 'tzxS4zjfxp8B86kSUGYM',
                             database = 'bjsqk1ojkibcchfv9y3h',
                             raw = False
                             )
cur = db.cursor(dictionary = True)


