from Model import Model

class Sql:

	model = None 
	def __init__(self,model=None):
		self.model = model
		
	def schema(self,table):
		rv = None
		try:
			schema = self.model.table(table)
			rv = 'create table %s (\n' % table
			for fld in self.model.fields(table):
				field = self.model.field(table,fld)
				typ = field['type']
				if typ in ['enum', 'password']:
					if typ == 'enum':
						typ = 'integer'
					else:
						typ = 'text'
				rv += ' %s %s' % (fld,typ)
				if 'constraints' in field:
					rv += ' %s' % ' '.join(field['constraints'])
				rv += ',\n'

			if 'keys' in schema:
				rv += ' primary key( %s )\n' % ",".join(schema['keys'])
			else:
				rv = rv[0:-2]

			rv += ');\n'
			if 'index' in schema:
				rv += 'create index %s_ix on %s ( %s );\n' % (table,table,','.join(schema['index']))
			return rv

		except Exception as e:
			print( "OOPS: %s" % e )

	def check_table(self,table):
		if table in self.model.tables():
			return True
		return False

	def check_fields(self,table,fields):
		if self.check_table(table):
			good_fields = self.model.fields(table)
			for f in fields:
				if f not in good_fields:
					print( "field %s is missing." % f )
					return False
		return True

	def mapdata(self,table,data):
		rv = ""
		for f in self.model.fields(table):
			schema = self.model.field(table,f)
			if schema['type'] in ['integer', 'float']:
				rv += str(data[f]) + ','
			else:
				rv += "'%s'," % data[f]
		return rv[0:-1]

	def insert(self,table,data):
		rv = ""
		good_table =  self.check_table( table )
		good_fields =  self.check_fields( table, data.keys() )
		if good_table and good_fields:
			model_fields = self.model.fields(table)
			rv = "insert into %s ( %s ) values ( %s );\n" % (table,",".join(model_fields),self.mapdata(table,data))
			return rv

	def delete(self,table,data):
		pass

	def update(self,table,data):
		pass



if __name__ == '__main__':

	import sys

	model = Model(sys.argv[1])
	sql = Sql( model = model )

	print( sql.model.database() )
	print( sql.model.tables() )
	for t in sql.model.tables():
		print("-- TABLE %s: (VER: %s)" % (t,sql.model.version(t)))
		print(sql.schema(t))
