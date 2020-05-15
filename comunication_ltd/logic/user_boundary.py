from comunication_ltd.database.models import User


class UserPayload:

    def __init__(self, id=None, email=None, password=None, salt=None):
        self.id = id
        self.email = email

    def serialize(self):
        return {"id": self.id,
                "email": self.email}


def parse_user(payload):
    username, password, mail, salt = payload.get_json().values()
    return User(username=username, password=password, mail=mail, salt=salt)
