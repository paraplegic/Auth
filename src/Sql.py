from Model import Model

class Sql:

	model = None 
	def __init__(self,model=None):
		self.model = model
		
	def schema(self,table):
		rv = []
		try:
			model = self.model.table(table)
			sch = 'CREATE TABLE IF NOT EXISTS ''%s'' (\n' % table
			for fld in self.model.fields(table):
				field = self.model.field(table,fld)
				typ = field['type']
				if typ in ['enum', 'password']:
					if typ == 'enum':
						typ = 'integer'
					else:
						typ = 'text'
				sch += ' %s %s' % (fld,typ)
				if 'constraints' in field:
					sch += ' %s' % ' '.join(field['constraints'])
				sch += ',\n'
 
			if 'keys' in model:
				sch += ' primary key( %s )\n' % ",".join(model['keys'])
			else:
				rv = rv[0:-2]

			sch += ');\n'
			rv.append(sch)
			if 'index' in model:
				rv.append('create index %s_ix on %s ( %s );\n' % (table,table,','.join(model['index'])))
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

	def mapfield(self,table,field,data):
		schema = self.model.field(table,field)
		if schema['type'] in ['integer', 'float', 'boolean']:
			return str(data[field])
		return "'%s'" % data[field]
		
	def mapdata(self,table,data):
		rv = ""
		for f in self.model.fields(table):
			rv += self.mapfield(table,f,data) + ','
		return rv[0:-1]

	def insert(self,table,data):
		rv = ""
		good_table =  self.check_table( table )
		good_fields =  self.check_fields( table, data.keys() )
		if good_table and good_fields:
			model_fields = self.model.fields(table)
			return 'INSERT INTO %s ( %s ) VALUES ( %s ) ;' % (table,",".join(model_fields),self.mapdata(table,data))

	def safe_insert(self,table,data,placeholder):
		good_table = self.check_table(table)
		good_fields = self.check_fields(table,data.keys())
		if good_table and good_fields:
			flist = self.model.fields(table)
			vlist = ",".join( [placeholder] * len(flist))
			return 'INSERT INTO %s ( %s ) VALUES ( %s ) ;' % (table,','.join(flist), vlist)
		return None
		
	def assign_list(self,table,data):
		a_list = []
		for f in self.model.payload(table):
			if f in data:
				a_list.append( "%s=%s" % (f,self.mapfield(table,f,data)) )
		return ', '.join( a_list )

	def where_list(self,table,data):
		w_list = []
		for k in self.model.key(table):
			if k in data:
				w_list.append( "%s=%s" % (k,self.mapfield(table,k,data)) )
		return ' and '.join( w_list )
	
	def update(self,table,data):
		return 'UPDATE %s SET %s WHERE %s;' % (table,self.assign_list(table,data),self.where_list(table,data))

	def delete(self,table,data):
		return "DELETE FROM %s WHERE %s;" % (table,self.where_list(table,data))

	def select(self,table,data):
		if data:
			return "SELECT * FROM %s WHERE %s ;" % (table,self.where_list(table,data))
		return "SELECT * FROM %s ;" % table


if __name__ == '__main__':

	import sys

	model = Model(sys.argv[1])
	sql = Sql( model = model )

	print( sql.model.tables() )
	for t in sql.model.tables():
		print("-- TABLE %s: (VER: %s)" % (t,sql.model.version(t)))
		for s in sql.schema(t):
			print(s)

	data = { 'uname': 'xyz', 'email': 'x@y.z', 'password': 'xyzzyMoo', 'authenticated': True, 'active': True }
	question = { 'email': 'x@y.z', 'question': 'who cuts your hair?', 'answer': 'my mom' }

	print( sql.insert( 'usr', data ) )
	print( sql.safe_insert( 'usr', data, '?' ) )
	print( sql.update( 'usr', data ) )
	print( sql.delete( 'usr', data ) )
	print( sql.select( 'usr', data ) )
	print( sql.select( 'usr', None ) )

	print( sql.insert( 'security', question ) )
	print( sql.safe_insert( 'security', question, '?' ) )
	print( sql.update( 'security', question ) )
	print( sql.delete( 'security', question ) )
	print( sql.select( 'security', question ) )
	print( sql.select( 'security', None ) )

