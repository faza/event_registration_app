from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_user(cls, username, email, password):
        user = cls(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def update_user(self, username=None, email=None, password=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if password:
            self.set_password(password)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organizer = db.relationship('User', backref=db.backref('events', lazy=True))

    @classmethod
    def create_event(cls, title, description, date, location, organizer_id):
        event = cls(title=title, description=description, date=date, location=location, organizer_id=organizer_id)
        db.session.add(event)
        db.session.commit()
        return event

    @classmethod
    def get_event_by_id(cls, event_id):
        return cls.query.get(event_id)

    @classmethod
    def get_all_events(cls):
        return cls.query.all()

    def update_event(self, title=None, description=None, date=None, location=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if date:
            self.date = date
        if location:
            self.location = location
        db.session.commit()

    def delete_event(self):
        db.session.delete(self)
        db.session.commit()
