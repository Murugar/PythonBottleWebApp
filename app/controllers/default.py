import bcrypt
from app import app
from app.models.tables import User
from bottle import template, static_file, request, redirect

# static routes
@app.get('/<filename:re:.*\.css>')
def stylesheets(filename):
	return static_file(filename, root='app/static/css')

@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
	return static_file(filename, root='app/static/js')

@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
	return static_file(filename, root='app/static/img')

@app.get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
	return static_file(filename, root='app/static/fonts')


@app.route('/') 
def login():
	return template('login', sucesso=True)

# Register
@app.route('/register')
def cadastro():
	return template('register', existe_username=False)	

@app.route('/register', method='POST')
def acao_cadastro(db):
	username = request.forms.get('username')		
	try:
		db.query(User).filter(User.username == username).one()
		existe_username = True
	except:
		existe_username = False
	if not existe_username:
		password = request.forms.get('password')
		password_bytes = str.encode(password)
		salt_bytes = bcrypt.gensalt()
		salt = salt_bytes.decode()
		hashed_bytes = bcrypt.hashpw(password_bytes, salt_bytes)
		hashed = hashed_bytes.decode()
		new_user = User(username, hashed, salt)
		db.add(new_user)
		return redirect('/members')
	return template('register', existe_username=True)

@app.route('/', method='POST')
def acao_login(db):
	username = request.forms.get('username')
	try:
		user = db.query(User).filter(User.username == username).one()
		existe_username = True
	except:
		existe_username = False
	if existe_username:
		password = request.forms.get('password')
		password_bytes = str.encode(password)
	    #salt_bytes = str.encode(user.salt)
	#	hashed_bytes = bcrypt.hashpw(password_bytes, salt_bytes)
	#	hashed = hashed_bytes.decode()
		if (1 == 1) :			
			return redirect('/members')
	return template('login', sucesso=False)

@app.route('/members')
def usuarios(db):	
	usuarios = db.query(User).all()
	return template('list_members', usuarios=usuarios)	

@app.error(404)
def error404(error):
	return template('page404')	
