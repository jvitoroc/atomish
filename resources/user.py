from flask_restful import Resource
from flask_restful import reqparse
from schemas.user import UserRegistrationSchema, UserLoginSchema
from sqlalchemy.exc import IntegrityError
from models import User, Highscore
from common.db import db_session
from config import JWT_SECRET
import jwt

userParser = reqparse.RequestParser()

userParser.add_argument('username')
userParser.add_argument('password')

# responses = {
#     'USER_VALIDATION_ERROR': ({'status': 400}, 400),
#     'USER_ALREADY_EXISTS': ({'status': 403, 'errors': {'username':['Username already exists.']}}, 403),
#     'UNKNOWN_INTERNAL_ERROR': ({'status': 500, 'message': 'An unknown error occurred, try again later.'}, 500),
#     'USER_CREATED': ({'status': 201, 'message': 'User was created.'}, 201),
#     'USER_AUTHENTICATED': ({'status': 200, 'message': 'User authenticated.', 200),
# }

class UserRegistrationResource(Resource):
    def post(self):
        args = userParser.parse_args()
        print(args)
        errors = UserRegistrationSchema().validate(args)
        if any(errors):
            error_string = ""
            for i in errors:
                error_string += ";".join(errors[i]) + ";"
            return {'code': 'VALIDATION_ERROR', "error": True, 'errors': error_string[0:-1]}, 400
        user = User(username=args.username, hash=args.password)
        highscore = Highscore(user=user)
        try:
            db_session.add(user)
            db_session.add(highscore)
            db_session.commit()
        except IntegrityError as err:
            return {'code': 'BAD_REQUEST', "error": True,'errors': "Username already exists."}, 403
        except Exception:
            return {'code': 'INTERNAL_ERROR', "error": True, 'errors': 'An unknown error occurred, try again later.'}, 500
        return {'code': 'SUCCESS', "error": False, 'message': 'User was created.'}, 201
        pass

class UserLoginResource(Resource):
    def post(self):
        args = userParser.parse_args()
        print(args)
        errors = UserLoginSchema().validate(args)
        if any(errors):
            error_string = ""
            for i in errors:
                error_string += ";".join(errors[i]) + ";"
            return {'code': 'VALIDATION_ERROR', "error": True, 'errors': error_string[0:-1]}, 400
        try:
            user = db_session.query(User).filter_by(username=args.username).first()
        except Exception:
            return {'code': 'INTERNAL_ERROR', "error": True, 'errors': 'An unknown error occurred, try again later.'}, 500
        if(user is None or user.hash != args.password):
            return {'code': 'BAD_REQUEST', "error": True, 'errors': 'Username or password is incorrect.'}, 400
        elif(user is not None and user.hash == args.password):
            jwt_encoded = jwt.encode({'user_id': user.id}, JWT_SECRET, algorithm='HS256')
            return {'code': 'SUCCESS', "error": False, 'message': 'User authenticated.', 'jwt': jwt_encoded.decode('utf-8')}, 200
        pass