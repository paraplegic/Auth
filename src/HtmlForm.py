from Model import Model

class EndPoint:
	'''
	A class to define the menu entries for a form application
	in html ... uses Bootstrap classes to define the entries
	in a dropdown menu link item
	'''

	def __init__(self):
		self.navList = []
		pass

	def add(self,url,label):
		self.navList.append( {'url': url, 'label': label} )

	def render(self):
		rv = []
		for ep in self.navList:
			rv.append('<li><a href="%s">%s</a></li>' % (ep['url'],ep['label']))
		return rv


class HtmlForm:
	'''
	A class to create an HtmlForm which can correspond either to a
	db model, or a view as provided by the Model class.
	'''

	def __init__(self,model):
		self.model = model 

	def render(self,url,table):
		classes = None
		rv = []
		rv.append( "<form action='%s' METHOD='post' enctype='multipart-form-data'>\n" % url)
		for f in self.model.fields(table):
			rv.extend( self.field(table,f) )
		rv.append(self.button('submit', 'Submit'))
		rv.append(self.button('reset','Reset'))
		rv.append("</form>\n")
		return self.stringify(rv)

	def button(self,typ,label):
		rv = " <div class='formgroup'>\n"
		rv += "<br><button class='btn btn-primary' type='%s' value='%s'>%s</button>\n" % (typ,typ,label)
		rv += " </div>"
		return rv

	def typeMap(self,table,field):
		schema = self.model.field(table,field)
		if 'formhint' in schema:
			return schema['formhint'] 
		if field in ['password'] or schema['type'] in ['password']:
			return 'password'
		if schema['type'] in ['enum']:
			return 'select'
		if schema['type'] in ['boolean']:
			return 'checkbox'
		return 'text'

	def fieldLabel(self,table,fname):
		sch = self.model.field(table,fname)
		if 'label' in sch:
			return sch['label']
		return fname.capitalize()

	def field(self,table,fname):
		typ = self.typeMap(table,fname)
		inp = "  <input type='%s' id='%s' name='%s'>\n" % (typ,fname,fname)
		if typ in ['select']:
			inp = "  <select id='%s' name='%s'>\n" % (fname,fname)
			for ix,val in enumerate(self.model.values(table,fname)):
				inp += "  <option value='%d'>%s</option>\n" % (ix,val)
			inp += " </select>\n"

		if typ not in ['radio', 'checkbox']:
			inp = '  <br>' + inp
		
		rv = [ 
			" <div class='formgroup'>\n",
			"  <label for='%s'>%s:</label>\n" % (fname,self.fieldLabel(table,fname)),
			inp,
			" </div>\n"
		]
		return rv

	def list(self):
		return self.model.tables()

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
	
