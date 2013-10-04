import flask
from pyboard.app import app

@app.route('/')
def index():
	return flask.render_template('index.html',
		title='Hello, world!',
		content='Welcome to [Pyboard 2.0](https://github.com/xtfc/pyboard2)!')
