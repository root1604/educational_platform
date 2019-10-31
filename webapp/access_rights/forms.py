from flask_wtf import FlaskForm
from webapp.access_rights.models import Access_rights
from wtforms import SelectField, SubmitField


class Add_user_to_courseForm(FlaskForm):
    username = SelectField('user', render_kw={"class": "form-control"}, default=1)
    course = SelectField('course', render_kw={"class": "form-control"}, default=1)                                                          
    submit = SubmitField('Add user to course', render_kw={"class": "btn btn-primary"})
