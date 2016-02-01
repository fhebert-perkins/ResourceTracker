from flask import Flask, request, redirect, url_for, session, render_template, send_from_directory, flash # Web library requirements
import os
import time

app = Flask(__name__) # initiates flask webapp

@app.route('/')
def root():
    return redirect(url_for('addtrans')) # if / is served, redirects webbrowser to the add transaction page
@app.route('/search')
def search():
    pass
@app.route('/history', methods=['GET','POST']) # request methods allowed Post and Get
def history():
    if session.get('logged_in'): # checks if session is logged in if so passes to authorized only values
        if request.method == 'POST': # if the request method is post
            return render_template('history.html')
       return redirect(url_for('search'))
return redirect(url_for('login'))

@app.route('/addtrans', methods=['POST','GET']) # adds transactions to the Transactions database
def addtrans():
    return render_template('addtrans.html', transtypes=types, resourcetype=resources)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if not session.get('logged_in'):
        if request.method == "POST":

            return redirect(url_for("addtrans"))
        else:
            return render_template('login.html')
    return redirect(url_for('addtrans'))
@app.route('/logout') # This can stay the same
def logout():
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
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('logged_in') == True:
        return render_template('adminpanel.html', adminURL=app.config['adminpanelURI'])
    return redirect(url_for('login'))
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.secret_key = app.config['app_secretKey']
    app.run(debug=app.config['app_debug'], host='0.0.0.0', port=app.config['app_port'])
