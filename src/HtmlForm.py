from Model import Model

class HtmlForm:

	def __init__(self,model):
		self.model = model 

	def render(self,url,table):
		classes = None
		rv = []
		rv.append( "<form action='%s' METHOD='post' enctype='multipart-form-data'>\n" % url)
		for f in model.fields(table):
			rv.extend( self.field(table,f) )
		rv.append("</form>\n")
		return self.stringify(rv)

	def typeMap(self,table,field):
		schema = model.field(table,field)
		if 'formhint' in schema:
			return schema['formhint'] 
		if field in ['password'] or schema['type'] in ['password']:
			return 'password'
		if schema['type'] in ['enum']:
			return 'select'
		if schema['type'] in ['boolean']:
			return 'radio'
		return 'text'

	def field(self,table,fname):
		typ = self.typeMap(table,fname)
		inp = "  <input type='%s' id='%s' name='%s'>\n" % (typ,fname,fname)
		if typ in ['select']:
			inp = "  <select id='%s' name='%s'>\n" % (fname,fname)
			for ix,val in enumerate(self.model.values(table,fname)):
				inp += "  <option value='%d'>%s</option>\n" % (ix,val)
			inp += " </select>\n"
		
		rv = [ 
			" <div class='formgroup'>\n",
			"  <label for='%s'>%s:</label><br>\n" % (fname,fname.capitalize()),
			inp,
			" </div>\n"
		]
		return rv

	def stringify(self, slist ):
		rv = ''
		for s in slist:
			rv += str( s )
		return rv

if __name__ == '__main__':

	import sys
	print(sys.argv[1])
	model = Model( sys.argv[1] )
	form = HtmlForm( model )
	print(form.render('http://blah.com/edit','usr'))
	print(form.render('http://blah.com/edit','security'))
	print(form.render('http://blah.com/edit','mfa'))
	print(form.render('http://blah.com/edit','role'))
	
