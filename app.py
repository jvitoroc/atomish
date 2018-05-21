from flask import Flask
from flask_restful import Api
from resources import UserRegistrationResource, UserLoginResource
from resources import HighscoreResource, HighscoreRankingResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UserRegistrationResource, '/user/register')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(HighscoreResource, '/highscore', '/highscore/<string:userid>')
api.add_resource(HighscoreRankingResource, '/highscore/ranking')

if __name__ == '__main__':
    app.run(debug=True)