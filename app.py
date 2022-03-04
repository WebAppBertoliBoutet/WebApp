from tempfile import mkdtemp

import flask
from flask import Flask, redirect, session, Blueprint, url_for, flash, get_flashed_messages
from flask import request
from flask_session import Session
from flask_restx import Resource, Api
from werkzeug.security import check_password_hash, generate_password_hash

from database.database import init_database
from database.models import *
from helpers import login_required

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/')
app.register_blueprint(blueprint)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

conv = api.namespace('conversation', description='Conversation operations')


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.test_request_context():
    init_database()


def clean():
    db.drop_all()
    db.create_all()
    return "Cleaned!"


@app.route('/', methods=["GET", "POST"])
@login_required
def home():
    conversations = Conversation.query.all()
    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name

    return flask.render_template("home.html.jinja2", conversations=conversations, names=names)


@app.route('/conversation/<id>', methods=["GET", "POST"])
@login_required
def conversation(id):
    conversations = Conversation.query.all()
    current_conversation = Conversation.query.filter_by(id=id).first()
    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name

    return flask.render_template("conversation.html.jinja2", conversations=conversations,
                                 conversation=current_conversation, names=names)


@app.route('/login', methods=["GET", "POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure email exists and password is correct
        email = request.form.get("email")
        password = request.form.get("password")

        maybe_user = User.query.filter_by(email=email).first()
        if maybe_user is None:
            flash('An error occurred. Please try again', 'error')
            return redirect("/login")
        if check_password_hash(User.query.filter_by(email=email).first().hash, password):
            # Remember which user has logged in and redirects to home page
            session["user_id"] = maybe_user.id
            return redirect("/")
        # Redirect user to login
        flash('Something wrong happened. Please try again', 'error')
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return flask.render_template("login.html.jinja2")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        # Ensure email exists and password is correct
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        maybe_user = User.query.filter_by(email=email).first()

        if maybe_user is not None:
            flash('Please provide a valid email.', 'error')
            return redirect("/register")
        else:
            hashed_password = generate_password_hash(password)
            user = User(name=name, email=email, hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            # Remember which user has logged in
            session["user_id"] = user.id
            return redirect("/")
        # Redirect user to home page
    else:
        return flask.render_template("register.html.jinja2")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    flash('Log out successful', 'validation')
    return redirect("/login")


@app.route('/conversation/<id>/message', methods=["POST"])
def send_message(id):
    message_content = request.form.get("message")
    conversation = Conversation.query.get(id)
    user = User.query.filter_by(id=session['user_id']).first()
    message = Message(content=message_content, user=user)
    conversation.messages.append(message)
    db.session.add(message)
    db.session.commit()
    return message.as_dict()


@app.route('/conversation', methods=['POST'])
@login_required
def create_conv():
    data = request.form
    conv = Conversation(name=data['name'])
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    conv.users.append(user)
    db.session.add(conv)
    db.session.commit()
    return redirect('/conversation/' + str(conv.id))


if __name__ == '__main__':
    app.run(debug=True)
