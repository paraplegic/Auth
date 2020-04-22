import jwt
from fastapi import FastAPI, Form, Body, Request
from starlette.templating import Jinja2Templates
from starlette.responses import Response, RedirectResponse

from Model import Model
from HtmlForm import HtmlForm

class EndPoint():

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

templates = Jinja2Templates(directory="../../templates")
app = FastAPI()

@app.middleware('http')
async def before(request: Request, callback):

	request.state.usr = None
	if 'X-JWT-Token' in request.cookies:
		token = request.cookies['X-JWT-Token']
		if token and len(token) > 0:
			usr = jwt.decode( token, SECRET, algorithms = ['HS256'])
			request.state.usr = usr
			return await callback(request)

	if request['path'] in ['/login', '/auth', '/register', '/index' ]:
		return await callback(request)

	return RedirectResponse(url='/login')


@app.get( '/register' )
def register(request: Request):
	context['request'] = request
	context['form'] = views.render( '/auth', 'register')
	return templates.TemplateResponse('register.html',context)

@app.get( '/index' )
def root(request: Request):
	context['request'] = request
	return templates.TemplateResponse('bootstrap.html',context)

@app.get( '/users' )
def users(request: Request):
	context['request'] = request
	return 'users'
	
@app.get( '/login' )
def login(request: Request):
	context['request'] = request
	context['form'] = views.render('/auth','login')
	return templates.TemplateResponse('login.html',context)
	
@app.post( '/auth' )
def auth(request: Request):
	context['request'] = request
	usr = request.state.usr
	return usr

@app.get( '/logout' )
def logout(request: Request):
	context['request'] = request
	response = RedirectResponse( url = '/login' )
	response.delete_cookie(key='X-JWT-Token')
	return response

ep = EndPoint()
ep.add( '/index', 'Home' )
ep.add( '/register', 'Register' )
ep.add( '/login', 'Login' )
ep.add( '/logout', 'Logout' )

ad = EndPoint()
ad.add( '/userad', 'Administer' )
ad.add( '/revoke', 'Revoke' )
ad.add( '/blah', 'Blah' )

context = {}
context['administer'] = ad.render()
context['navigation'] = ep.render()
context['app'] = 'Turnout'
context['version'] = 0.9

model = Model('../../resources/model/users.yml')
view = Model('../../resources/view/users.yml')
forms = HtmlForm(model)
views = HtmlForm(view)
SECRET='ThisDog can Hunt!'
VERSION=0.9


if __name__ == '__main__':
	pass
