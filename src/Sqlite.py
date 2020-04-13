import os
import sqlite3
from Sql import Sql
from Model import Model

class Sqlite():
	'''
	The service provider for an SQLite3 file based database
	'''

	cx = None
	dbms = None
	model = None
	db_type = None
	dialect = None
	placeholder = '?'
	tbl_list_qry = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"

	def __init__(self, model=None):
		try:
			self.model = model 
			self.dbms = self.get_dsn()
			self.db_type = 'sqlite3'
			self.dialect = Sql(model = self.model)
			if not self.dbms:
				self.dbms = ':memory:'
			self.cx = sqlite3.connect(self.dbms, check_same_thread=False)
			self.cx.row_factory = self.dictFactory

		except Exception as e:
			print( "DB Error %s" % e )

	def get_secrets(self):
		rv = {}
		secrets = self.model.secrets()
		for k in secrets.keys():
			rv[k] = os.getenv(secrets[k])
		return rv
	
	def get_dsn(self):
		secrets = self.get_secrets()
		return os.path.join(secrets['path'],secrets['dbms'])

	def database(self):
		secrets = self.get_secrets()
		return secrets['dbms']

	def get_cursor(self):
		return self.cx.cursor()

	def dictFactory(self,cur,row):
		rv = {}
		ix = 0
		for t in cur.description:
			tag = t[0]
			rv[tag] = row[ix]
			ix += 1
		return rv

	def dictTotuple(self, d):
		if not type(d) == type(dict()):
			return None
		return tuple(d.values())

	def dlistTotlist(self,dl):
		if not type(dl) == type(list()):
			return None
		rv = []
		for d in dl:
			t = self.dictTotuple(d)
			if t:
				rv.append(t)
		return rv

	def type(self):
		return self.db_type

	def table_list(self):
		return self.exec(self.table_list_query())

	def table_list_query(self):
		return self.tbl_list_qry

	def variable_list_query(self, table):
		pass

	def safe_exec(self,qry,data):
		try:
			dta = self.dictTotuple(data)
			rv = self.get_cursor()
			rv.execute(qry,dta)
			return rv
		except Exception as e:
			print( "ERROR: %s\n  QUERY:" % e, qry )
		return None

	def exec(self,qry):
		try:
			rv = self.get_cursor()
			rv.execute(qry)
			return rv
		except Exception as e:
			print( "ERROR: %s\n  QUERY:" % e, qry )
			return None

	def upsert(self,table,data):
		rv = self.dialect.insert(table,data)
		return rv[0:-1] + 'on conflict do update set %s ;' % self.dialect.assign_list(table,data)


if __name__ == '__main__':
	import sys

	model = Model(sys.argv[1])
	db = Sqlite( model=model )
	print( db.get_dsn() )
	tlq = db.table_list_query()
	cur = db.exec( tlq )
	for r in cur:
		print(r['name'])
