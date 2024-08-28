import logging
import hashlib
import uuid
import datetime

from flask_restx import Resource
from flask import make_response, request

from .models import Document, Conversation, Message
from .vector import EmbeddingInfo
from .config import api, db, llm, vectorindices


@api.route("/documents")
class DocumentsApi(Resource):
    @api.marshal_with(Document.model(), as_list=True)
    def get(self):
        try:
            docs = db.session.execute(db.select(Document)).scalars()
        except Exception as exec:
            logging.error(f"Error querying database: {exec}")
            return make_response({"error": str(exec)}, 500)

        results = []
        for doc in docs:
            results.append(doc.data())

        return results

    def _get_hash(self, body):
        return hashlib.md5(body.encode("utf-8")).hexdigest()

    def _get_existing(self, body):
        existing = (
            db.session.execute(
                db.select(Document).where(Document.hash == self._get_hash(body)),
            )
            .scalars()
            .all()
        )

        return existing

    def _create_embedding(self, docid, body):
        vectoridx = vectorindices.create(docid)

        chunks = llm.chunkify(body)
        ntokens = 0
        for i, chunk in enumerate(chunks):
            body, ntoken = chunk

            logging.info(
                f"creating #{i+1}/{len(chunks)} for doc {docid} "
                + f"{ntoken} tokens..."
            )
            embedding = llm.create_embedding(body)
            ntokens += ntoken

            vectoridx.put(
                EmbeddingInfo(
                    key=docid + ":" + str(i),
                    text=body,
                    tag=docid,
                    ntokens=ntoken,
                    embedding=embedding,
                )
            )

        return ntokens

    @api.marshal_with(Document.model(), as_list=False)
    def post(self):
        req = request.get_json()
        body: str = req["document"]
        name: str = req["name"]
        doctype: str = req["type"]

        # check if the text is already uploaded, based on hash
        existing = self._get_existing(body)
        if len(existing) != 0:
            return existing[0].data()

        docid = str(uuid.uuid4())

        # create embedding for the document and saves in the vector db
        logging.info(f"creating embedding for document {docid}: {body[:32]}..")
        ntokens = self._create_embedding(docid, body)

        newdoc = Document(
            docid=docid,
            name=name,
            doctype=doctype,
            hash=self._get_hash(body),
            body=body,
            ntokens=ntokens,
        )
        db.session.add(newdoc)
        db.session.commit()

        return newdoc.data()


class DocumentApi(Resource):
    def get(self, docid):
        doc = db.one_or_404(
            db.select(Document).where(Document.docid == docid),
            description=f"Error 404: no record of document with id {docid}",
        )
        docdata = doc.data()
        convdata = []
        for conv in doc.conversations:
            convdata.append(conv.data())
        docdata["conversations"] = convdata

        return docdata

    def delete(self, docid):
        # delete corresponding embedding as well

        doc = db.one_or_404(
            db.select(Document).where(Document.docid == docid),
            description=f"Error 404: no record of document with id {docid}",
        )
        db.session.delete(doc)
        db.session.commit()

        return make_response({}, status=204)


class DocumentConversationsApi(Resource):
    def get(self, docid):
        convs = db.session.execute(
            db.select(Conversation).where(Conversation.docid == docid),
        ).scalars()

        results = []
        for conv in convs:
            results.append(conv.data())
        return results


class ConversationsApi(Resource):
    def get(self):
        convs = db.session.execute(db.select(Conversation)).scalars()

        return [conv.data() for conv in convs]

    def post(self):
        convreq = request.get_json()
        user = convreq["user"]
        docid = convreq["docid"]

        doc = db.one_or_404(
            db.select(Document).where(Document.docid == docid),
            description=f"Error 404: no record of document with id {docid}",
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
            db.select(Conversation).where(Conversation.convid == convid)
        )

        return conv.data()

    def delete(self, convid):
        conv = db.one_or_404(
            db.select(Document).where(Conversation.convid == convid),
            description=f"Error 404: no conversation found with id {convid}",
        )
        db.session.delete(conv)
        db.session.commit()

        return conv.data()


class MessagesApi(Resource):
    def get(self, convid):
        msgs = db.session.execute(
            db.select(Message).where(Message.convid == convid)
        ).scalars()

        results = []
        for m in msgs:
            results.append(m.data())
        return results

    def _add_message(self, convid, msgtype, msgtext, context=""):
        with db.session.begin():
            conv = db.one_or_404(
                db.select(Conversation).where(Conversation.convid == convid)
            )
            lastmessage = db.session.execute(
                db.select(Message)
                .where(Message.convid == convid)
                .order_by(Message.index.desc())
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
                context=context,
                time=datetime.datetime.now(),
            )

            db.session.add(msg)
            db.session.commit()
        return msg

    def _create_prompt(self, msg, vector_results):
        context = "\n###\n".join([v["text"] for v in vector_results])

        return (
            "Answer the question based on the context, and if it "
            + "cannot be answered based on the context, say 'I don't know'\n"
            + f"Context:\n{context}\n"
            + f"Question: {msg}\n"
            + "Answer:"
        )

    def post(self, convid):
        msgreq = request.get_json()
        msgtext = msgreq["text"]

        conv = db.one_or_404(
            db.select(Conversation).where(Conversation.convid == convid)
        )
        docid = conv.doc.docid
        db.session.commit()

        logging.info(f"Adding new message to conversaiton {convid}")
        msg = self._add_message(convid, msgtype="user", msgtext=msgtext)

        # create emebedding for the message
        embedding = llm.create_embedding(msgtext)

        # query vector db to create prompt context
        vectoridx = vectorindices.get(docid)
        logging.debug(f"embedding: {embedding}")
        results = vectoridx.search(embedding)

        logging.debug(
            "vector search results, " + f"{len(results)} total results: {results}"
        )

        prompt = self._create_prompt(msgtext, results)
        logging.debug(f"Creating prompt results: {prompt}")

        # query QA engine for answer
        logging.info("Querying LLM engine to create completion")
        answertext = llm.create_completion(prompt)

        logging.info("Adding new answer to conversaiton")
        answer = self._add_message(
            convid, msgtype="system", msgtext=answertext, context=prompt
        )

        return make_response(
            [
                msg.data(),
                answer.data(),
            ],
        )
