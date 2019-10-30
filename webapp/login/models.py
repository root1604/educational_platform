from flask_login import UserMixin
from webapp.db.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    access_rights = db.relationship('Access_rights', backref='user', lazy='dynamic') 
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_teacher(self):
        return self.role == 'teacher'    

    @property
    def is_student(self):
        return self.role == 'student'    

    def __repr__(self):
        return self.username
    