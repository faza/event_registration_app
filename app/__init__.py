from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import db, User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_registration.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app import routes
    app.add_url_rule('/', 'index', routes.index)
    app.add_url_rule('/register', 'register', routes.register, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', routes.login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', routes.logout)
    app.add_url_rule('/create_event', 'create_event', routes.create_event, methods=['GET', 'POST'])
    app.add_url_rule('/events', 'list_events', routes.list_events)
    app.add_url_rule('/event/<int:event_id>', 'event_details', routes.event_details)
    app.add_url_rule('/register_for_event/<int:event_id>', 'register_for_event', routes.register_for_event, methods=['GET', 'POST'])
    app.add_url_rule('/home', 'home', routes.dashboard)
    app.add_url_rule('/search', 'search_events', routes.search_events, methods=['GET', 'POST'])

    return app
