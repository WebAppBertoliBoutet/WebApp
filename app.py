from flask import Flask, redirect, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from database.database import init_database
from database.models import *
from flask import request
import flask

from helpers import login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


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

## INIT TEST DATABASE
    user1 = User(name='Eliot', email='bouteteliot@gmail.com', hash='a123')
    user2 = User(name='Gaby', email='test1234@gmail.com', hash='b456')
    user3 = User(name='Maxime oui', email='test5678@gmail.com', hash='hashsecret')
    user4 = User(name='Louis', email='test2938@gmail.com', hash='tressecret')
    user5 = User(name='Robin', email='test2288@gmail.com', hash='ahah')
    user6 = User(name='Baptiste', email='test0999@gmail.com', hash='eheh')
    user7 = User(name='André', email='test0974@gmail.com', hash='ohoh')
    user8 = User(name='Mario', email='test3344@gmail.com', hash='uwu')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)

    conversation1 = Conversation(isGroup=True, name="DCL")
    db.session.add(conversation1)

    conversation1.users.append(user1)
    conversation1.users.append(user2)
    conversation1.users.append(user3)
    conversation1.users.append(user4)
    conversation1.users.append(user5)

    db.session.add(conversation1)

    conversation2 = Conversation(isGroup=True, name="Yakuzart")

    conversation1.users.append(user3)
    conversation1.users.append(user4)
    conversation1.users.append(user5)

    db.session.add(conversation2)

    message1 = Message(content='Coucou c\'est le premier message', user=user1)
    message2 = Message(content='Coucou c\'est le deuxième message', user=user2)

    db.session.add(message1)
    db.session.add(message2)

    conversation1.messages.append(message1)
    conversation1.messages.append(message2)

    db.session.add(conversation1)
    db.session.commit()

    message3 = Message(content='Coucou c\'est le premier message des Yaku', user=user5)
    message4 = Message(content='Coucou c\'est le deuxième message des Yaku', user=user3)

    db.session.add(message3)
    db.session.add(message4)

    conversation2.messages.append(message3)
    conversation2.messages.append(message4)

    db.session.add(conversation2)
    db.session.commit()


@app.route('/', methods=["GET", "POST"])
@login_required
def hello_world():

    conversations = Conversation.query.all()

    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name

    return flask.render_template("home.html.jinja2", conversations=conversations, names=names)


@app.route('/conversation/<id>', methods=["GET", "POST"])
@login_required
def conversation(id):
    id = 1
    conv = Conversation.query.filter_by(id=id).first()
    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name

    return flask.render_template("conversation.html.jinja2", conversation=conversation, names=names)


@app.route('/login', methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure email exists and password is correct
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first() == None:
            return redirect("/login")
        if check_password_hash(User.query.filter_by(email=email).first().hash, password):
            # Remember which user has logged in and redirects to home page
            session["user_id"] = User.query.filter_by(email=email).first().id
            return redirect("/")
        # Redirect user to login
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
        if User.query.filter_by(email=email).first() != None:
            return redirect("/register")
        else:
            hash = generate_password_hash(password)
            user = User(name=name, email=email, hash=hash)
            db.session.add(user)
            db.session.commit()
            # Remember which user has logged in
            session["user_id"] = User.query.filter_by(email=email).first().id
            return redirect("/")
        # Redirect user to home page
    else:
        return flask.render_template("register.html.jinja2")

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/login")

@app.route('/conversation/<id>/message', methods=["POST"])
def send_message(id):

        message_content = request.form.get("message")
        conversation = Conversation.query.get(id)
        first_user = conversation.users[1]
        message = Message(content=message_content, user=first_user)
        db.session.add(message)
        db.session.commit()
        return message.as_dict()


if __name__ == '__main__':
    app.run()
