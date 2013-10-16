import flask, os, time
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

	if 'username' in session:
		g.user = g.db.queryone('SELECT * FROM users WHERE username=:username', username=session['username'])
		if g.user is not None:
			g.courses = g.db.query(open_sql('courses_uid'), uid=g.user['uid'])

@app.teardown_request
def teardown(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
@requires_auth
def dashboard():
	assignments = g.db.query(open_sql('assignments-future_uid'), uid=g.user['uid'])
	messages = g.db.query(open_sql('messages_uid-limit'), uid=g.user['uid'], limit=4)

	return flask.render_template('dashboard.html',
		title='Dashboard',
		navkey='dashboard',
		assignments=group(assignments, 'cid'),
		messages=group(messages, 'cid'))

@app.route('/course/<cid>')
@requires_auth
def course(cid):
	# ensure the user is enrolled in this course
	entry = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid',
		uid=g.user['uid'],
		cid=cid)

	if entry is None:
		flask.flash('You are not enrolled in that course.')
		return flask.redirect(flask.url_for('dashboard'))

	course = g.db.queryone('SELECT * FROM courses WHERE cid=:cid', cid=cid)
	entry = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid',
		uid=g.user['uid'], cid=cid)
	grades = g.db.query(open_sql('grades_uid-cid'), uid=g.user['uid'], cid=cid)
	assignments = g.db.query(open_sql('assignments_cid'), cid=cid)
	messages = g.db.query(open_sql('messages_cid'), cid=cid)

	return flask.render_template('course.html',
		title=course['name'],
		navkey='cid-' + str(cid),
		course=course,
		entry=entry,
		grades=grades,
		assignments=assignments,
		messages=messages)

@app.route('/assignment/<aid>')
@requires_auth
def assignment(aid):
	assignment = g.db.queryone('SELECT * FROM assignments WHERE aid=:aid', aid=aid)
	course = g.db.queryone('SELECT * FROM courses WHERE cid=:cid', cid=assignment['cid'])

	# ensure the user is enrolled in this assignment's course
	entry = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid',
		uid=g.user['uid'],
		cid=assignment['cid'])

	if entry is None:
		flask.flash('You are not enrolled in that course.')
		return flask.redirect(flask.url_for('dashboard'))

	grades = g.db.query(open_sql('grades_aid'), aid=aid)

	return flask.render_template('assignment.html',
		title=assignment['name'],
		navkey='aid-' + str(aid),
		assignment=assignment,
		submittable=assignment['due'] > time.time(),
		grades=grades)

@app.route('/assignment/<aid>/submit', methods=['POST'])
@requires_auth
def submit(aid):
	assignment = g.db.queryone('SELECT * FROM assignments WHERE aid=:aid', aid=aid)
	if assignment['due'] <= time.time():
		flask.flash('Unable to submit past the due date')
		return flask.redirect(flask.url_for('assignment', aid=aid))

	ufile = request.files['submission']
	if not ufile:
		flask.flash('No file selected')
		return flask.redirect(flask.url_for('assignment', aid=aid))

	filename = secure_filename(ufile.filename)

	gid = g.db.execute('INSERT INTO grades(uid, aid, score, timestamp) values(:uid, :aid, 0, strftime("%s", "now"))',
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
