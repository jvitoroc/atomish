from marshmallow import fields, Schema, validates, ValidationError

class UserSchema(Schema):
    username = fields.String(
        required=True,
        allow_none=True
    )
    password = fields.String(
        required=True,
        allow_none=True
    )

class UserRegistrationSchema(UserSchema):

    @validates('username')
    def validate_username(self, value):
        if(value == None):
            raise ValidationError('Username was not provided.')
        value_len = len(value)
        if(value_len == 0):
            raise ValidationError('Username was not provided.')
        if value_len < 6:
            raise ValidationError('Username is too short, it\'s required at least 6 characters.')
        if value_len > 20:
            raise ValidationError('Username is too long, it\'s required at most 20 characters.')

    @validates('password')
    def validate_password(self, value):
        if (value == None):
            raise ValidationError('Password was not provided.')
        value_len = len(value)
        if (value_len == 0):
            raise ValidationError('Password was not provided.')
        if value_len < 6:
            raise ValidationError('Password is too short, it\'s required at least 6 characters.')
        if value_len > 20:
            raise ValidationError('Password is too long, it\'s required at most 20 characters.')

class UserLoginSchema(UserSchema):

    @validates('username')
    def validate_username(self, value):
        if(value == None):
            raise ValidationError('Username was not provided.')
        value_len = len(value)
        if(value_len == 0):
            raise ValidationError('Username was not provided.')
        if value_len < 6 or value_len > 20:
            raise ValidationError('Username is invalid.')

    @validates('password')
    def validate_password(self, value):
        if (value == None):
            raise ValidationError('Password was not provided.')
        value_len = len(value)
        if (value_len == 0):
            raise ValidationError('Password was not provided.')
        if value_len < 6 or value_len > 20:
            raise ValidationError('Password is invalid.')