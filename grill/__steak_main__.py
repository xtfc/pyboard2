import steak as s
from pyboard.app import app

def setup():
	'''Run standard setup tasks'''
	pass

def run():
	'''Run the production server'''
	app.run(host='0.0.0.0')

def debug():
	'''Run the debug server'''
	app.run(host='0.0.0.0', debug=True)
