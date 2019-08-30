from flask_restful import Resource, reqparse
from login import models
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity, get_raw_jwt)


parser = reqparse.RequestParser()
parser.add_argument('userId')
parser.add_argument('userName',help='This field cannot be blank',required = True)
parser.add_argument('userPassword',help='This field cannot be blank',required = True)
parser.add_argument('userAddress')
parser.add_argument('userFullName')
parser.add_argument('userRole')
parser.add_argument('userOrg')
parser.add_argument('createdBy')
parser.add_argument('modifiedBy')


class UserRegistration(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()

        if models.UserModel.find_by_username(data['userName']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = models.UserModel(
            userName=data['userName'],
            userPassword=data['userPassword'],
            userAddress=data['userAddress'],
            userFullName=data['userFullName'],
            userRole=data['userRole'],
            userOrg=data['userOrg'],
            createdBy=data('createdBy')
        )
        try:
            new_user.save_to_db()

            return {
                'message': 'User {} was created'.format(data['username']),
            }
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def get(self):
        data = parser.parse_args()

        try:
            return models.UserModel.find_by_userid(data['userId'])
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def delete(self):
        data = parser.parse_args()

        try:
            return models.UserModel.delete_by_userid(data['userId'])
        except:
            return {'message': 'Something went wrong'}, 500

    @jwt_required
    def put(self):
        data = parser.parse_args()

        new_user = models.UserModel(
            userId=data['userId'],
            userName=data['userName'],
            userPassword=data['userPassword'],
            userAddress=data['userAddress'],
            userFullName=data['userFullName'],
            userRole=data['userRole'],
            userOrg=data['userOrg'],
            createdBy=data('modifiedBy')
        )
        try:
            new_user.update_to_db()
            access_token = create_access_token(identity=data['userId'])

            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        current_user = models.UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if bcrypt.checkpw(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            return {'message': 'Logged in as {}'.format(current_user.username), 'access_token': access_token}
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}


class AllUsers(Resource):
    @jwt_required
    def get(self):
        return models.UserModel.return_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }