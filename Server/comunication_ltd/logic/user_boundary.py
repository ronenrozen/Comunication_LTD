from flask_jwt_extended import create_access_token

from Server.comunication_ltd.database.models import User


class UserPayload:

    def __init__(self, id=None, email=None, password=None, salt=None):
        self.id = id
        self.email = email

    def serialize(self):
        return {"id": self.id,
                "email": self.email,
                "access_token": create_access_token(identity=self.email)}


def parse_user(payload):
    email, password = payload.get_json().values()
    return User(email=email, password=password)
