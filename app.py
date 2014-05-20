from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, Response
import dbmysql

app = Flask(__name__)
app.config.from_object('app.config')
login_info = {'temptemp': 'temptemppassword', 'admin': 'adminPassword'}
@app.route('/', methods=['GET', 'POST'])
def root():
	if session['logged_in']:
		if request.method == 'post':
			error = []
			if request.form['resource_id'] in resource_ids: # form field called resource id
				#get basic data about resource id, concatinate new info inject into db
			else:
				error.append('No such id, creating new id')
				#check if form is complete, if so create new entry in database, other wise error out
			return #sucess + errors
	return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
	if not session['logged_in']:
		if request.method == 'post':
			try:
				if  request.form['password']== login_info[request.form['username']]:
					session['logged_in'] = True
					return redirect(url_for('root'))
				return render_template('login.html', error='Incorect login info')
			except:
				return render_template('login.html', error='Incorect login info')
		return render_template('login.html')
	return redirect(url_for('root'))
@app.route('/getinfo', methods=['GET','POST'])
def getinfo:
	if session['logged_in']:
		if request.method == 'post':
			#get the history of the computer
			info = {}
			return render_template('getinfo.html', info=info)
		return render_template('getinfo.html')
	return redirect(url_for('login'))

