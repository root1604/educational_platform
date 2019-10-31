from flask import Blueprint, render_template, flash, redirect, request, url_for
from sqlalchemy import desc
from webapp.access_rights.forms import Add_user_to_courseForm
from webapp.access_rights.models import Access_rights
from webapp.category.models import Category
from webapp.course.models import Course
from webapp.db.db import db
from webapp.login.decorators import admin_required
from webapp.login.models import User

blueprint = Blueprint('access_levels', __name__)

@blueprint.route('/access_rights', methods=['GET', 'POST'])

@admin_required
def access_rights():
    title = "Access rights"
    is_homepage = False
    is_loginpage = False
    is_catalogpage = False
    is_adminpage = False
    is_registrationpage = False
    is_access_rights_page = True

    if request.method == 'POST':
        sort_type = request.form['sort_by']
        access_rights = access_rights_query(sort_type)    
    else:
        access_rights = access_rights_query("sort_by_course_asc") 

    form = Add_user_to_courseForm()
    users_list = []
    courses_list = []
    users_query = User.query.order_by(User.username).all()
    for users_query_counter in users_query:
        user_id = users_query_counter.id
        username = users_query_counter.username
        user = (user_id, username)
        if not users_query_counter.role == 'admin':
            users_list.append(user)
    courses_query = (db.session.query(Course, Category)
            .join(Category, Category.id == Course.category_id)
            .order_by(Course.name)
            ).all() 
    for courses_query_counter in courses_query: 
        course_id = courses_query_counter.Course.id
        coursename = courses_query_counter.Course
        categoryname = courses_query_counter.Category
        coursename = str(categoryname) + ': ' + str(coursename)
        course = (course_id, coursename)
        courses_list.append(course)
    form.username.choices = users_list
    form.course.choices = courses_list
    form.query_factory = courses_query
    return render_template('access_rights/access_rights.html', access_rights=access_rights, 
                            page_title=title, form=form, is_homepage=is_homepage,
                            is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                            is_adminpage=is_adminpage, is_registrationpage=is_registrationpage,
                            is_access_rights_page=is_access_rights_page)

def access_rights_query(sort_type_str):
    if sort_type_str == "sort_by_username_asc":
            access_rights = (db.session.query(Access_rights, User, Category, Course)
            .join(User, User.id == Access_rights.user_id)
            .join(Category, Category.id == Access_rights.category_id)
            .join(Course, Course.id == Access_rights.course_id)
            .filter(Access_rights.grant_access == True)
            .order_by(User.username)
            ).all()
    elif sort_type_str == "sort_by_username_desc": 
        access_rights = (db.session.query(Access_rights, User, Category, Course)
        .join(User, User.id == Access_rights.user_id)
        .join(Category, Category.id == Access_rights.category_id)
        .join(Course, Course.id == Access_rights.course_id)
        .filter(Access_rights.grant_access == True)
        .order_by(desc(User.username))
        ).all() 
    elif sort_type_str == "sort_by_category_asc":
        access_rights = (db.session.query(Access_rights, User, Category, Course)
        .join(User, User.id == Access_rights.user_id)
        .join(Category, Category.id == Access_rights.category_id)
        .join(Course, Course.id == Access_rights.course_id)
        .filter(Access_rights.grant_access == True)
        .order_by(Category.name)
        ).all()
    elif sort_type_str == "sort_by_category_desc": 
        access_rights = (db.session.query(Access_rights, User, Category, Course)
        .join(User, User.id == Access_rights.user_id)
        .join(Category, Category.id == Access_rights.category_id)
        .join(Course, Course.id == Access_rights.course_id)
        .filter(Access_rights.grant_access == True)
        .order_by(desc(Category.name))
        ).all() 
    elif sort_type_str == "sort_by_course_asc":
        access_rights = (db.session.query(Access_rights, User, Category, Course)
        .join(User, User.id == Access_rights.user_id)
        .join(Category, Category.id == Access_rights.category_id)
        .join(Course, Course.id == Access_rights.course_id)
        .filter(Access_rights.grant_access == True)
        .order_by(Course.name)
        ).all()
    elif sort_type_str == "sort_by_course_desc": 
        access_rights = (db.session.query(Access_rights, User, Category, Course)
        .join(User, User.id == Access_rights.user_id)
        .join(Category, Category.id == Access_rights.category_id)
        .join(Course, Course.id == Access_rights.course_id)
        .filter(Access_rights.grant_access == True)
        .order_by(desc(Course.name))
        ).all()             
    else:
        access_rights = (db.session.query(Access_rights, User, Category, Course)
        .join(User, User.id == Access_rights.user_id)
        .join(Category, Category.id == Access_rights.category_id)
        .join(Course, Course.id == Access_rights.course_id)
        .filter(Access_rights.grant_access == True)
        .order_by(Course.name)
    ).all()       
    return access_rights

@blueprint.route('/delete_a_user_from_a_course', methods=['POST'])
@admin_required    
def delete_a_user_from_a_course():
    try:
        delete_access_rights_id = request.form['delete_access_rights_id']
        Access_rights.query.filter_by(id=delete_access_rights_id).delete() 
        db.session.commit()
    except:
        flash('Error while deleting. Try again.') 
        return redirect(url_for('access_levels.access_rights') )  
    flash('Successfully deleted.')    
    return redirect(url_for('access_levels.access_rights')) 
    
@blueprint.route('/grant_access', methods=['POST'])
@admin_required
def grant_access():
    form = Add_user_to_courseForm()
    if form.username.data:
        try:
            username = int(form.username.data)
        except:
            flash('The user id ' + username + """isn't correct.""")
            return redirect(url_for('access_levels.access_rights'))    
    else:
        flash('Fill in the username field.')
        return redirect(url_for('access_levels.access_rights'))
    if form.course.data:  
        try:   
            course = int(form.course.data)
        except:
            flash('The course id ' + course + """isn't correct.""")
            return redirect(url_for('access_levels.access_rights'))     
    else:
        flash('Fill in the category field.')
        return redirect(url_for('access_levels.access_rights')) 
    user_exists = User.query.filter_by(id=username).first()
    if user_exists:
        course_exists = Course.query.filter(Course.id==course).first()
        if course_exists: 
            access_right_exists = Access_rights.query.filter(Access_rights.user_id==username,
                                                             Access_rights.category_id==course_exists.category_id,
                                                             Access_rights.course_id==course).first()
            if not access_right_exists:                                                                
                new_access_right = Access_rights(user_id=username,
                                                 category_id=course_exists.category_id,
                                                 course_id=course,
                                                 grant_access=True)
                db.session.add(new_access_right)
                db.session.commit()
                flash('The access right was granted successfully.')
                return redirect(url_for('access_levels.access_rights'))
            else:
                flash('This user already has access to this course.')
                return redirect(url_for('access_levels.access_rights'))    
        else:
            flash("""This course doesn't exist.""")
            return redirect(url_for('access_levels.access_rights'))                
    else:
        flash('The user with id ' + str(username) + """ doesn't exist.""")
        return redirect(url_for('access_levels.access_rights'))     
    return redirect(url_for('access_levels.access_rights'))
