import os
import psycopg2 as pg
import psycopg2.extras as pg_extras
from Sql import Sql
from Model import Model
from Sqlite import Sqlite

class Postgres(Sqlite):
	'''
	The service provider for an PostgreSQL database
	'''

	cx = None
	dbms = None
	model = None
	db_type = None
	dialect = None
	placeholder = '%s'
	tbl_list_qry = '''
		SELECT table_name as name 
			FROM information_schema.tables 
			WHERE table_schema = 'public' 
			ORDER BY name;
		'''

	def __init__(self, model=None):
		try:
			self.model = model 
			self.dbms = self.get_dsn()
			self.db_type = 'postgres'
			self.dialect = Sql(model = self.model)
			if not self.dbms:
				self.dbms = None
			self.cx = pg.connect(self.get_dsn() )
		except Exception as e:
			print( "DB Error %s" % e )

	def fix_dsn(self,key):
		if key in 'dbms':
			return 'dbname'
		if key in 'pass':
			return 'password'
		return key

	def get_dsn(self):
		dsn = ''
		secrets = self.get_secrets()
		if secrets:
			for k in ['dbms', 'host', 'user', 'pass', 'port']:
				if k in secrets:
					key = self.fix_dsn(k)
					dsn += '%s=%s ' % (key,secrets[k])
		return dsn

	def get_secrets(self):
		rv = {}
		secrets = self.model.secrets()
		for k in secrets.keys():
			rv[k] = os.getenv(secrets[k])
		return rv
	
	def get_cursor(self):
		try:
			return self.cx.cursor(cursor_factory = pg_extras.DictCursor)
		except Exception as e:
			print( 'get_cursor: %s' % e )
		return None

	def upsert(self,table,data):
		rv = self.dialect.insert(table,data)
		return rv[0:-1] + 'on conflict (%s) do update set %s ;' % (self.dialect.keys(table),self.dialect.assign_list(table,data))


if __name__ == '__main__':
	import sys

	model = Model(sys.argv[1])
	db = Postgres( model=model )
	print( db.get_dsn() )

	tlq = db.table_list_query()
	cur = db.exec( tlq )
	for r in cur:
		print(r[0])
	
