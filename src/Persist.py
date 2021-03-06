from Model import Model

class Db_Error(Exception):
	pass

class Persist():

	model = None
	provider = None

	def __init__(self, provider=None ):
		if provider:
			self.provider = provider
			self.model = provider.model
		self.validateModel()

	def get(self, source, data ):
		qry = self.provider.dialect.select(source,data)
		return self.provider.exec(qry)

	def put(self, source, data ):
		qry = self.provider.dialect.safe_insert(source,data,self.provider.placeholder)
		try:
			c = self.provider.safe_exec(qry,data)
			self.commit()
			return True

		except Exception as e:
			print( 'ERROR: (put) %s' % e )
			self.edit(source,data)

		return False

	def edit(self, source, data ):
		qry = self.provider.upsert.safe_insert(source,data)
		print("::::", qry)
		try:
			c = self.provider.exec(qry)
			self.commit()
			return True

		except Exception as e:
			print( 'ERROR: (edit) %s' % e )

		return False

	def revision(self,table,ver):
		self.query(self.provider.dialect.insert('model', {'tab': table, 'version': str(ver) } ))
		self.commit()
		
	def instantiate(self,table):
		v = self.model.version(table)
		sch = self.provider.dialect.schema(table)
		try:
			print("-- Instantiating %s: (version: %s)" % (table,self.model.version(table)),end='')
			cursor = self.provider.get_cursor()
			for cmd in sch:
				cursor.execute(cmd)
			self.revision(table,v)
			print( ' [ok]' )

		except Exception as e:
			print(' fail: %s' % e )

	def table_list(self):
		return [t['name'] for t in self.provider.table_list()]

	def validateModel(self):
		missing = []
		expected = self.model.tables()
		actual = self.table_list()

		if len(actual) == 0:
			for t in expected:
				self.instantiate(t)
			return

		if len(actual) > 0:
			print("Validating db against model: ", end='')
			missing = list(set(expected)-set(actual))

		if len(missing) < 1:
			print("model check complete: [ok]")
			return

		## instantiate relies upon the model table existing 
		## before the rest, so create it first.
		if 'model' in missing:
			missing.remove('model')
			self.instantiate('model')

		for t in missing:
			self.instantiate(t)

	def commit(self):
		return self.provider.cx.commit()

	def close(self):
		return self.provider.cx.close()

	def query(self,qry):
		return self.provider.exec(qry)

if __name__ == '__main__':

	import sys
	from Sqlite import Sqlite
	from Postgres import Postgres
	from MySql import MySql

	db = None
	if sys.argv[2] == 'sqlite':
		db = Sqlite( model = Model(sys.argv[1]) )

	if sys.argv[2] == 'postgres':
		db = Postgres( model = Model(sys.argv[1]) )

	if sys.argv[2] == 'mysql':
		db = MySql( model = Model(sys.argv[1]) )

	print('dbStore: %s' % sys.argv[2] )
	store = Persist( provider = db )
	print("db:", db.database())
	print("server:", store.model.server())
	print("secrets:", store.model.secrets())
	
	data = { 'uname': 'xyz', 'email': 'x@y.z', 'password': 'xyzzyMoo', 'authenticated': True, 'active': True }
	question = { 'email': 'x@y.z', 'question': 'who cuts your hair?', 'answer': 'my mom' }

	store.put( 'usr', data )
	for u in store.get( 'usr', {'email': 'x@y.z'} ):
		print(u)

	store.put( 'security', question )
	for q in store.get( 'security', {'email': 'x@y.z'} ):
		print(q)
