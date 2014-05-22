from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, Response
import MySQLdb
# db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                      user="resource_tracker", # your username
#                       passwd="password", # your password
#                       db="data")
app = Flask(__name__)
app.config.from_object('app.config')
login_info = {'temptemp':'temptemppassword', 'admin':'password'}
@app.route('/')
def root():
	return redirect(url_for('getinfo'))
@app.route('/getinfo', methods=['GET','POST'])
def getinfo():
	if session.get('logged_in'):
		if request.method == 'post':
			info = {}
			return render_template('getinfo.html', firstnameoption=firstnames, lastnameoption=lastnames, )
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