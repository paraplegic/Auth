
class HtmlTable():
	'''
	Tied to Bootstrap table classes, this will render a
	list of dicts to an html table with some decoration
	and add a class to each <TABLE> element to make it 
	clickable via some jQuery magic.  This is done in
	the root file in the Jinja2 templating system, and
	all templates which inherit from the root can access it.
	'''

	def __init__(self):
		pass

	def render(self, dlist):
		rv = [
			'<div class="table-responsive">',
			'<table class="table table-striped clickable">',
		]
		rv.append('<thead>')
		keys = dlist[0].keys()
		for k in keys:
			rv.append('<td>%s</td>'%k.capitalize())
		rv.append('</thead>')
		for d in dlist:
			rv.append('<tr data-href="">')
			for k in keys:
				if k in 'password':
					rv.append('<td>%s</td>'%'*****')
				else:
					rv.append('<td>%s</td>'%d[k])
			rv.append('</tr>')

		rv.append('</table>')
		rv.append('</div>')
		return rv

	def stringify(self, slist ):
		rv = ''
		for s in slist:
			rv += str( s )
		return rv
