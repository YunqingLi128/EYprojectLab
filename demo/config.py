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
    DEBUG = True


