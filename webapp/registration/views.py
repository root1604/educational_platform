from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from webapp.db.db import db
from webapp.login.decorators import admin_required
from webapp.login.forms import RegistrationForm
from webapp.login.models import User

blueprint = Blueprint('registration', __name__)         

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
        is_access_rights_page = False
        form = RegistrationForm()
        return render_template('registration/registration.html', page_title=title, is_homepage=is_homepage,
                                is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                is_adminpage=is_adminpage, is_registrationpage=is_registrationpage,
                                form=form, is_access_rights_page=is_access_rights_page)
    elif request.method == 'POST': 
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, role=form.role.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('The user ' + new_user.username + ' was created successfully.')
            return redirect(url_for('homepage.index'))
        else:    
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Error in the field "{}":  {}'.format(getattr(form, field).label.text, error))
            return redirect(url_for('registration.registration'))
    else:
        return redirect('/')
