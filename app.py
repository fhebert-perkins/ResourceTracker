from flask import Flask, request, redirect, url_for, session, render_template, send_from_directory, flash # Web library requirements
import os
import time
from models import db, bcrypt, User, Transaction, TransactionType

app = Flask(__name__) # initiates flask webapp
db.init(app)
bcrypt.init(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("logged_in") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not User.query.filter_by(email=session.get("email")).first().admin:
            abort(405)
        elif session.get("logged_in") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def root():
    return redirect(url_for('addtrans')) # if / is served, redirects webbrowser to the add transaction page

@app.route('/search')
@login_required
def search():
    return "NYI"

@app.route('/history', methods=['GET','POST']) # request methods allowed Post and Get
@login_required
def history():
    return "NYI"

@app.route('/addtrans', methods=['POST','GET']) # adds transactions to the Transactions database
@login_required
def addtrans():
    return "NYI"

@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if not session.get('logged_in'):
        if request.method == "POST":
            try:
                user = User.query.filter_by(email=request.form["email"]).first() # get user that is
                yield user.login(request.form["password"])
                session["logged_in"]= True
                session["email"] = user.email
                return redirect(url_for("addtrans"))
            except:
                flash("Incorrect Username or Password")
                return render_template('login.html')
        else:
            return render_template('login.html')
    return redirect(url_for('addtrans'))

@app.route('/logout') # This can stay the same
@login_required
def logout():
    if session.get('logged_in'):
        session.pop('logged_in', None)
        return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/newuser', methods=['GET', 'POST'])
@admin_required
def newuser():
    return "NYI"

@app.route("/users")
@login_required
def listusers():
    return "NYI"

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    return "NYI"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.secret_key = os.urandom(16).encode("base_64")
    app.run(debug=True)
