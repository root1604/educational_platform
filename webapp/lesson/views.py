import boto3
from flask import Blueprint, current_app, Flask, redirect,render_template, request, Response
from flask_login import login_required, current_user
from sqlalchemy import exc
from webapp.category.models import Category
from webapp.content.models import Audio, Image, TextLecture, Video
from webapp.course.models import Course
from webapp.lesson.models import Lesson
from webapp.db.db import db
from webapp.s3.filters import file_type, create_presigned_url
from webapp.s3.upload_file_to_s3 import upload_file_to_s3
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'avi', 'mp4', 'mp3'])
ALLOWED_VIDEO_FILETYPES = set(['video/x-msvideo', 'video/mp4'])
ALLOWED_AUDIO_FILETYPES = set(['audio/mpeg'])
ALLOWED_IMAGE_FILETYPES = set(['image/png', 'image/jpeg', 'image/gif'])
ALLOWED_TEXT_FILETYPES = set(['text/plain', 'application/pdf'])

blueprint = Blueprint('lesson', __name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_bucket_from_s3():
    bucket = current_app.config["S3_BUCKET"]
    try:
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(bucket)
        return my_bucket
    except:
        return None           

@blueprint.route('/download', methods=['POST'])
@login_required
def download():
    key = request.form['key']
    my_bucket = get_bucket_from_s3()
    if my_bucket != None:
        file_obj = my_bucket.Object(key).get()
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    ) 

@blueprint.route('/<category_name>/<course_name>/<lesson_name>', methods=['GET', 'POST'])
@login_required    
def lesson_page(category_name, course_name, lesson_name):
    category_exists = Category.query.filter_by(name=category_name).first()
    if category_exists:
        course_exists = Course.query.filter(Course.name==course_name, Course.category_id==category_exists.id).first() 
        if course_exists:
            lesson_exists = Lesson.query.filter(Lesson.name==lesson_name, Lesson.course_id==course_exists.id).first()
            if lesson_exists:
                if request.method == 'POST':
                    if current_user.is_admin or current_user.is_teacher:
                        if "user_file" not in request.files:
                            return "No user_file key in request.files"
                        file = request.files["user_file"]
                        if file.filename == "":
                            return "Please select a file"
                        if file and allowed_file(file.filename):
                            file.filename = secure_filename(file.filename)
                            bucket = current_app.config["S3_BUCKET"]
                            upload_file_to_s3(file, bucket)
                            type_of_file = file_type(file.filename)
                            if type_of_file in ALLOWED_VIDEO_FILETYPES:
                                try:
                                    name = file.filename
                                    new_video = Video(name, lesson_exists.id)              
                                    if new_video.name != '':
                                        db.session.add(new_video)
                                        db.session.commit()
                                except(exc.IntegrityError):
                                    print('the videofile exists')
                                return redirect('/' + category_name + '/' + course_name + '/' + lesson_name)   
                            elif type_of_file in ALLOWED_AUDIO_FILETYPES:
                                try:
                                    name = file.filename
                                    new_audio = Audio(name, lesson_exists.id)              
                                    if new_audio.name != '':
                                        db.session.add(new_audio)
                                        db.session.commit()
                                except(exc.IntegrityError):
                                    print('the audiofile exists')
                                return redirect('/' + category_name + '/' + course_name + '/' + lesson_name) 
                            elif type_of_file in ALLOWED_IMAGE_FILETYPES:
                                try:
                                    name = file.filename
                                    new_image = Image(name, lesson_exists.id)              
                                    if new_image.name != '':
                                        db.session.add(new_image)
                                        db.session.commit()
                                except(exc.IntegrityError):
                                    print('the imagefile exists')
                                return redirect('/' + category_name + '/' + course_name + '/' + lesson_name)  
                            elif type_of_file in ALLOWED_TEXT_FILETYPES:
                                try:
                                    name = file.filename
                                    text = 'This is a text'
                                    new_text = TextLecture(name, lesson_exists.id, text)              
                                    if new_text.name != '':
                                        db.session.add(new_text)
                                        db.session.commit()
                                except(exc.IntegrityError):
                                    print('the textfile exists')
                                return redirect('/' + category_name + '/' + course_name + '/' + lesson_name)                                          
                        else:
                            return redirect('/' + category_name + '/' + course_name + '/' + lesson_name) 
                    else:
                        return redirect('/' + category_name + '/' + course_name + '/' + lesson_name)        
                elif request.method == 'GET':
                    title = lesson_name
                    is_homepage = False
                    is_loginpage = False
                    is_catalogpage = False
                    is_adminpage = False
                    is_registrationpage = False
                    lesson_videos = Video.query.filter(Video.lesson_id==lesson_exists.id).all()
                    my_bucket = get_bucket_from_s3()
                    s3 = boto3.resource('s3')
                    summaries = []
                    for v in lesson_videos:
                        video_file = s3.ObjectSummary(my_bucket,v.name)
                        summaries.append(video_file)
                    lesson_audios = Audio.query.filter(Audio.lesson_id==lesson_exists.id).all()
                    for a in lesson_audios:
                        audio_file = s3.ObjectSummary(my_bucket, a.name)
                        summaries.append(audio_file) 
                    lesson_images = Image.query.filter(Image.lesson_id==lesson_exists.id).all()
                    for i in lesson_images:
                        image_file = s3.ObjectSummary(my_bucket, i.name)
                        summaries.append(image_file) 
                    lesson_texts = TextLecture.query.filter(TextLecture.lesson_id==lesson_exists.id).all()      
                    for t in lesson_texts:
                        text_file = s3.ObjectSummary(my_bucket, t.name)
                        summaries.append(text_file)           
                    return render_template('lessons/lesson.html', category_name=category_name,
                                            course_name=course_name, lesson_name=lesson_name, 
                                            files=summaries, page_title=title, is_homepage=is_homepage,
                                            is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                            is_adminpage=is_adminpage, is_registrationpage=is_registrationpage)
                else:
                    return render_template('error.html')                           
            else:
                return render_template('error.html')     
        else:
            return render_template('error.html')    
    else:
        return render_template('error.html')   

