from flask import Blueprint, render_template
from webapp.category.models import Category

blueprint = Blueprint('homepage', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    title = "Homepage"
    is_homepage = True
    is_loginpage = False
    is_catalogpage = False
    is_adminpage = False
    is_registrationpage = False
    categories = Category.query.order_by(Category.name).all()  
    return render_template('homepage/index.html', categories=categories, page_title=title, is_homepage=is_homepage,
                            is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                            is_adminpage=is_adminpage, is_registrationpage=is_registrationpage)
