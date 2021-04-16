from os import getenv


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = getenv('JWT_KEY')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv('DB_URI_DEV')


class ProductionConfig(Config):
    ...


class TestConfig(Config):
    ...


config_selector = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