@blueprint.route('/delete_a_lesson', methods=['POST'])
@login_required    
def delete_a_lesson():
    if current_user.is_admin or current_user.is_teacher:
        lesson_id = request.form['lesson_id']
        lesson_for_delete=Lesson.query.filter_by(id=lesson_id).first()
        course_name=lesson_for_delete.course.name
        category_name=lesson_for_delete.course.category.name
        try:        
            Lesson.query.filter_by(id=lesson_id).delete() 
            db.session.commit()
        except:
            return redirect('/' + category_name + '/' + course_name)    
        return redirect('/' + category_name + '/' + course_name) 
    else:
        return redirect('/' + category_name + '/' + course_name)     

@blueprint.route('/delete', methods=['POST'])
@login_required
def delete():
    key = (request.form['key'])
    key = key.split('*')
    file_to_delete = key[0] 
    category = key[1]
    course = key [2]
    lesson = key [3]
    link = '/' + category + '/' + course + '/' + lesson
    file_extension = '.' in file_to_delete and file_to_delete.rsplit('.', 1)[1]
    category_id = Category.query.filter_by(name=category).first().id
    course_id = Course.query.filter(Course.name==course, Course.category_id==category_id).first().id
    lesson_id = Lesson.query.filter(Lesson.name==lesson, Lesson.course_id==course_id).first().id
    if current_user.is_admin or current_user.is_teacher:
        try:
            my_bucket = get_bucket_from_s3()
            if my_bucket != None:
                my_bucket.Object(file_to_delete).delete()
            if file_extension in ['txt', 'pdf']:
                file_id_to_delete_from_db = TextLecture.query.filter(TextLecture.name==file_to_delete, TextLecture.lesson_id==lesson_id).first().id 
                try:
                    TextLecture.query.filter_by(id=file_id_to_delete_from_db).delete() 
                    db.session.commit()
                    return redirect(link)  
                except:
                    print('The file ' + file_to_delete + ' from ' + lesson + ' was not deleted')
                    return redirect(link)    
                return redirect(link) 
            elif file_extension in ['avi', 'mp4']:
                file_id_to_delete_from_db = Video.query.filter(Video.name==file_to_delete, Video.lesson_id==lesson_id).first().id 
                try:
                    Video.query.filter_by(id=file_id_to_delete_from_db).delete() 
                    db.session.commit()
                    return redirect(link)  
                except:
                    print('The file ' + file_to_delete + ' from ' + lesson + ' was not deleted')
                    return redirect(link)    
                return redirect(link) 
            elif file_extension in ['mp3']:
                file_id_to_delete_from_db = Audio.query.filter(Audio.name==file_to_delete, Audio.lesson_id==lesson_id).first().id 
                try:
                    Audio.query.filter_by(id=file_id_to_delete_from_db).delete() 
                    db.session.commit()
                    return redirect(link)  
                except:
                    print('The file ' + file_to_delete + ' from ' + lesson + ' was not deleted')
                    return redirect(link)    
                return redirect(link)  
            elif file_extension in ['png', 'jpg', 'jpeg', 'gif']:
                file_id_to_delete_from_db = Image.query.filter(Image.name==file_to_delete, Image.lesson_id==lesson_id).first().id 
                try:
                    Image.query.filter_by(id=file_id_to_delete_from_db).delete() 
                    db.session.commit()
                    return redirect(link)  
                except:
                    print('The file ' + file_to_delete + ' from ' + lesson + ' was not deleted')
                    return redirect(link)    
                return redirect(link)                             
        except: 
            return redirect(link)  
    else:
        return redirect(link)        
    return redirect(link) 
            