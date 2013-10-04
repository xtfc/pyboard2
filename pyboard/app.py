import flask
from werkzeug.contrib.fixers import ProxyFix
from flaskext.markdown import Markdown

# Create a Flask object
app = flask.Flask(__name__)

# Configure it to work with nginx
app.wsgi_app = ProxyFix(app.wsgi_app)

# Add the |markdown template filter
Markdown(app)
