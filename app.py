from flask import Flask, request, redirect, url_for, send_from_directory, session, render_template, Response
import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="resource_tracker", # your username
                      passwd="password", # your password
                      db="resource_tracker") # name of the data base
cur = db.cursor()

app = Flask(__name__)
app.config.from_object('app.config')

login_info = {'temptemp': 'temptemppassword', 'admin': 'adminPassword'}
def get_history(id):
	cur.excecute('SELECT * data WHERE id = %s', % id)
	if len(cur.fetchall()) > 0:
		toreturn = []
		ids = []
		date = []
		type = []
		data = []
		for row in cur.fetchall():
			ids.append(row[0])
			date.append(row[1])
			type.append(row[2])
			data.append(row[3])
		toreturn.append(ids)
		toreturn.append(data)
		toreturn.append(type)
		toreturn.append(data)
		return toreturn
	else:
		return False

@app.route('/', methods=['GET', 'POST'])
def root():
	if session['logged_in']:
		if request.method == 'post':
			error = []
			if 'resource_id' in request.form['resource_id']:
				
				#check if form is complete, if so create new entry in database, other wise error out
			return #sucess + errors
	return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
	if not session['ldogged_in']:
		if request.method == 'post':
			try:
				if  request.form['password'] == login_info[request.form['username']]:
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
		firstnames 
		if request.method == 'post':
			#get the history of the computer
			info = {}
			return render_template('getinfo.html', firstnameoption=firstnames, lastnameoption=lastnames, )
		return render_template('getinfo.html')
	return redirect(url_for('login'))


