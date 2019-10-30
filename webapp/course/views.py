from flask import Blueprint, redirect,render_template, request
from flask_login import login_required, current_user
from sqlalchemy import exc
from webapp.category.models import Category
from webapp.course.models import Course
from webapp.lesson.models import Lesson
from webapp.db.db import db

blueprint = Blueprint('course', __name__)

@blueprint.route('/<category_name>/<course_name>', methods=['GET', 'POST'])
@login_required    
def course_page(category_name, course_name):
    category_exists = Category.query.filter_by(name=category_name).first()
    if category_exists:
        course_exists = Course.query.filter(Course.name==course_name, Course.category_id==category_exists.id).first() 
        if course_exists:
            if request.method == 'POST':
                if current_user.is_admin or current_user.is_teacher:
                    try:
                        name = request.form['lesson']
                        lesson_description = 'This is a lesson description'
                        new_lesson = Lesson(name, course_exists.id, lesson_description)              
                        if new_lesson.name != '':
                            db.session.add(new_lesson)
                            db.session.commit()
                    except(exc.IntegrityError):
                        print('the lesson exists')
                    return redirect('/' + category_name + '/' + course_name) 
                else:
                    return redirect('/' + category_name + '/' + course_name)   
            elif request.method == 'GET': 
                title = course_name
                is_homepage = False
                is_loginpage = False
                is_catalogpage = False
                is_adminpage = False
                is_registrationpage = False
                is_access_rights_page = False
                lessons = Lesson.query.filter(Lesson.course_id==course_exists.id).all()   
                return render_template('courses/course.html', category_name=category_name, course_name=course_name,
                                        lessons=lessons, page_title=title, is_homepage=is_homepage,
                                        is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                        is_adminpage=is_adminpage, is_registrationpage=is_registrationpage,
                                        is_access_rights_page=is_access_rights_page) 
            else:
                return render_template('error.html')     
        else:
            return render_template('error.html')    
    else:
        return render_template('error.html') 

@blueprint.route('/delete_a_course', methods=['POST'])
@login_required    
def delete_a_course():
    if current_user.is_admin:
        course_id = request.form['course_id']
        course_for_delete=Course.query.filter_by(id=course_id).first()
        category_name=course_for_delete.category.name
        try:        
            Course.query.filter_by(id=course_id).delete() 
            db.session.commit()
        except:
            return redirect('/'+category_name)    
        return redirect('/'+category_name)   
    else:
        return redirect('/'+category_name)          