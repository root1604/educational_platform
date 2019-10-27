from flask_wtf import FlaskForm
from webapp.login.models import User
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],
                              render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember me', default=True, render_kw={"class": "form-check-input"})                          
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],
                              render_kw={"class": "form-control"})
    password2 = PasswordField('Retype the password', validators=[DataRequired(),
                               EqualTo('password')], render_kw={"class": "form-control"})   
    role = RadioField('Role', choices=[('admin','admin'), ('teacher','teacher'), ('student','student')],
                       default='student', validators=[DataRequired()],
                       render_kw={"class": "form-control", "style":"list-style-type:none"})                                                                  
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('The user ' + username.data + ' already exists.Try again.')
