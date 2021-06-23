from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from . auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/authenticate')

    from . main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # setting config
    from .requests import configure_request
    configure_request(app)


    return app