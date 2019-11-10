from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from models.Users import UserModel

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', help = 'This field cannot be blank', required = True)
user_parser.add_argument('password', help = 'This field cannot be blank', required = True)
user_parser.add_argument('email', help= 'This field cannot be blank')

#User API
class UserRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists!'.format(data['username'])}

        new_user = UserModel(data['username'], UserModel.generate_hash(data['password']), data['email'])
        try:
            new_user.save_to_db()
            return {'message': 'User {} was created!'.format(data['username'])}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if not user:
            return {'message': "User {} doesn't exist".format(data['username'])}, 500

        if UserModel.verify_hash(data['password'], user.password):            
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token       
            }
        else:
            return {'message': "Wrong password!"}, 500
      
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.save_to_db()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.save_to_db()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class AllUsers(Resource):
    def get(self):
        return {'users': UserModel.return_all()}, 200

#Token API
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}