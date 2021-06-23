import os
    
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL='http://quotes.stormconsultancy.co.uk/random.json'
        #email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://est:newpassword@localhost/blogger'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    pass
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    }