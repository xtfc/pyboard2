import bumpy as b
from pyboard.app import app
from pyboard.db import Database
from pyboard.views import open_sql

@b.task
def init():
	db = Database(app.config['DATABASE'])
	db.executescript(open_sql('schema'))
	db.close()

@b.task
def test():
	db = Database(app.config['DATABASE'])
	db.executescript(open_sql('test'))
	db.close()
