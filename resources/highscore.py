from flask_restful import Resource
from models import Highscore, User
from schemas.highscore import HighscoreSchema
from common.db import db_session
import jwt
from flask_restful import reqparse
from config import JWT_SECRET

highscoreSchema = HighscoreSchema(many=True)

highscorePostParser = reqparse.RequestParser()
highscorePostParser.add_argument('score', 'form', type=int)
highscorePostParser.add_argument('Authorization', location='headers')

highscoreGetParser = highscorePostParser.copy()
highscoreGetParser.remove_argument('score')

rankingParser = reqparse.RequestParser()
rankingParser.add_argument('page', location='args', type=int)
rankingParser.add_argument('per_page', location='args', type=int)


class HighscoreResource(Resource):
    def patch(self):
        args = highscorePostParser.parse_args()
        score = args.score
        jwt_encoded = args['Authorization'][7:]
        jwt_payload = jwt.decode(jwt_encoded, JWT_SECRET, algorithms=['HS256'])
        user_highscore = db_session.query(Highscore).filter_by(user_id=jwt_payload['user_id']).first()
        if(user_highscore is not None):
            if(user_highscore.score < score):
                user_highscore.score = score
                db_session.commit()
                return {'status': 200, 'updated': True, 'message': 'Highscore updated.'}, 200
            else:
                return {'status': 200, 'updated': False, 'message': 'Highscore could not be updated.'}, 200
        else:
            return {'status': 404, 'message': 'The server could not find your user account.'}, 404
        pass

    def get(self, userid):
        user_id = None
        if(userid == '-1'):
            args = highscorePostParser.parse_args()
            jwt_encoded = args['Authorization'][7:]
            jwt_payload = jwt.decode(jwt_encoded, JWT_SECRET, algorithms=['HS256'])
            user_id = jwt_payload['user_id']
        else:
            user_id = int(userid)
        user_highscore = db_session.query(Highscore).filter_by(user_id=user_id).first()
        if(user_highscore is not None):
            return {'status': 200, 'message': 'Highscore retrieved with success.',
                    'score': user_highscore.score}
        else:
            return {'status': 404, 'message': 'The server could not find your user account.'}, 404
        pass

class HighscoreRankingResource(Resource):
    def get(self):
        args = rankingParser.parse_args()

        try:
            ordered_highscores = db_session.query(Highscore).join(User).order_by(Highscore.score.desc())

            per_page, page = args['per_page'], args['page']
            if(per_page is not None):
                ordered_highscores = ordered_highscores.limit(per_page)
            if(page is not None):
                ordered_highscores = ordered_highscores.offset(per_page*page)

            result = highscoreSchema.dump(ordered_highscores.all()).data
        except Exception as exc:
            return {'status': 500, 'message': 'An unknown error occurred, try again later.'}, 500

        return {'status': 200, 'message': 'Ranking retrieved with success.','ranking': result}, 200
        pass