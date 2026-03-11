from flask import Flask
from app.extensions import db, login_manager
from app.config import Config
import os

def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "templates"
        ),
    )
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth import auth_bp
    from app.todos import todos_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todos_bp)

    with app.app_context():
        db.create_all()

    return app
