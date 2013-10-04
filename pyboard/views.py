import flask
from flask import g, request, session
from functools import wraps
from pyboard.app import app
from pyboard.db import Database

def check_auth(username, password):
	if app.debug:
		return password == 'password'

	return False

def requires_auth(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'username' not in session:
			flask.flash('You must be logged in to view this page')
			return flask.redirect(flask.url_for('login'))
		return func(*args, **kwargs)
	return wrapper

@app.route('/')
@requires_auth
def index():
	return flask.render_template('index.html',
		title='Hello, world!',
		content='Welcome to [Pyboard 2.0](https://github.com/xtfc/pyboard2)!')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return flask.render_template('login.html')

	if check_auth(request.form['username'], request.form['password']):
		session['username'] = request.form['username']
		flask.flash('Logged in as {}'.format(session['username']))
		return flask.redirect(flask.url_for('index'))

	flask.flash('Invalid login')
	return flask.redirect(flask.url_for('login'))

@app.route('/logout')
def logout():
	session.pop('username', None)
	flask.flash('Logged out')
	return flask.redirect(flask.url_for('login'))
