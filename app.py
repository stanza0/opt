from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////C/Users/Stanza1/untitled/todo.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('index.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('index'))

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'username' and auth.password == 'password':
            return f(*args, **kwargs)

        return make_response('Could not verify your login', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

    @app.route('/')
    def index():
        if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password'
            return '<h1>You are logged in</h1>'

        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

    def connect():
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        c = conn.cursor()
        c.execute("CREATE TABLE users (username TEXT, password TEXT, rank TEXT)")
        c.execute("INSERT INTO users VALUES ('admin', 'e1568c571e684e0fb1724da85d215dc0', 'admin')")
        c.execute("INSERT INTO users VALUES ('bob', '2b903105b59299c12d6c1e2ac8016941', 'user')")
        c.execute("INSERT INTO users VALUES ('alice', 'd8578edf8458ce06fbc5bb76a58c5ca4', 'moderator')")

        c.execute("CREATE TABLE SSN(user_id INTEGER, number TEXT)")
        c.execute("INSERT INTO SSN VALUES (1, '480-62-10043')")
        c.execute("INSERT INTO SSN VALUES (2, '690-10-6233')")
        c.execute("INSERT INTO SSN VALUES (3, '401-09-1516')")

        conn.commit()
        return conn

    CONNECTION = connect()

    @app.route("/login")
    def login():
        username = request.args.get('username', '')
        password = request.args.get('password', '')
        md5 = hashlib.new('md5', password.encode('utf-8'))
        password = md5.hexdigest()
        c = CONNECTION.cursor()
        c.execute("SELECT * FROM users WHERE username = ? and password = ?", (username, password))
        data = c.fetchone()
        if data is None:
            return 'Incorrect username and password.'
        else:
            return 'Welcome %s! Your rank is %s.' % (username, data[2])

    @app.route("/users")
    def list_users():
        rank = request.args.get('rank', '')
        if rank == 'admin':
            return "Can't list admins!"
        c = CONNECTION.cursor()
        c.execute("SELECT username, rank FROM users WHERE rank = '{0}'".format(rank))
        data = c.fetchall()
        return str(data)


if __name__ == '__main__':
    app.run(debug=True)