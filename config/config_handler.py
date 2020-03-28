import configparser
from pathlib import Path
import secrets
from waf import log

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
        CONFIG_PARSER['APP'] = {
            'SECRET_KEY': secrets.token_hex(16),
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///database/server.db'}
        CONFIG_PARSER['PASSWORD'] = {
            'password_length': 10,
            'server_url': ''
        }
        with open(str(FILE_PATH), 'w') as configfile:
            CONFIG_PARSER.write(configfile)

    @staticmethod
    def get_value(section, key, default):
        try:
            return CONFIG_PARSER.get(section, key)
        except (configparser.NoOptionError, KeyError):
            log.exception(f"Key - '{key}' dont exist in the config file, using default value - {default}.")
            return default

    @staticmethod
    def set_value(section, key, value):
        try:
            CONFIG_PARSER.set(section, key, value)
            with open(str(FILE_PATH), 'w') as configfile:
                CONFIG_PARSER.write(configfile)
        except (configparser.NoSectionError, TypeError):
            log.exception(f"Key - '{key}' dont exist in the config file, using default value - {default}.")
            return None

