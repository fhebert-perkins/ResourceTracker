from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, Response
import MySQLdb

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
	USERNAME='admin',
	PASSWORD='default'
))
login_info = {'temptemp':'temptemppassword', 'admin':'password'}
@app.route('/')
def root():
	return redirect(url_for('getinfo'))
@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid Username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Password'
		else:
			session['logged_in'] = True
			return redirect(url_for('getinfo'))
	return render_template('login.html', error=error)
@app.route('/getinfo', methods=['GET','POST'])
def getinfo():
	if session.get('logged_in'):
		if request.method == 'post':
			info = {}
			return render_template('getinfo.html', firstnameoption=firstnames, lastnameoption=lastnames, )
		return render_template('getinfo.html')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.secret_key = 'as;ldfjkas;lfj2i1212'
	app.run(debug=True, host='0.0.0.0')