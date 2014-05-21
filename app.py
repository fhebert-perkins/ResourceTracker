from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, Response
import MySQLdb

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
))
login_info = {'temptemp':'temptemppassword', 'admin':'password'}
@app.route('/')
def root():
	return redirect(url_for('getinfo'))
@app.route('/login', methods=['GET', 'POST'])
def login():
	if not session.get('logged_in'):
		if request.method == 'post':
			#if request.form['password'] == login_info[request.form['username']]:
			if request.form['password'] == 'password' and request.form['username'] == 'admin':
				session['logged_in'] = True
				return redirect(url_for('getinfo'))
			return render_template('login.html', error=True)
		return render_template('login.html')
	return redirect(url_for('root'))
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
	app.run(debug=True)