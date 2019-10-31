from flask import Blueprint, redirect,render_template, request
from flask_login import login_required, current_user
from sqlalchemy import exc
from webapp.access_rights.models import Access_rights
from webapp.category.models import Category
from webapp.course.models import Course
from webapp.db.db import db

blueprint = Blueprint('category', __name__)

@blueprint.route('/categories', methods=['GET', 'POST'])
@login_required 
def add_a_category():
    if request.method == 'POST':
        if current_user.is_admin:
            try:
                name = request.form['category']
                category_description = 'This is a description'
                new_category = Category(name, category_description)
                if new_category.name != '':
                    db.session.add(new_category)
                    db.session.commit()
            except(exc.IntegrityError):
                print('the category exists')
                return redirect('/categories')     
            return redirect('/categories') 
        else:
            return redirect('/categories')     
    elif request.method == 'GET':
        title = "Categories"
        is_homepage = False
        is_loginpage = False
        is_catalogpage = True
        is_adminpage = False
        is_registrationpage = False
        is_access_rights_page = False
        categories = Category.query.order_by(Category.name).all() 
        return render_template('categories/categories.html', categories=categories, page_title=title,
                                is_homepage=is_homepage, is_loginpage=is_loginpage,
                                is_catalogpage=is_catalogpage, is_adminpage=is_adminpage,
                                is_registrationpage=is_registrationpage, is_access_rights_page=is_access_rights_page)
    else:
        return redirect('/')                            


@blueprint.route('/delete_a_category', methods=['POST'])
@login_required    
def delete_a_category():
    if current_user.is_admin:
        try:
            category_id = request.form['category_id']
            Category.query.filter_by(id=category_id).delete() 
            db.session.commit()
        except:
            return redirect('/categories')    
        return redirect('/categories') 
    else:
        return redirect('/categories')   

@blueprint.route('/<link_path>', methods=['GET', 'POST'])
@login_required
def page(link_path):
    category_exists = Category.query.filter_by(name=link_path).first()
    if category_exists:
        if request.method == 'POST':
            if current_user.is_admin:
                try:
                    name = request.form['course']
                    course_description = 'This is the best course'
                    new_course = Course(name, category_exists.id, course_description)              
                    if new_course.name != '':
                        db.session.add(new_course)
                        db.session.commit()
                except(exc.IntegrityError):
                    print('the course exists')
                return redirect('/'+link_path) 
            else:
                return redirect('/'+link_path)     
        elif request.method == 'GET':
            title = link_path
            is_homepage = False
            is_loginpage = False
            is_catalogpage = False
            is_adminpage = False
            is_registrationpage = False
            is_access_rights_page = False
            if current_user.is_admin:
                courses = Course.query.filter(Course.category_id==category_exists.id).all() 
            else:
                courses = (db.session.query(Access_rights, Course)
                                .join(Course, Course.id == Access_rights.course_id)
                                .filter(Access_rights.user_id == current_user.id, 
                                 Access_rights.category_id == category_exists.id,
                                 Access_rights.grant_access == True)
                                .order_by(Course.name)
                                ).all()        
            return render_template('categories/category.html', category_name=link_path, 
                                    courses=courses, category_id=category_exists.id, page_title=title, is_homepage=is_homepage,
                                    is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                    is_adminpage=is_adminpage, is_registrationpage=is_registrationpage,
                                    is_access_rights_page=is_access_rights_page) 
        else:
             return render_template('error.html')        
    else:
        return render_template('error.html')    