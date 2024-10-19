from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    lti_user_id = db.Column(db.String(255), unique=True, nullable=True)
    worksheets = db.relationship('Worksheet', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Worksheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    grade_level = db.Column(db.String(20), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    subtopic = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    estimated_time = db.Column(db.Integer, nullable=True)  # in minutes
    learning_objectives = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('worksheet_template.id'), nullable=True)
    is_shared = db.Column(db.Boolean, default=False)
    shared_with = db.Column(db.String(255), default='')
    file_name = db.Column(db.String(255), nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    file_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class WorksheetTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    template_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
