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

	def __init__(self, model=None):
		try:
			self.model = model 
			self.dbms = self.get_dbpath()
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
	
	def get_dbpath(self):
		secrets = self.get_secrets()
		return os.path.join(secrets['path'],secrets['dbms'])

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

	def type(self):
		return self.db_type

	def database(self):
		return self.dbms

	def table_list_query(self):
		return "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'";

	def variable_list_query(self, table):
		pass


if __name__ == '__main__':
	import sys

	model = Model(sys.argv[1])
	db = Sqlite( model=model )
	print( db.get_dbpath() )
	print( 'tables:', db.table_list_query() )
	
