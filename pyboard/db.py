import flask, sqlite3

class Database:
	def __init__(self, path):
		self.path = path
		self._connection = None

	def connect(self):
		if not self._connection:
			self._connection = sqlite3.connect(self.path)
			self._connection.row_factory = sqlite3.Row

		return self._connection

	def close(self):
		if self._connection:
			self._connection.close()

	def query(self, query, **kwargs):
		cur = self.connect().execute(query, kwargs)
		rv = cur.fetchall()
		cur.close()
		return rv

	def queryone(self, query, **kwargs):
		rv = self.query(query, **kwargs)
		return (rv[0] if rv else None)


	def querymany(self, query, args):
		cur = self.connect().executemany(query, args)

	def commit(self):
		self.connect().commit()
