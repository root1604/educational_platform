from flask import Blueprint, render_template, flash, redirect, url_for
from webapp.access_rights.models import Access_rights
from webapp.db.db import db
from webapp.login.decorators import admin_required

blueprint = Blueprint('access_levels', __name__)

@blueprint.route('/access_rights', methods=['GET'])

@admin_required
def access_rights():
    title = "Access rights"
    is_homepage = False
    is_loginpage = False
    is_catalogpage = False
    is_adminpage = False
    is_registrationpage = False
    is_access_rights_page = True

    access_rights = Access_rights.query.order_by(Access_rights.course_id.name).all()

    return render_template('access_rights/access_rights.html', access_rights=access_rights, 
                            page_title=title, is_homepage=is_homepage,
                            is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                            is_adminpage=is_adminpage, is_registrationpage=is_registrationpage,
                            is_access_rights_page=is_access_rights_page)

# @blueprint.route('/grant_access', methods=['POST'])
# @admin_required
# def grant_access():
#     category_id = request.form['category_id']
#     course_id = request.form['course_id']
#     """ query existing access rights from access_rights filter by category_id and course_id
#     and then click botton add users that don't have access to the course"""
