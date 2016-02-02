from flask import Flask, request, redirect, url_for, session, render_template, send_from_directory, flash # Web library requirements
import os
import time
from models import db, bcrypt, User, Transaction, TransactionType
from functools import wraps

app = Flask(__name__) # initiates flask webapp
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
bcrypt.init_app(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            print("Logged in")
            return redirect(url_for('login', next=request.url))
        else:
            return f(*args, **kwargs)
    return decorated_function

def admin_required(h):
    @wraps(h)
    def decorated_function(*args, **kwargs):
        if not User.query.filter_by(email=session.get("email")).first().isAdmin:
            abort(405)
        elif session.get("logged_in") is None:
            return redirect(url_for('login', next=request.url))
        return h(*args, **kwargs)
    return decorated_function

@app.route('/')
def root():
    try:
        if len(User.query.all()) == 0:
            return redirect(url_for("setup"))
    except:
        return redirect(url_for("setup"))
    return redirect(url_for('addtrans')) # if / is served, redirects webbrowser to the add transaction page

@app.route('/search')
@login_required
def search():
    return "NYI"

@app.route("/settings")
@login_required
def settings():
    return "NYI"

@app.route('/history', methods=['GET','POST']) # request methods allowed Post and Get
@login_required
def history():
    items = Transaction.query.all().order_by("date")
    return render_template("history.html", entries=items)

@app.route('/addtrans', methods=['POST','GET']) # adds transactions to the Transactions database
@login_required
def addtrans():
    if request.method == "POST":
        serialNumber= request.form["serialNumber"]
        user        = request.form["loginName"]
        models      = request.form["resourceType"]
        transtype   = request.form["transType"]
        note        = request.form["notes"]
        transaction = Transaction(owner=user,
                                user=session.get("email"),
                                serial=serialNumber,
                                model=model,
                                transtype=transtype,
                                notes=note)
        db.session.add(transaction)
        db.session.commit()
        flash("Transaction added")
    else:
        pass
    return render_template("addtrans.html")

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if not session.get('logged_in'):
        if request.method == "POST":
            try:
                user = User.query.filter_by(email=request.form["email"]).first() # get user that is
                assert user.login(request.form["password"])
                session["logged_in"] = True
                session["email"] = user.email
                return redirect(url_for("addtrans"))
            except AssertionError:
                error = "Incorrect Username or Password"
                return render_template('login.html', error=error)
        else:
            return render_template('login.html', error=error)
    else:
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

@app.route("/setup", methods=["POST", "GET"])
def setup():
    if len(User.query.all()) != 0:
        abort(404)
    elif request.method == "POST":
        if request.form["password"] == request.form["passwordAgain"]:
            user = User(email=request.form["email"], password=request.form["password"], isAdmin=True)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            flash("Passwords do not match")
            return render_template("setup.html")
    else:
        return render_template("setup.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.secret_key = os.urandom(16)
    app.run(debug=True)
