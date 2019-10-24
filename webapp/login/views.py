from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from webapp.login.models import User
from webapp.login.forms import LoginForm

blueprint = Blueprint('login', __name__)

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage.index'))
    title = "Authorization"
    login_form = LoginForm()
    is_homepage = False
    is_loginpage = True
    return render_template('login/login.html', page_title=title, form=login_form, is_homepage=is_homepage,
                            is_loginpage=is_loginpage)   

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You are logged in')
            return redirect(url_for('homepage.index'))

    flash('The username or password is wrong')
    return redirect(url_for('login.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('homepage.index'))  