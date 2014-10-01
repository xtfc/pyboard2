import steak as s
from pyboard.app import app
from pyboard.db import Database
from pyboard.views import open_sql

def init():
	db = Database(app.config['DATABASE'])
	db.executescript(open_sql('schema'))
	db.close()

def test():
	db = Database(app.config['DATABASE'])
	db.executescript(open_sql('test'))
	db.close()
