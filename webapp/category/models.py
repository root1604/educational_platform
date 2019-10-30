from webapp.db.db import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text(1000), nullable=True) 
    courses = db.relationship('Course', backref='category', lazy='dynamic') 
    access_rights = db.relationship('Access_rights', backref='category', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name 
        self.description = description 
    def __repr__(self):
        return self.name
