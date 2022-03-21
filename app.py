from tempfile import mkdtemp

import flask
import os
import os.path
from sys import getsizeof
from flask import Flask, redirect, session, Blueprint, url_for, flash, send_from_directory
from flask import request, jsonify
from flask_session import Session
from flask_restx import Resource, Api
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import null

from database.database import init_database
from database.models import *
from helpers import login_required, convert_bytes
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/eliot/Desktop/IMT Atlantique/WebApp/WebApp/static/storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/')
app.register_blueprint(blueprint)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conv = api.namespace('conversation', description='Conversation operations')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension


def get_last_message(messages):
    for message in reversed(messages):
        if message.content:
            return message.content


app.jinja_env.globals.update(
    get_last_message=get_last_message,
    get_file_extension=get_file_extension
)


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
    all_conversations = Conversation.query.all()
    conversations = []
    logged_user = User.query.filter_by(id=session['user_id']).first()
    for conversation in all_conversations:
        if logged_user in conversation.users:
            conversations += [conversation]
    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name

    return flask.render_template("home.html.jinja2", conversations=conversations, names=names)


@app.route('/conversation/<id>', methods=["GET", "POST"])
@login_required
def conversation(id):
    all_conversations = Conversation.query.all()
    conversations = []
    logged_user = User.query.filter_by(id=session['user_id']).first()
    for conversation in all_conversations:
        if logged_user in conversation.users:
            conversations += [conversation]
    current_conversation = Conversation.query.filter_by(id=id).first()
    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name
    if logged_user in current_conversation.users:
        return flask.render_template("conversation.html.jinja2", conversations=conversations,
                                     conversation=current_conversation, names=names)
    else:
        return redirect("/")


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


@app.route("/dashboard")
def dashboard():
    all_conversations = Conversation.query.all()
    conversations = []
    logged_user = User.query.filter_by(id=session['user_id']).first()
    for conversation in all_conversations:
        if logged_user in conversation.users:
            conversations += [conversation]
    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name

    sent_messages = Message.query.filter_by(user_id=session['user_id']).count()
    size_sent_messages = 0
    for sent_message in Message.query.filter_by(user_id=session['user_id']):
        if sent_message not in Message.query.filter_by(filename=null()):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], sent_message.filename)
            size_sent_messages += os.path.getsize(file_path)
        size_sent_messages += getsizeof(sent_message.content)
    total_messages = Message.query.count()
    size_total_messages = 0
    for message in Message.query.all():
        if message not in Message.query.filter_by(filename=null()):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], message.filename)
            size_total_messages += os.path.getsize(file_path)
        size_total_messages += getsizeof(message.content)
    stocked_files = total_messages-Message.query.filter_by(filename=null()).count()
    size_stocked_files = 0
    for file in Message.query.all():
        if file not in Message.query.filter_by(filename=null()):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            size_stocked_files += os.path.getsize(file_path)

    return flask.render_template("dashboard.html.jinja2", conversations=conversations, names=names,
                                 sent_messages=sent_messages, size_sent_messages=convert_bytes(size_sent_messages),
                                 total_messages=total_messages, size_total_messages=convert_bytes(size_total_messages),
                                 stocked_files=stocked_files, size_stocked_files=convert_bytes(size_stocked_files))

@app.route('/conversation/<id>/message', methods=["POST"])
def send_message(id):
    message_content = request.form.get("message")
    file = request.files.get('file')
    conversation = Conversation.query.get(id)
    user = User.query.filter_by(id=session['user_id']).first()
    if message_content:
        message = Message(content=message_content, user=user)
        conversation.messages.append(message)
        db.session.add(message)
        db.session.commit()
        return message.as_dict()
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        message = Message(filename=filename, user=user)
        conversation.messages.append(message)

        db.session.add(message)
        db.session.commit()
        return path


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


@app.route('/search', methods=['GET','POST'])
@login_required
def search():
    # get string to look for in messages
    string_to_search = request.form.get("string")
    logged_user = User.query.filter_by(id=session['user_id']).first()
    # get user conversations and related messages
    all_conversations = Conversation.query.all()
    conversations = []
    messages = []
    for conversation in all_conversations:
        if logged_user in conversation.users:
            conversations += [conversation]
            messages += conversation.messages
    # get messages that contain the string
    searched_messages = []
    for message in messages:
        if string_to_search.lower() in message.content.lower():
            searched_messages += [message]
    names = {}
    for user in User.query.all():
        names[user.id] = User.query.filter_by(id=user.id).first().name
    return flask.render_template("search.html.jinja2", names=names, conversations=conversations,
                                 messages=searched_messages)


@app.route('/conversation/<id>/members', methods=['POST'])
@login_required
def add_member(id):
    member_email = request.form.get("email")
    conversation = Conversation.query.filter_by(id=id).first()
    user_to_add = User.query.filter_by(email=member_email).first()
    if user_to_add is None:
        return jsonify(error="Cet utilisateur n\'existe pas")
    elif conversation.users.filter_by(email=member_email).first():
        return jsonify(error="Cet utilisateur est déjà dans la conversation")
    else:
        conversation.users.append(user_to_add)
        db.session.add(conversation)
        db.session.commit()
        return redirect('/conversation/' + str(conversation.id))


@app.route('/conversation/<id>/leave', methods=['GET'])
@login_required
def leave_conversation(id):
    conversation = Conversation.query.filter_by(id=id).first()
    logged_user = User.query.filter_by(id=session['user_id']).first()
    if logged_user is None:
        return jsonify(error="Cet utilisateur n\'existe pas")
    else:
        conversation.users.remove(logged_user)
        db.session.add(conversation)
        db.session.commit()
        return redirect('/')



@app.route('/uploads/<name>')
@login_required
def download_file(name):
    print(name)
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(debug=True)
