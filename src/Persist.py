from Model import Model

class Persist():

	model = None
	provider = None

	def __init__(self, provider=None ):
		if provider:
			self.provider = provider
			self.model = provider.model

		self.validateModel()

	def connect(self):
		pass

	def get(self, source, data ):
		pass

	def put(self, source, data ):
		pass

	def revision(self,table,ver):
		self.query(self.provider.dialect.insert('model', {'tab': table, 'version': ver } ))
		self.commit()
		
	def instantiate(self,table):
		cursor = self.provider.get_cursor()
		v = self.model.version(table)
		cursor.execute(self.provider.dialect.schema(table))
		self.revision(table,v)

	def table_list(self):
		rv = []
		for d in self.query(self.provider.table_list_query()):
			rv.append(d['name'])
		return rv

	def validateModel(self):
		db_tables = self.table_list()
		model = self.model.tables()
		print("Validating db against model: ", end='')
		missing = list(set(model)-set(db_tables))
		if len(missing) < 1:
			print("ok")
		if 'model' in missing:
			missing.remove('model')
			self.instantiate('model')
		if len(missing) > 0:
			print("missing tables: %s" % missing)
		for t in missing:
			print("-- Instantiating %s: (version: %s)" % (t,self.model.version(t)))
			self.instantiate(t)

	def commit(self):
		return self.provider.cx.commit()

	def query(self,query):
		cursor = self.provider.get_cursor()
		return cursor.execute(query)

if __name__ == '__main__':

	import sys
	from Sqlite import Sqlite

	db = Sqlite( model = Model(sys.argv[1]) )

	store = Persist( provider = db )
	print("db:", store.model.database())
	print("server:", store.model.server())
	print("secrets:", store.model.secrets())
	for t in store.model.tables():
		print(t, store.model.key(t), store.model.version(t))
		for f in store.model.fields(t):
			print("\t", f, store.model.field(t,f))
			ev = store.model.values(t,f)
			if ev:
				print("\tenum values:", store.model.values(t,f))

