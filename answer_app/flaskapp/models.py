import uuid

from flaskapp.config import db


class Document(db.Model):
    __tablename__ = 'documents'
    docid = db.Column('id', db.String(16),
                      default=str(uuid.uuid4()), primary_key=True)
    doctype = db.Column('type', db.String(16), default='text')
    hash = db.Column('hash', db.String(64))
    body = db.Column('body', db.Text)
    vectorid = db.Column('vector', db.String(64))

    def __repr__(self):
        return f'<Document {self.docid}>'

    def data(self):
        return {
            'id': self.docid,
            'body': self.body,
            'type': self.doctype,
        }


class Conversation(db.Model):
    __tablename__ = 'conversations'
    convid = db.Column('id', db.String(16), primary_key=True)
    docid = db.Column('docid', db.String(16), nullable=False)
    user = db.Column('user', db.String(16))

    def __repr__(self):
        return f'<Conversation {self.convid}>'


class Message(db.Model):
    __tablename__ = 'messages'
    msgid = db.Column('id', db.String(16), primary_key=True)
    convid = db.Column('convid', db.ForeignKey('conversations.id'),
                       nullable=False)
    msg = db.Column('message', db.Text)
    msgtype = db.Column('type', db.String(32))
    context = db.Column('context', db.Text)
    ntokens = db.Column('ntokens', db.Integer)
    time = db.Column('time', db.DateTime)

    def __repr__(self):
        return f'<Message {self.convid}>'
