from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from webapp.db.db import db
from webapp.login.decorators import admin_required
from webapp.login.models import User

blueprint = Blueprint('admin', __name__)

@blueprint.route('/admin', methods=['GET'])
@admin_required
def admin_index():
    if request.method == 'GET':
        title = "Settings"
        is_homepage = False
        is_loginpage = False
        is_catalogpage = False
        is_adminpage = True
        is_registrationpage = False
        return render_template('admin/index.html', page_title=title, is_homepage=is_homepage,
                                is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                is_adminpage=is_adminpage, is_registrationpage=is_registrationpage)
    else:
        return redirect('/')                   

@blueprint.route('/registration', methods=['GET', 'POST'])
@admin_required
def registration():
    if request.method == 'GET':
        title = "Registration"
        is_homepage = False
        is_loginpage = False
        is_catalogpage = False
        is_adminpage = False
        is_registrationpage = True
        return render_template('admin/registration.html', page_title=title, is_homepage=is_homepage,
                                is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                is_adminpage=is_adminpage, is_registrationpage=is_registrationpage)
    elif request.method == 'POST':
        username = request.form['login']
        username_exists=User.query.filter_by(username=username).first()
        if username_exists and username == username_exists.username:
            flash('The user ' + username + ' already exists.Try again')
            return redirect(url_for('admin.registration'))
        password_1 = request.form['password_1']
        password_2 = request.form['password_2']
        if not password_1 == password_2:
            flash('''Those passwords didn't match. Try again.''')
            return redirect(url_for('admin.registration'))
        role = request.form['role']
        new_user = User(username=username, role=role)
        new_user.set_password(password_1)
        db.session.add(new_user)
        db.session.commit() 
        flash('The user ' + username + ' was created successfully.')       
        return redirect(url_for('homepage.index'))
    else:
        return redirect('/')
