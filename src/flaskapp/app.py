from flask import Blueprint
from flask_cors import CORS

from flaskapp.route import create_api_route
from flaskapp.config import app, db

apibp = Blueprint('api', __name__)
apibp = create_api_route(apibp)
app.register_blueprint(apibp, url_prefix='/api')

CORS(app)


def initapp():
    with app.app_context():
        db.create_all()


def runapp(*args, **kwargs):
    app.run(*args, **kwargs)
