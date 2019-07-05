import os
from os.path import join, dirname, realpath

import sentry_sdk
from dotenv import load_dotenv, find_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_uploads import patch_request_class
from sentry_sdk.integrations.flask import FlaskIntegration

from config import SWAGGER_CONFIG, MAX_CONTENT_LENGTH, UPLOAD_FOLDER, JWT_ACCESS_TOKEN_EXPIRES
from model import RevokedToken
from utils.exceptions import register_error_handlers
from utils.model_encoder import AlchemyEncoder
from utils.model_session import Session
from utils.seeder import init_admin

UPLOADS_PATH = join(dirname(realpath(__file__)), UPLOAD_FOLDER + '/')
load_dotenv(find_dotenv(), override=True)


def create_app():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FlaskIntegration()]
    )

    app = Flask(__name__)

    CORS(app, expose_headers=["X-Total-Count"])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['ENV'] = os.environ.get('ENV', 'dev')

    app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH * 1024 * 1024

    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'test')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    jwt = JWTManager(app)

    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    patch_request_class(app)

    from model.db import db
    db.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_jti_blacklisted(jti)

    app.json_encoder = AlchemyEncoder
    register_error_handlers(app)

    Swagger(app, template=SWAGGER_CONFIG)
    app.sess = Session()
    with app.app_context():
        from blueprint.auth import auth as auth_route
        from blueprint.user import user_route

        app.register_blueprint(auth_route)
        app.register_blueprint(user_route)

        init_admin()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()

    return app


if __name__ == '__main__':
    lapp = create_app()
    lapp.run(host='0.0.0.0', debug=os.getenv('FLASK_DEBUG', False))
