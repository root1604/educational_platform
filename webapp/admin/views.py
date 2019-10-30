from flask import Blueprint, redirect, render_template, request, url_for
from webapp.login.decorators import admin_required

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
        is_access_rights_page = False
        return render_template('admin/index.html', page_title=title, is_homepage=is_homepage,
                                is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                is_adminpage=is_adminpage, is_registrationpage=is_registrationpage,
                                is_access_rights_page=is_access_rights_page)
    else:
        return redirect('/')  
