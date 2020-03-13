from comunication_ltd.database.models import User


class UserPayload:

    def __init__(self, id=None, username=None, password=None, mail=None, salt=None):
        self.id = id
        self.username = username
        self.password = password
        self.mail = mail
        self.salt = salt

    def serialize(self):
        return {"id": self.id,
                "username": self.username,
                "password": self.password,
                "salt": self.salt}


def parse_user(payload):
    username, password, mail, salt = payload.get_json().values()
    return User(username=username, password=password, mail=mail, salt=salt)
