from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'hash-password-secret'
jwt = JWTManager(app)

import resources,__init__

api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.UserRegistration, '/user')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.SecretResource, '/secret')

db = __init__.db;