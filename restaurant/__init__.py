import os
import optparse
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException

from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from restaurant.config import Config
from restaurant.connection import MysqlConnection
from restaurant.config import Config

api = Api()
mssqlcur = MysqlConnection()

bcrypt = Bcrypt()
jwt = JWTManager()
mail=Mail()
from restaurant.restaurant import *
from restaurant.user import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(Config)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'preethireethu14@gmail.com'
    app.config['MAIL_PASSWORD'] = ''
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail=Mail(app)
    mssqlcur.init_app(app)
    mail.init_app(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass





    api.add_resource(Users, '/user', endpoint='user')
    api.add_resource(UserLogin, '/login', endpoint='login')
    #
    api.add_resource(Restaurant, '/restaurant', endpoint="restaurant")
    api.add_resource(Tables, '/tables', endpoint="tables")
    api.add_resource(Menu, '/menu', endpoint="menu")
    api.add_resource(Booking, '/booking', endpoint="booking")

    #
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'authorization,content-type,x-auth-token')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,get,post,delete,put')
        return response



    api.init_app(app)
    jwt.init_app(app)

    return app


def hashPassword(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')
