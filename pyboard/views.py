import flask, os
from flask import g, request, session
from functools import wraps
from pyboard.app import app
from pyboard.db import Database

def open_sql(filename):
	with open(os.path.join('sql', filename + '.sql')) as f:
		return f.read()

def check_auth(username, password):
	if app.debug:
		user = g.db.queryone('SELECT uid FROM users WHERE username=:username', username=username)
		return (user is not None) and (password == 'password')

	return False

def requires_auth(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'username' not in session:
			flask.flash('You must be logged in to view this page')
			return flask.redirect(flask.url_for('login'))
		return func(*args, **kwargs)
	return wrapper

@app.before_request
def setup():
	g.db = Database(app.config['DATABASE'])
	g.user = None
	g.course = None

	if 'username' in session:
		g.user = g.db.queryone('SELECT * FROM users WHERE username=:username', username=session['username'])

	if request.view_args:
		if 'course' in request.view_args:
			g.course = g.db.queryone('SELECT * FROM courses WHERE name=:course', course=request.view_args['course'])

@app.teardown_request
def teardown(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
@app.route('/course/<course>')
@requires_auth
def dashboard(course = None):
	courses = g.db.query(open_sql('courses_uid'), uid=g.user['uid'])

	if course is None:
		grades = g.db.query(open_sql('grades_uid'), uid=g.user['uid'])
		assignments = g.db.query(open_sql('assignments_uid'), uid=g.user['uid'])
		title = 'Dashboard'
		navkey = 'dashboard'
	else:
		grades = g.db.query(open_sql('grades_uid-cid'), uid=g.user['uid'], cid=g.course['cid'])
		assignments = g.db.query(open_sql('assignments_uid-cid'), uid=g.user['uid'], cid=g.course['cid'])
		title = g.course['displayname'] + ' Dashboard'
		navkey = g.course['name'] + '-dashboard'

	return flask.render_template('dashboard.html',
		title=title,
		navkey=navkey,
		courses=courses,
		grades=grades,
		assignments=assignments)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return flask.render_template('login.html')

	if check_auth(request.form['username'], request.form['password']):
		session['username'] = request.form['username']
		flask.flash('Logged in as {}'.format(session['username']))
		return flask.redirect(flask.url_for('dashboard'))

	flask.flash('Invalid login')
	return flask.redirect(flask.url_for('login'))

@app.route('/logout')
def logout():
	session.pop('username', None)
	flask.flash('Logged out')
	return flask.redirect(flask.url_for('login'))
