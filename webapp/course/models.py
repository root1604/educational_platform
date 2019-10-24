from webapp.db.db import db

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