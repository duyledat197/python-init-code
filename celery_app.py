import os
import sys
from importlib import reload

from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from services.celery_app import make_celery
from utils.model_encoder import AlchemyEncoder

load_dotenv(find_dotenv(), override=True)

reload(sys)


def create_app():
    app_init = Flask(__name__)
    CORS(app_init)
    app_init.secret_key = os.environ.get('SECRET_KEY')
    app_init.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app_init.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app_init.config['ENV'] = os.environ.get('ENV', 'dev')
    app_init.json_encoder = AlchemyEncoder
    celery_instance = make_celery(app_init)

    from utils.model_session import Session
    app_init.sess = Session()

    @app_init.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()

    return app_init, celery_instance


app, celery = create_app()


@app.errorhandler(404)
def not_found(_e):
    rv = dict()
    rv['code'] = 404
    rv['msg'] = 'Please try another endpoint'
    return jsonify(rv), 404
