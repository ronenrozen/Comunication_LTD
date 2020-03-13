from comunication_ltd import ma
from comunication_ltd.database.models import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
