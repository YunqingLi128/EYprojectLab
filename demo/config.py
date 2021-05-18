class Config(object):
    DEBUG = False
    TESTING = False

    @property
    def DATA_PATH(self):
        return 'test'


class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = '192.168.19.32'  # Not used currently


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'  # Not used currently
    SESSION_COOKIE_PATH = '/'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    SECRET_KEY = 'super secret key'
    DEBUG = True
    FRONT_END_HOST = 'http://localhost:8080'

