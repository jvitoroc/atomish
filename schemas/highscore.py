from marshmallow import fields, Schema
from schemas.user import UserSchema

class HighscoreSchema(Schema):
    user = fields.Nested(UserSchema, only=['username'])
    score = fields.Integer()

