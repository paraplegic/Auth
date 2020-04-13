import os
import mysql.connector
from Sql import Sql
from Model import Model
from Sqlite import Sqlite

class MySql(Sqlite):
	'''
	The service provider for an MySQL database
	'''

	cx = None
	dbms = None
	model = None
	db_type = None
	dialect = None
	placeholder = '%s'
	tbl_list_qry = '''
		SELECT table_name as name FROM information_schema.tables where table_schema = '%s';
	'''

	def __init__(self, model=None):
		try:
			self.model = model 
			self.dbms = self.get_dsn()
			self.db_type = 'postgres'
			self.dialect = Sql(model = self.model)
			if not self.dbms:
				self.dbms = None
			self.cx = mysql.connector.connect(**self.get_dsn(),auth_plugin='mysql_native_password')
		except Exception as e:
			print( "DB Error %s" % e )

	def fix_dsn(self,key):
		if key in 'dbms':
			return 'database'
		if key in 'pass':
			return 'password'
		return key

	def get_dsn(self):
		secrets = self.get_secrets()
		if secrets:
			dsn = {}
			for k in ['dbms', 'host', 'user', 'pass', 'port']:
				if k in secrets:
					key = self.fix_dsn(k)
					dsn[key] = secrets[k]
			return dsn
		return None
			
	def xget_dsn(self):
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

	def table_list_query(self):
		dsn = self.get_dsn()
		return self.tbl_list_qry % dsn['database']
	
	def get_cursor(self):
		rv = None
		try:
			rv = self.cx.cursor(dictionary=True)
			return rv
		except Exception as e:
			print( 'get_cursor: %s' % e )
			return rv

	def upsert(self,table,data):
		rv = self.dialect.insert(table,data)
		return rv[0:-1] + 'on duplicate key do update set %s ;' % self.dialect.assign_list(table,data)


if __name__ == '__main__':
	import sys

	model = Model(sys.argv[1])
	db = MySql( model=model )
	print( db.get_dsn() )

	tlq = db.table_list_query()
	cur = db.exec( tlq )
	for r in cur:
		print(r['name'])
