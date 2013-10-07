import flask, os
from datetime import datetime
from flask import g, request, session
from functools import wraps
from werkzeug import secure_filename
from pyboard.app import app
from pyboard.db import Database

def open_sql(filename):
	with open(os.path.join('sql', filename + '.sql')) as f:
		return f.read()

def group(items, key):
	groups = dict()
	for item in items:
		if item[key] not in groups:
			groups[item[key]] = []
		groups[item[key]].append(item)
	return groups

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
	if course is None:
		courses = g.db.query(open_sql('courses_uid'), uid=g.user['uid'])
		grades = g.db.query(open_sql('grades_uid'), uid=g.user['uid'])
		assignments = g.db.query(open_sql('assignments_uid'), uid=g.user['uid'])
		title = 'Dashboard'
		navkey = 'dashboard'
	else:
		courses = g.db.query(open_sql('courses_uid-cid'), uid=g.user['uid'], cid=g.course['cid'])
		grades = g.db.query(open_sql('grades_uid-cid'), uid=g.user['uid'], cid=g.course['cid'])
		assignments = g.db.query(open_sql('assignments_uid-cid'), uid=g.user['uid'], cid=g.course['cid'])
		title = g.course['displayname'] + ' Dashboard'
		navkey = g.course['name'] + '-dashboard'

	return flask.render_template('dashboard.html',
		title=title,
		navkey=navkey,
		courses=courses,
		grades=group(grades, 'C.name'),
		assignments=group(assignments, 'C.name'))

@app.route('/assignments/<aid>')
@requires_auth
def assignment(aid):
	assignment = g.db.queryone('SELECT * FROM assignments WHERE aid=:aid', aid=aid)

	# ensure the user is enrolled in this assignment's course
	entry = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid', uid=g.user['uid'], cid=assignment[1])
	if entry is None:
		flask.flash('Not in course')
		return flask.redirect(flask.url_for('dashboard'))

	courses = g.db.query(open_sql('courses_uid'), uid=g.user['uid'])
	grades = g.db.query(open_sql('grades_aid'), aid=aid)

	return flask.render_template('assignment.html',
		title=assignment['name'],
		navkey='assignment' + str(aid),
		assignment=assignment,
		grades=grades,
		courses=courses)

@app.route('/assignments/<aid>/submit', methods=['POST'])
@requires_auth
def submit(aid):
	ufile = request.files['submission']
	if not ufile:
		flask.flash('No file selected')
		return flask.redirect(flask.url_for('assignment', aid=aid))

	filename = secure_filename(ufile.filename)

	gid = g.db.query_saveid('INSERT INTO grades(uid, aid, score, message) values(:uid, :aid, 0, "")',
		uid=g.user['uid'],
		aid=aid)

	upload_path = os.path.join('uploads', str(gid))
	upload_file = os.path.join(upload_path, filename)

	try:
		os.makedirs(upload_path)
		ufile.save(upload_file)
	except:
		flask.flash('There was an error processing your submission. Please try again.')
		return flask.redirect(flask.url_for('assignment', aid=aid))

	g.db.commit()
	flask.flash('Submission received')

	return flask.redirect(flask.url_for('assignment', aid=aid))

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
