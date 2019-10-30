from webapp.db.db import db

class Access_rights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grant_access = db.Column(db.Boolean, default=False, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'category_id', 'course_id'),)
    def __init__(self, user_id, category_id, course_id, grant_access):
        self.user_id = user_id 
        self.category_id = category_id
        self.course_id = course_id
        self.grant_access = grant_access 
    def __repr__(self):
        return '<Access rights {} {} {}>'.format(self.user_id, self.category_id, self.course_id)   
