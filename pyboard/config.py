from pyboard.app import app

# Add necessary configuration variables here
app.config['SECRET_KEY'] = 'thiskeyneedstobesecret'
app.config['DATABASE'] = 'test.db'
app.config['EMAIL_FROM'] = 'pyboard@localhost'
