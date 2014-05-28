from flask import Flask, request, redirect, url_for, session, render_template, send_from_directory, flash # Web library requirements
import MySQLdb  # mysql library
import keygen  # generate random 64 bits of entropy for the application secret key
import random  # random secret key every run
from werkzeug.security import generate_password_hash, check_password_hash # for salted passwords
import os


app = Flask(__name__) # initiates flask webap
adminpanelURI=''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890') for _ in range(10)) # url for the admin panel
#app.config.from_pyfile('config.py')
app.config.update(dict(
	USERNAME='admin',
	PASSWORD='default',
	app_secretKey=keygen.key(),
	app_debug=True,
	app_port=5000,
	app_hashKey='derpderpderp',
	adminPassword=generate_password_hash('password'),
	sql_host='localhost',
	sql_user='tracker',
	sql_password='password',
	sql_db='Tracker',
	#SESSION_COOKIE_DOMAIN='coleyarbrough.com'
)) # application configuratio

def select(query):
	flash(query) #debug
	db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db'])
	cur = db.cursor()
	cur.execute(query)
	toreturn=cur.fetchall()
	cur.close()
	db.close()
	return toreturn
def insert(query):
	flash(query) #debug
	db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db'])
	cur = db.cursor()
	cur.execute(query)
	cur.close()
	db.close()

@app.route('/')
def root():
	return redirect(url_for('addtrans')) # if / is served, redirects webbrowser to the add transaction page
@app.route('/search')
def search():
	if session.get('logged_in'): # checks if session is logged in, if so passes search form
		types = select('SELECT * FROM TransType')
		resources = select('SELECT * FROM Resources')
		return render_template('search.html', transtypes=types, resourcetype=resources) # serves search form
	return redirect(url_for('login')) # redirects to login if user is not logged in

@app.route('/history', methods=['GET','POST']) # request methods allowed Post and Get
def history():
	if session.get('logged_in'): # checks if session is logged in if so passes to authorized only values
		if request.method == 'POST': # if the request method is post
			if request.form['serialNumber'] != '': # if serial number is present, use that to 
				data = select('SELECT * FROM Transactions WHERE SerialNumber=\'%s\'' % request.form['serialNumber'])
				return render_template('history.html', data=data) # renders template with rows
			elif request.form['loginName'] != '':	
				data = select('SELECT * FROM Transactions WHERE LoginName=%s' % request.form['loginName'])
				return render_template('history.html', data=data)
			elif request.form['resource'] != '':				
				data = select('SELECT * FROM Transactions WHERE LaptopModel=%s'% request.form['resource'])
				return render_template('history.html', data=data)
			elif request.form['transactionType'] != '':
				data = select('SELECT * FROM Transactions WHERE TransType=%s'% request.form['transactionType'])
				return render_template('history.html', data=data)
			else:
				return render_template('history.html')
		return redirect(url_for('search'))
	return redirect(url_for('login'))

@app.route('/addtrans', methods=['POST','GET']) # adds transactions to the Transactions database
def addtrans():
	if session.get('logged_in'): # checks if logged in 
		types = select('SELECT * FROM TransType')
		resources = select('SELECT * FROM Resources')
		if request.method == 'POST':
			loginName = request.form['loginName']
			serialNumber = request.form['serialNumber']
			resource = request.form['resourceType']
			resource = ''.join(select('SELECT Name FROM Resources WHERE RID='+resource)[0])
			transType = request.form['transtype']
			transType = ''.join(select('SELECT TransTypeDesc FROM TransType WHERE TransOrder='+transType)[0])
			note = request.form['note']
			insert('INSERT INTO `Transactions` (LoginName, SerialNumber, LaptopModel, TransType, `Notes`) VALUES (%s, %s, %s, %s, %s)' % (loginName, serialNumber, resource, transType, note))
			return render_template('addtrans.html', transtypes=types, resourcetype=resources)
		return render_template('addtrans.html', transtypes=types, resourcetype=resources)
	return redirect(url_for('login'))
@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if not session.get('logged_in'):
		if request.method == 'POST':
			if request.form['username'] == 'admin':
				if check_password_hash(app.config['adminPassword'], request.form['password']):
					session['logged_in'] = True
					return redirect(url_for('admin'))
				else:
					return render_template('login.html', error='Incorrect Username/password')
			else:	
				hashed_password = select('SELECT Password FROM Users WHERE Username=\'%s\'' % (request.form['username']))
				flash(hashed_password)
				if check_password_hash(hashed_password, request.form['password']):
					session['logged_in'] = True
					return redirect(url_for('addtrans'))
				else:
					return render_template('login.html', error=hashed_password)
		return render_template('login.html', error=error)
	return redirect(url_for('addtrans'))
@app.route('/logout')
def logout():
	print session.get('logged_in')
	if session.get('logged_in'):
		session.pop('logged_in', None)
		return redirect(url_for('login'))
	return redirect(url_for('login'))
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
	if session.get('logged_in'):
		if request.method == 'POST':
			
			return render_template('adduser.html', updated=True)
		return render_template('adduser.html')
	return redirect(url_for('login'))
@app.route('/'+adminpanelURI, methods=['GET', 'POST'])
def admin():
	if session.get('logged_in') == True:
		if request.method == 'POST':
			if request.form['btn'] == 'add resource':
				insert('INSERT INTO Resources (`ResourceName`, `ResourceType`) VALUES (%s, %s)' %(request.form['resourceName'], request.form['resourceType']))
				flash('New resource '+request.form['resourceName']+' added')
				return render_template('adminpanel.html', adminURL=adminpanelURI)
			if request.form['btn'] == 'add transaction':	
				insert('INSERT INTO Transactions (Transaction) VALUES (%s)' % (request.form['transactionName']))
				flash('New transaction '+reques.form['transactionName']+' added')
				return render_template('adminpanel.html', adminURL=adminpanelURI)
			if request.form['btn'] == 'create user':
				password = generate_password_hash(request.form['password'])
				insert('INSERT INTO Users (`Username`, `Password`) VALUES (\'%s\', \'%s\')' % (request.form['username'], password))
				flash('New user "'+request.form['username']+'" added')
				return render_template('adminpanel.html', adminpanel=adminpanelURI)
		return render_template('adminpanel.html', adminURL=adminpanelURI)
	return redirect(url_for('login'))
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
	app.secret_key = app.config['app_secretKey']
	app.run(debug=app.config['app_debug'], host='0.0.0.0', port=app.config['app_port'])
