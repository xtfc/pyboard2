import bumpy as b, sys
from pyboard.app import app

@b.task
def setup():
	'''Run standard setup tasks'''
	pass

@b.task
def run():
	'''Run the production server'''
	app.run(host='0.0.0.0')

@b.task
def debug():
	'''Run the debug server'''
	app.run(host='0.0.0.0', debug=True)
