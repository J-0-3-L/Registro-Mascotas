from flask import Flask

from flask_wtf import CSRFProtect
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


from config import Config

from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
# from flask_smorest import Api
# from flask_marshmallow import Marshmallow

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
# login_manager = LoginManager()

http_auth = HTTPBasicAuth()
jwt = JWTManager()
# smorest_api = Api()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app,db)
    # login_manager.init_app(app)
    jwt.init_app(app)
    # smorest_api.init_app(app)
    # ma.init_app(app)

    
    with app.app_context():
    
        from app.views import bp as views_bp
        from app.pets import bp as pets_bp
        

    
        app.register_blueprint(views_bp)
        app.register_blueprint(pets_bp)
        

    return app