from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        courses = db.relationship('Course', backref='category', lazy='dynamic')    
        def __repr__(self):
            return '<Category {}>'.format(self.name)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.name)   

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    videos = db.relationship('Video', backref='lesson', lazy='dynamic')
    images = db.relationship('Image', backref='lesson', lazy='dynamic')
    textlectures = db.relationship('TextLecture', backref='lesson', lazy='dynamic')
    def __repr__(self):
        return '<Lesson {}>'.format(self.name)   

 class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    url = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Video {}>'.format(self.name)       

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    url = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Image {}>'.format(self.name)                 

class TextLecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<TextLecture {}>'.format(self.name)                         