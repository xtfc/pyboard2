from datetime import datetime
from pyboard.app import app

@app.template_filter('datetime')
def filter_datetime(seconds, fmt='%b %e, %Y @ %I:%M%P'):
	return datetime.fromtimestamp(seconds).strftime(fmt)
