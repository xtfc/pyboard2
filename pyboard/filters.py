from datetime import datetime
from pyboard.app import app

@app.template_filter('datetime')
def filter_datetime(seconds, format='%B %e, %Y @ %I:%M%P'):
	return datetime.fromtimestamp(seconds).strftime(format)
