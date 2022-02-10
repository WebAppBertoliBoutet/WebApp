from flask import Flask

from database.database import init_database
from database.models import *
import flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.test_request_context():
    init_database()


@app.route('/')
def hello_world():

    conversation = Conversation.query.first()

    result = ''
    for message in conversation.messages:
        result += message.user.name + '\n'

    return flask.render_template("home.html.jinja2", conversation=conversation)


@app.route('/seed')
def seed():
    user1 = User(name='Eliot', email='bouteteliot@gmail.com')
    user2 = User(name='Gaby', email='test1234@gmail.com')
    user3 = User(name='Maxime', email='test5678@gmail.com')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    conversation1 = Conversation(isGroup=True, name="DCL")
    db.session.add(conversation1)

    conversation1.users.append(user1)
    conversation1.users.append(user2)

    db.session.add(conversation1)

    message1 = Message(content='Coucou c\'est le premier message', user=user1)
    message2 = Message(content='Coucou c\'est le deuxième message', user=user2)

    db.session.add(message1)
    db.session.add(message2)

    conversation1.messages.append(message1)
    conversation1.messages.append(message2)

    db.session.add(conversation1)
    db.session.commit()

    return 'well seeded'


if __name__ == '__main__':
    app.run()
