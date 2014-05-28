from flask import Flask, request, redirect, url_for, session, render_template, send_from_directory # Web library requirements
import MySQLdb  # mysql library
import keygen  # generate random 64 bits of entropy for the application secret key
import random  # random secret key every run
from werkzeug.security import generate_password_hash, check_password_hash # for salted passwords


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
	SESSION_COOKIE_DOMAIN='coleyarbrough.com'
)) # application configuration

db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
cur = db.cursor() # initiates database cursor
try:
	cur.execute('SET autocommit=1;') # sets the database to autocommit changes
except:
	db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
	cur.execute('SET autocommit=1;')



@app.route('/')
def root():
	return redirect(url_for('addtrans')) # if / is served, redirects webbrowser to the add transaction page
@app.route('/search')
def search():
	if session.get('logged_in'): # checks if session is logged in, if so passes search form
		return render_template('search.html') # serves search form
	return redirect(url_for('login')) # redirects to login if user is not logged in

@app.route('/history', methods=['GET','POST']) # request methods allowed Post and Get
def history():
	if session.get('logged_in'): # checks if session is logged in if so passes to authorized only values
		if request.method == 'POST': # if the request method is post
			if request.form['serialNumber'] != '': # if serial number is present, use that to 
				try:
					cur.execute('SELECT * FROM Transactions WHERE SerialNumber=%s', request.form['serialNumber']) 
				except:
					db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
					cur.execute('SELECT * FROM Transactions WHERE SerialNumber=%s', request.form['serialNumber'])
				data = cur.fetchall()
				return render_template('history.html', data=data) # renders template with rows
			elif request.form['loginName'] != '':
				try:
					cur.execute('SELECT * FROM Transactions WHERE LoginName=%s', request.form['loginName'])
				except:
					db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
					cur.execute('SELECT * FROM Transactions WHERE LoginName=%s', request.form['loginName'])
				data = cur.fetchall()
				return render_template('history.html', data=data)
			elif request.form['resource'] != '':
				try:
					cur.execute('SELECT * FROM Transactions WHERE LaptopModel=%s', request.form['resource'])
				except:
					db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
					cur.execute('SELECT * FROM Transactions WHERE LaptopModel=%s', request.form['resource'])
				data = cur.fetchall()
				return render_template('history.html', data=data)
			elif request.form['transactionType'] != '':
				try:
					cur.execute('SELECT * FROM Transactions WHERE TransType=%s', request.form['transactionType'])
				except:
					db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
					cur.execute('SELECT * FROM Transactions WHERE TransType=%s', request.form['transactionType'])
				data = cur.fetchall()
				return render_template('history.html', data=data)
			else:
				return render_template('history.html')
		return redirect(url_for('serach'))
	return redirect(url_for('login'))

@app.route('/addtrans', methods=['POST','GET']) # adds transactions to the Transactions database
def addtrans():
	if session.get('logged_in'): # checks if logged in 
		try:
			cur.execute('SELECT * FROM TransType')
		except:
			db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
			cur.execute('SELECT * FROM TransType')
		types = cur.fetchall()
		try:
			cur.execute('SELECT * FROM Resources')
		except:
			db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
			cur.execute('SELECT * FROM Resources')
		resources = cur.fetchall()
		if request.method == 'POST':
			loginName = request.form['loginName']
			serialNumber = request.form['serialNumber']
			resource = request.form['resourceType']
			try:
				cur.execute('SELECT Name FROM Resources WHERE RID='+resource)
			except:
				db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
				cur.execute('SELECT Name FROM Resources WHERE RID='+resource)
			resource = ''.join(cur.fetchall()[0])
			transType = request.form['transtype']
			try:
				cur.execute('SELECT TransTypeDesc FROM TransType WHERE TransOrder='+transType)
			except:
				db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
				cur.execute('SELECT TransTypeDesc FROM TransType WHERE TransOrder='+transType)
			transType = ''.join(cur.fetchall()[0])
			note = request.form['note']
			try:
				cur.execute('INSERT INTO `Transactions` (LoginName, SerialNumber, LaptopModel, TransType, `Notes`) VALUES (%s, %s, %s, %s, %s)', (loginName, serialNumber, resource, transType, note))
			except:
				db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
				cur.execute('INSERT INTO `Transactions` (LoginName, SerialNumber, LaptopModel, TransType, `Notes`) VALUES (%s, %s, %s, %s, %s)', (loginName, serialNumber, resource, transType, note))
			return render_template('addtrans.html', transtypes=types, resourcetype=resources)
		return render_template('addtrans.html', transtypes=types, resourcetype=resources)
	return redirect(url_for('login'))
@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'admin':
			if check_password_hash(app.config['adminPassword'], request.form['password']):
				session['logged_in'] = True
				return redirect(url_for('admin'))
			else:
				return render_template('login.html', error='Incorrect Username/password')
		else:
			try:
				cur.execute('SELECT Password FROM Users WHERE Username=%s', (request.form['username']))
			except:
				db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
				cur.execute('SELECT Password FROM Users WHERE Username=%s', (request.form['username']))
			hashed_password = str(cur.fetchall()[0][0])
			if check_password_hash(hashed_password, request.form['password']):
				session['logged_in'] = True
				return redirect(url_for('addtrans'))
			else:
				return render_template('login.html', error=hashed_password)
	return render_template('login.html', error=error)
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
			password = generate_password_hash(request.form['password'])
			try:
				cur.execute('INSERT INTO Users (`Username`, `Password`) VALUES (%s, %s)', (request.form['username'], password))
			except:
				db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
				cur.execute('INSERT INTO Users (`Username`, `Password`) VALUES (%s, %s)', (request.form['username'], password))

			return render_template('adduser.html', updated=True)
		return render_template('adduser.html')
	return redirect(url_for('login'))
@app.route('/'+adminpanelURI, methods=['GET', 'POST'])
def admin():
	if session.get('logged_in'):
		if request.method == 'POST':
			if request.form['btn'] == 'add resource':
				try:
					cur.execute('INSERT INTO Resources (`ResourceName`, `ResourceType`) VALUES (%s, %s)', (request.form['resourceName'], request.form['resourceType']))
				except:
					db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
					cur.execute('INSERT INTO Resources (`Name`, `Type`) VALUES (%s, %s)', (request.form['resourceName'], request.form['resourceType']))
				return render_template('adminpanel.html', adminURL=adminpanelURI)
			if request.form['btn'] == 'add transaction':
				try:
					cur.execute('INSERT INTO Transactions (Transaction) VALUES (%s)', (request.form['transactionName']))
				except:
					db = MySQLdb.connect(host=app.config['sql_host'], user=app.config['sql_user'], passwd=app.config['sql_password'], db=app.config['sql_db']) # initiates mysql connection
					cur.execute('INSERT INTO Transactions (Transaction) VALUES (%s)', (request.form['transactionName']))
				return render_template('adminpanel.html', adminURL=adminpanelURI)
		return render_template('adminpanel.html', adminURL=adminpanelURI)
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.secret_key = app.config['app_secretKey']
	app.run(debug=app.config['app_debug'], host='0.0.0.0', port=app.config['app_port'])
