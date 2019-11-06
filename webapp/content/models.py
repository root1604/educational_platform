from webapp.db.db import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id', ondelete='CASCADE'), nullable=False)
    def __init__(self, name, lesson_id):
        self.name = name 
        self.lesson_id = lesson_id
    def __repr__(self):
        return '<Video {}>'.format(self.name)       

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id', ondelete='CASCADE'), nullable=False)
    def __init__(self, name, lesson_id):
        self.name = name 
        self.lesson_id = lesson_id
    def __repr__(self):
        return '<Image {}>'.format(self.name)                 

class TextLecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id', ondelete='CASCADE'), nullable=False)
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
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id', ondelete='CASCADE'), nullable=False)
    def __init__(self, name, lesson_id):
        self.name = name 
        self.lesson_id = lesson_id
    def __repr__(self):
        return '<Audio {}>'.format(self.name)     
