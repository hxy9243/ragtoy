import logging
import hashlib

from flask_restful import Resource
from flask import Response, request

from flaskapp.models import Document
from flaskapp.config import db


class DocumentsApi(Resource):
    def get(self):
        try:
            docs = Document.query.all()
        except Exception as exec:
            logging.error(f'Error querying database: {exec}')
            return Response({'error': str(exec)})

        results = []
        for doc in docs:
            results.append(doc.data())

        return results

    def _get_hash(self, body):
        return hashlib.md5(body.encode('utf-8')).hexdigest()

    def post(self):
        body = request.form['document']
        doctype = request.form['type']

        existing = Document.query.filter_by(
            hash=self._get_hash(body),
        ).first()

        if existing:
            return Response(existing.data())

        newdoc = Document(
            doctype=doctype,
            hash=self._get_hash(body),
            body=body,
        )
        db.session.add(newdoc)
        db.session.commit()

        return Response(newdoc.data())


class DocumentApi(Resource):
    def get(self, docid):
        try:
            doc = Document.query.one(docid)
        except Exception as exec:
            logging.error(f'Error querying database: {exec}')
            return Response({'error': str(exec)})

        return doc


