import flask
import os
import time
from flask import g, request, session
from functools import wraps
from pyboard.app import app
from pyboard.db import Database
from pyboard.util import open_sql, group
from werkzeug.utils import secure_filename

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
			return flask.redirect(flask.url_for('view_login'))
		return func(*args, **kwargs)
	return wrapper

def requires_level(level):
	def outer_wrapper(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			perm = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid AND level >= :level',
				level=level,
				uid=g.user['uid'],
				cid=request.view_args['cid'])
			if perm is None:
				flask.flash('You do not have permission to view this page')
				return flask.redirect(flask.url_for('view_dashboard'))
			return func(*args, **kwargs)
		return wrapper
	return outer_wrapper

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
	if getattr(g, 'db', None) is not None:
		g.db.close()

@app.route('/')
@requires_auth
def view_dashboard():
	assignments = g.db.query(open_sql('assignments-future_uid'), uid=g.user['uid'])
	messages = g.db.query(open_sql('messages_uid-limit'), uid=g.user['uid'], limit=4)

	return flask.render_template('dashboard.html',
		title='Dashboard',
		navkey='dashboard',
		assignments=group(assignments, 'cid'),
		messages=group(messages, 'cid'))

@app.route('/course/<cid>')
@requires_auth
def view_course(cid):
	# ensure the user is enrolled in this course
	entry = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid',
		uid=g.user['uid'],
		cid=cid)

	if entry is None:
		flask.flash('You are not enrolled in that course.')
		return flask.redirect(flask.url_for('view_dashboard'))

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

@app.route('/course/<cid>/assignment', methods=['GET', 'POST'])
@requires_auth
@requires_level(2)
def view_new_assignment(cid):
	course = g.db.queryone('SELECT * FROM courses WHERE cid=:cid', cid=cid)
	entry = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid',
		uid=g.user['uid'], cid=cid)

	if request.method == 'GET':
		return flask.render_template('assignment_new.html',
			navkey='cid-' + str(cid),
			course=course,
			entry=entry)

	else:
		assignment = g.db.execute('INSERT INTO assignments(cid, points, name, body, due) VALUES(:cid, :points, :name, :body, :due)',
				cid=cid,
				points=request.form['points'],
				name=request.form['name'],
				body=request.form['body'],
				due=request.form['due'])
		g.db.commit()
		return flask.redirect(flask.url_for('view_assignment', aid=assignment))

@app.route('/assignment/<aid>')
@requires_auth
def view_assignment(aid):
	assignment = g.db.queryone('SELECT * FROM assignments WHERE aid=:aid', aid=aid)
	course = g.db.queryone('SELECT * FROM courses WHERE cid=:cid', cid=assignment['cid'])

	# ensure the user is enrolled in this assignment's course
	entry = g.db.queryone('SELECT * FROM entries WHERE uid=:uid AND cid=:cid',
		uid=g.user['uid'],
		cid=assignment['cid'])

	if entry is None:
		flask.flash('You are not enrolled in that course.')
		return flask.redirect(flask.url_for('view_dashboard'))

	grades = g.db.query(open_sql('grades_aid'), aid=aid)

	return flask.render_template('assignment.html',
		title=assignment['name'],
		navkey='aid-' + str(aid),
		assignment=assignment,
		submittable=assignment['due'] > time.time(),
		entry=entry,
		grades=grades,
		course=course)

@app.route('/assignment/<aid>/submit', methods=['POST'])
@requires_auth
def view_submit(aid):
	assignment = g.db.queryone('SELECT * FROM assignments WHERE aid=:aid', aid=aid)
	if assignment['due'] <= time.time():
		flask.flash('Unable to submit past the due date')
		return flask.redirect(flask.url_for('view_assignment', aid=aid))

	ufile = request.files['submission']
	if not ufile:
		flask.flash('No file selected')
		return flask.redirect(flask.url_for('view_assignment', aid=aid))

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
		return flask.redirect(flask.url_for('view_assignment', aid=aid))

	g.db.commit()
	flask.flash('Submission received')

	return flask.redirect(flask.url_for('view_assignment', aid=aid))

@app.route('/login', methods=['GET', 'POST'])
def view_login():
	if request.method == 'GET':
		return flask.render_template('login.html')

	if check_auth(request.form['username'], request.form['password']):
		session['username'] = request.form['username']
		flask.flash('Logged in as {}'.format(session['username']))
		return flask.redirect(flask.url_for('view_dashboard'))

	flask.flash('Invalid login')
	return flask.redirect(flask.url_for('view_login'))

@app.route('/logout')
def view_logout():
	session.pop('username', None)
	flask.flash('Logged out')
	return flask.redirect(flask.url_for('view_login'))
