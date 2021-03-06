from Config import Config

class Model(object):
	'''
	A class to take a specific yml file and model either a database table
	or a view of one in accordance with the MVC design pattern. Yadda yadda.
	'''

	config = None
	model = None

	def __init__(self,cfg=None):
		try:
			self.config = Config(cfg)
			defined = self.config.objects()
			if 'database' in defined:
				self.model = self.config.object('database')

		except Exception as e:
			print( "MODEL ERROR: %s" % e )
		
	def secrets(self):
		return self.config.object('secrets')

	def enums(self,table):
		rv=[]
		for f in self.fields(table):
			schema = self.field(table,f)
			if 'enum' in schema['type']:
				rv.append(f)
		return rv

	def server(self):
		return self.config.object('server')

	def tables(self):
		rv = []
		for t in self.model['tables']:
			rv.append(t)
		return rv

	def table(self,table):
		return self.model['tables'][table]

	def fields(self,table):
		rv = []
		if table in self.tables():
			schema = self.model['tables'][table]['fields']
			for f in schema.keys():
				rv.append(f)
		return rv

	def field(self,table,field):
		return self.model['tables'][table]['fields'][field]

	def values(self,table,field):
		schema = self.field(table,field)
		if 'type' in schema and schema['type'] == 'enum':
			return schema['values']
		return None

	def version(self,table):
		return self.model['tables'][table]['version']

	def key(self,table):
		if 'keys' in self.model['tables'][table]:
			return self.model['tables'][table]['keys']
		return None

	def payload(self,table):
		keys = self.key(table)
		fields = self.fields(table)
		if not keys:
			return fields
		return list(set(fields)-set(keys))

	def check_table(self,table):
		if table in self.tables():
			return True
		return False

	def check_fields(self,table,fields):
		if self.check_table(table):
			good_fields = self.fields(table)
			for f in fields:
				if f not in good_fields:
					return False
		return True

if __name__ == '__main__':

	import sys

	model = Model( sys.argv[1] )
	for t in model.tables():
		for f in model.enums(t):
			print(t,f,model.values(t,f))

