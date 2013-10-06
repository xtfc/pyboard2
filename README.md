# Pyboard

Fast, minimal course management software powered by [Python](http://www.python.org/), [Flask](https://github.com/mitsuhiko/flask), and [SQlite](http://www.sqlite.org/).

## Usage

You don't yet.

## Development Usage

```bash
$ pip install -U -r requirements.txt
$ sqlite3 test.db < sql/schema.sql
$ sqlite3 test.db < sql/test.sql
$ bump debug
```

Point browser to `http://localhost:5000/` and log in with any valid username and a password of `password`.
