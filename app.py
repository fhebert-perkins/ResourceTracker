from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, Response
from flask.bcrypt import Bcrypt
import MySQLdb
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                      user="tracker", # your username
                       passwd="password", # your password
                       db="Tracker")
app = Flask(__name__)
bcrypt = Bcrypt(app)
#app.config.from_pyfile('config.py')
app.config.update(dict(
	USERNAME='admin',
	PASSWORD='default',
	app_secretKey='aslkdfjalsdjkfalskdjfl3jlk1j2l3kj',
	app_debug=True,
	app_port=5000,
	SESSION_COOKIE_DOMAIN='coleyarbrough.com'
))
cur = db.cursor()
cur.execute('SET autocommit=1;')
login_info = {'temptemp':'temptemppassword', 'admin':'password'}
@app.route('/')
def root():
	return redirect(url_for('addtrans'))
@app.route('/search')
def search():
	return render_template('search.html')
@app.route('/history', methods=['GET','POST'])
def history():
	if session.get('logged_in'):
		if request.method == 'POST':
			pass
		return render_template('history.html')
	return redirect(url_for('login'))
@app.route('/addtrans', methods=['POST','GET'])
def addtrans():
	if session.get('logged_in'):
		cur.execute('SELECT * FROM TransType')
		types = cur.fetchall()
		cur.execute('SELECT * FROM Resources')
		resources = cur.fetchall()
		if request.method == 'POST':
			loginName = request.form['loginName']
			serialNumber = request.form['serialNumber']
			resource = request.form['resourceType']
			cur.execute('SELECT Name FROM Resources WHERE RID='+resource)
			resource = ''.join(cur.fetchall()[0])
			transType = request.form['transtype']
			cur.execute('SELECT TransTypeDesc FROM TransType WHERE TransOrder='+transType)
			transType = ''.join(cur.fetchall()[0])
			note = request.form['note']
			cur.execute('INSERT INTO `Transactions` (LoginName, SerialNumber, LaptopModel, TransType, `Notes`) VALUES (%s, %s, %s, %s, %s)', (loginName, serialNumber, resource, transType, note))
			return render_template('addtrans.html', transtypes=types, resourcetype=resources)
		return render_template('addtrans.html', transtypes=types, resourcetype=resources)
	return redirect(url_for('login'))
@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if request.method == 'POST':
		cur.execute('SELECT Password FROM Users WHERE Username=%s', (request.form['Username']))
		hashed_password = cur.fetchall()[0]
		if Bcrypt.check_password_hash(hashed_password, request.form['Password']):
			session['logged_in'] = True
			return redirect(url_for('addtrans'))
		else:
			return render_template('login.html')
	return render_template('login.html', error=error)
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))
@app.teardown_appcontext
def teardown():
	cur.close()
	db.close()
if __name__ == '__main__':
	app.secret_key = app.config['app_secretKey']
	app.run(debug=app.config['app_debug'], host='0.0.0.0', port=app.config['app_port'])
