import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://est:newpassword@localhost/blogger'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://est:newpassword@localhost/blogger'
    SECRET_KEY = os.environ.get('SECRET_KEY') or '8c44b407c2896a289a57817228ca8ed1'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    pass
    
class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    }