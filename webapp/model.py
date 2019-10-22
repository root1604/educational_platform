from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Category(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False, unique=True)
        courses = db.relationship('Course', backref='category', lazy='dynamic')  
        def __init__(self, name):
            self.name = name  
        def __repr__(self):
            return '<Category {}>'.format(self.name)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.Text(1000), nullable=True)
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic')
    __table_args__ = (db.UniqueConstraint('category_id', 'name'),)
    def __init__(self, name, category_id, description):
        self.name = name 
        self.category_id = category_id
        self.description = description 
    def __repr__(self):
        return '<Course {}>'.format(self.name)   

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    description = db.Column(db.Text(1000), nullable=True)
    videos = db.relationship('Video', backref='lesson', lazy='dynamic')
    images = db.relationship('Image', backref='lesson', lazy='dynamic')
    textlectures = db.relationship('TextLecture', backref='lesson', lazy='dynamic')
    audios = db.relationship('Audio', backref='lesson', lazy='dynamic')
    __table_args__ = (db.UniqueConstraint('course_id', 'name'),)
    def __init__(self, name, course_id, description):
        self.name = name 
        self.course_id = course_id
        self.description = description 
    def __repr__(self):
        return '<Lesson {}>'.format(self.name)   

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    def __init__(self, name, lesson_id):
        self.name = name 
        self.lesson_id = lesson_id
    def __repr__(self):
        return '<Video {}>'.format(self.name)       

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    def __init__(self, name, lesson_id):
        self.name = name 
        self.lesson_id = lesson_id
    def __repr__(self):
        return '<Image {}>'.format(self.name)                 

class TextLecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    text = db.Column(db.Text(1000), nullable=True)
    def __init__(self, name, lesson_id, text):
        self.name = name 
        self.lesson_id = lesson_id
        self.text = text 
    def __repr__(self):
        return '<TextLecture {}>'.format(self.name)       

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    def __init__(self, name, lesson_id):
        self.name = name 
        self.lesson_id = lesson_id
    def __repr__(self):
        return '<Audio {}>'.format(self.name)     

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)                                 