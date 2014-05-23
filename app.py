from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, Response
import MySQLdb
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                      user="root", # your username
                       passwd="password", # your password
                       db="Tracker")
app = Flask(__name__)
#app.config.from_pyfile('config.py')
app.config.update(dict(
	USERNAME='admin',
	PASSWORD='default',
	app_secretKey='aslkdfjalsdjkfalskdjfl3jlk1j2l3kj',
	app_debug=True,
	app_port=5000
))
cur = db.cursor()

login_info = {'temptemp':'temptemppassword', 'admin':'password'}
@app.route('/')
def root():
	return redirect(url_for('getinfo'))
@app.route('/getinfo', methods=['GET','POST'])
def getinfo():
	if session.get('logged_in'):
		transactions = cur.execute('SELECT * FROM transtype')
		if request.method == 'post':
			if request.form['btn'] == 'search':
				query = []
				form = request.form
				search = {'SerialNumber': False, 'CaseNumber': False, 'FirstName': False, 'LastName': False}
				for key in form:
					if form[key] != None:
						search[key] = True
				for key in search:
					if key:
						query.append(key+'='+form[key])
				if len(query) > 1:
					querystring = 'SELECT * FROM transactions WHERE '+query[0]
				else:
					querystring = 'SELECT * FROM * WHERE '
					querystring += query[0]
					for i in range(len(1, query)):
						querystring+=' AND '+query[i]
				history = cur.execute(querystring)
				return render_template('getinfo.html', transactions=transactions, history=history)
			else:
				return render_template('getinfo.html')
		return render_template('getinfo.html')
	return redirect(url_for('login'))
@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] in login_info:
			if request.form['password'] == login_info[request.form['username']]:
				session['logged_in'] = True
				return redirect(url_for('getinfo'))
			else:
				error = 'Invalid Password'
		else:
			error = 'Invalid Username'	
	return render_template('login.html', error=error)
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))
if __name__ == '__main__':
	app.secret_key = app.config['app_secretKey']
	app.run(debug=app.config['app_debug'], host='0.0.0.0', port=app.config['app_port'])