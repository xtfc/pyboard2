import sqlite3

class Database(object):
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
		rows = cur.fetchall()
		cur.close()
		return rows

	def queryone(self, query, **kwargs):
		rows = self.query(query, **kwargs)
		return (rows[0] if rows else None)

	def execute(self, query, **kwargs):
		cur = self.connect().execute(query, kwargs)
		rows = cur.fetchall()
		index = cur.lastrowid
		cur.close()
		return index

	def executescript(self, query):
		self.connect().executescript(query)

	def querymany(self, query, args):
		cur = self.connect().executemany(query, args)

	def commit(self):
		self.connect().commit()
