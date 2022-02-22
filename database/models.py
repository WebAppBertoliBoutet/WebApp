from database.database import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    email = db.Column(db.Text)
    message = db.relationship("Message", backref='user')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


conversations_junction_table = db.Table('user_conversations',
                                        db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id')),
                                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                        )

messages_junction_table = db.Table('message_conversations',
                                   db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id')),
                                   db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
                                   )


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    isGroup = db.Column(db.Boolean)
    users = db.relationship('User', backref='conversations', secondary=conversations_junction_table)
    messages = db.relationship('Message', backref='conversations', secondary=messages_junction_table)
