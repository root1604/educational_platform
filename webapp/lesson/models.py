from webapp.db.db import db

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
