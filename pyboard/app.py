import flask
from flaskext.markdown import Markdown
from werkzeug.contrib.fixers import ProxyFix

# Create a Flask object
app = flask.Flask(__name__)

# Configure it to work with nginx
app.wsgi_app = ProxyFix(app.wsgi_app)

# Add the |markdown template filter
Markdown(app)
