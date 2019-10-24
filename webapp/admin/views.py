from flask import Blueprint
from flask_login import login_required, current_user

blueprint = Blueprint('admin', __name__)

@blueprint.route('/admin')
@login_required
def admin_index():
    if current_user.is_admin:
        return 'You are admin'
    else:
        return 'You are user'          
