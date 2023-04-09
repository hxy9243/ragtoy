import logging
import hashlib
import uuid
import datetime

from flask_restful import Resource
from flask import make_response, request

from flaskapp.models import Document, Conversation, Message
from flaskapp.config import db


class DocumentsApi(Resource):
    def get(self):
        try:
            docs = db.session.execute(db.select(Document)).scalars()
        except Exception as exec:
            logging.error(f'Error querying database: {exec}')
            return make_response({'error': str(exec)}, 500)

        results = []
        for doc in docs:
            results.append(doc.data())

        return results

    def _get_hash(self, body):
        return hashlib.md5(body.encode('utf-8')).hexdigest()

    def post(self):
        body = request.form['document']
        doctype = request.form['type']

        existing = db.session.execute(
            db.select(Document).where(
                Document.hash == self._get_hash(body)
            ),
        ).scalars().all()

        if existing:
            return make_response(existing[0].data())


        newdoc = Document(
            docid=str(uuid.uuid4()),
            doctype=doctype,
            hash=self._get_hash(body),
            body=body,
        )
        db.session.add(newdoc)
        db.session.commit()

        return make_response(newdoc.data(), 201)


class DocumentApi(Resource):
    def get(self, docid):
        doc = db.one_or_404(
            db.select(Document).
            where(Document.docid == docid),
            description=f'Error 404: no record of document with id {docid}',
        )
        docdata = doc.data()
        convdata = []
        for conv in doc.conversations:
            convdata.append(conv.data())
        docdata['conversations'] = convdata

        return docdata

    def delete(self, docid):
        doc = db.one_or_404(
            db.select(Document).where(Document.docid == docid),
            description=f'Error 404: no record of document with id {docid}',
        )
        db.session.delete(doc)
        db.session.commit()

        return make_response({}, status=204)


class DocumentConversationsApi(Resource):
    def get(self, docid):
        convs = db.session.execute(
            db.select(Conversation).
            where(Conversation.docid == docid),
            ).scalars()

        results = []
        for conv in convs:
            results.append(conv.data())
        return results


class ConversationsApi(Resource):
    def get(self):
        convs = db.session.execute(db.select(Conversation)).scalars()

        results = []
        for conv in convs:
            results.append(conv.data())

        return results

    def post(self):
        user = request.form['user']
        docid = request.form['docid']
        doc = db.one_or_404(
            db.select(Document).where(Document.docid == docid),
            description=f'Error 404: no record of document with id {docid}',
        )

        convid = str(uuid.uuid4())
        newconv = Conversation(
            convid=convid,
            user=user,
            docid=doc.docid,
        )
        db.session.add(newconv)
        db.session.commit()

        return make_response(newconv.data())


class ConversationApi(Resource):
    def get(self, convid):
        conv = db.one_or_404(
            db.select(Conversation).
            where(Conversation.convid == convid))

        return conv.data()

    def delete(self, convid):
        conv = db.one_or_404(
            db.select(Document).where(Conversation.convid == convid),
            description=f'Error 404: no conversation found with id {convid}',
        )
        db.session.delete(conv)
        db.session.commit()


class MessagesApi(Resource):
    def get(self, convid):
        msgs = db.session.execute(
            db.select(Message).
            where(Message.convid == convid)
        ).scalars()

        results = []
        for m in msgs:
            results.append(m.data())
        return results

    def _add_message(self, convid, msgtype, msgtext):
        with db.session.begin():
            conv = db.one_or_404(
                db.select(Conversation).
                where(Conversation.convid == convid)
            )

            lastmessage = db.session.execute(
                db.select(Message).
                where(Message.convid == convid).
                order_by(Message.index.desc())
            ).scalar()

            index = 1
            if lastmessage:
                index = lastmessage.index + 1

            msg = Message(
                msgid=str(uuid.uuid4()),
                convid=conv.convid,
                index=index,
                msg=msgtext,
                msgtype=msgtype,
                time=datetime.datetime.now(),
            )

            db.session.add(msg)
        return msg

    def post(self, convid):
        msgtype = request.form['message-type']
        msgtext = request.form['message']

        msg = self._add_message(convid, msgtext, msgtype)

        return msg.data()
