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

def clean():
    db.drop_all()
    db.create_all()
    return "Cleaned!"

@app.route('/')
def hello_world():
    clean()
    user1 = User(name='Eliot', email='bouteteliot@gmail.com')
    user2 = User(name='Gaby', email='test1234@gmail.com')
    user3 = User(name='Maxime oui', email='test5678@gmail.com')
    user4 = User(name='Louis', email='test2938@gmail.com')
    user5 = User(name='Robin', email='test2288@gmail.com')
    user6 = User(name='Baptiste', email='test0999@gmail.com')
    user7 = User(name='André', email='test0974@gmail.com')
    user8 = User(name='Mario', email='test3344@gmail.com')
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

    conversations = Conversation.query.all()

    return flask.render_template("home.html.jinja2", conversations=conversations)


@app.route('/seed')
def seed():

    return 'well seeded'


if __name__ == '__main__':
    app.run()
