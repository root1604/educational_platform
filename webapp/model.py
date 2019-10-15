from flask_sqlalchemy import SQLAlchemy

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
    __table_args__ = (db.UniqueConstraint('course_id', 'name'),)
    def __init__(self, name, course_id, description):
        self.name = name 
        self.course_id = course_id
        self.description = description 
    def __repr__(self):
        return '<Lesson {}>'.format(self.name)   

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    aws_key = db.Column(db.String(2000), nullable=True)
    def __init__(self, name, lesson_id, url):
        self.name = name 
        self.lesson_id = lesson_id
        self.aws_key = aws_key
    def __repr__(self):
        return '<Video {}>'.format(self.name)       

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    aws_key = db.Column(db.String(2000), nullable=True)
    def __init__(self, name, lesson_id, url):
        self.name = name 
        self.lesson_id = lesson_id
        self.aws_key = aws_key
    def __repr__(self):
        return '<Image {}>'.format(self.name)                 

class TextLecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    text = db.Column(db.Text(1000), nullable=True)
    aws_key = db.Column(db.String(2000), nullable=True)
    def __init__(self, name, lesson_id, url):
        self.name = name 
        self.lesson_id = lesson_id
        self.text = text 
        self.aws_key = aws_key
    def __repr__(self):
        return '<TextLecture {}>'.format(self.name)                         