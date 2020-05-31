import configparser
from pathlib import Path
import secrets

FILE_PATH = (Path(__file__).parent / 'config.ini').resolve()
CONFIG_PARSER = configparser.ConfigParser()


class Config:

    def __init__(self):
        if not FILE_PATH.is_file():
            self.create_config()
        else:
            CONFIG_PARSER.read(str(FILE_PATH))

    @staticmethod
    def create_config():
        CONFIG_PARSER['GENERAL'] = {
            'SECRET_KEY': secrets.token_hex(16),
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///database/server.db',
            'PASSWORD_LENGTH': 10,
            'IS_BIG_LETTERS': True,
            'IS_SMALL_LETTERS': True,
            'IS_NUMBERS': True,
            'SPECIAL_CHAR': True,
            'PASSWORD_ATTEMPTS': 3}

        with open(str(FILE_PATH), 'w') as configfile:
            CONFIG_PARSER.write(configfile)

    @staticmethod
    def get_value(key, default):
        try:
            return CONFIG_PARSER.get('GENERAL', key)
        except (configparser.NoOptionError, KeyError):
            return default

    @staticmethod
    def set_value(key, value):
        try:
            CONFIG_PARSER.set('GENERAL', key, value)
            with open(str(FILE_PATH), 'w') as configfile:
                CONFIG_PARSER.write(configfile)
        except (configparser.NoSectionError, TypeError):
            return None
