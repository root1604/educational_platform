import boto3
from flask import Flask, render_template, request, redirect, Response
from werkzeug.utils import secure_filename
from webapp.upload_file_to_s3 import upload_file_to_s3
from webapp.filters import file_type
from webapp.filters import create_presigned_url
from webapp.model import db, Category, Course, Lesson, Video, Image, TextLecture, Audio
from sqlalchemy import exc

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'avi', 'mp4', 'mp3'])
ALLOWED_VIDEO_FILETYPES = set(['video/x-msvideo', 'video/mp4'])
ALLOWED_AUDIO_FILETYPES = set(['audio/mpeg'])
ALLOWED_IMAGE_FILETYPES = set(['image/png', 'image/jpeg', 'image/gif'])
ALLOWED_TEXT_FILETYPES = set(['text/plain', 'application/pdf'])

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.jinja_env.filters['file_type'] = file_type
    app.jinja_env.filters['create_presigned_url'] = create_presigned_url
    
    bucket = app.config["S3_BUCKET"]

    @app.route('/', methods=['GET'])
    def index():
        categories = Category.query.all()  
        return render_template('index.html', categories=categories)
    
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def get_bucket_from_s3():
        try:
            s3 = boto3.resource('s3')
            my_bucket = s3.Bucket(bucket)
            return my_bucket
        except:
            return None    

    @app.route('/delete', methods=['POST'])
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
        return redirect(link)          

    @app.route('/download', methods=['POST'])
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

    @app.route('/categories', methods=['POST'])
    def add_a_category():
        try:
            name = request.form['category']
            new_category = Category(name)
            if new_category.name != '':
                db.session.add(new_category)
                db.session.commit()
        except(exc.IntegrityError):
            print('the category exists')
            return redirect('/')     
        return redirect('/')  

    @app.route('/delete_a_category', methods=['POST'])
    def delete_a_category():
        try:
            category_id = request.form['category_id']
            Category.query.filter_by(id=category_id).delete() 
            db.session.commit()
        except:
            return redirect('/')    
        return redirect('/') 

    @app.route('/<link_path>', methods=['GET', 'POST'])
    def page(link_path):
        category_exists = Category.query.filter_by(name=link_path).first()
        if category_exists:
            if request.method == 'POST':
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
                courses = Course.query.filter(Course.category_id==category_exists.id).all()    
                return render_template('category.html', category_name=link_path, courses=courses)  
        else:
            return render_template('error.html')         
    
    @app.route('/<category_name>/<course_name>', methods=['GET', 'POST'])
    def course_page(category_name, course_name):
        category_exists = Category.query.filter_by(name=category_name).first()
        if category_exists:
            course_exists = Course.query.filter(Course.name==course_name, Course.category_id==category_exists.id).first() 
            if course_exists:
                if request.method == 'POST':
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
                    lessons = Lesson.query.filter(Lesson.course_id==course_exists.id).all()   
                    return render_template('course.html', category_name=category_name, course_name=course_name, lessons=lessons) 
            else:
                return render_template('error.html')    
        else:
            return render_template('error.html')         

    @app.route('/<category_name>/<course_name>/<lesson_name>', methods=['GET', 'POST'])
    def lesson_page(category_name, course_name, lesson_name):
        category_exists = Category.query.filter_by(name=category_name).first()
        if category_exists:
            course_exists = Course.query.filter(Course.name==course_name, Course.category_id==category_exists.id).first() 
            if course_exists:
                lesson_exists = Lesson.query.filter(Lesson.name==lesson_name, Lesson.course_id==course_exists.id).first()
                if lesson_exists:
                    if request.method == 'POST':
                        if "user_file" not in request.files:
                            return "No user_file key in request.files"
                        file = request.files["user_file"]
                        if file.filename == "":
                            return "Please select a file"
                        if file and allowed_file(file.filename):
                            file.filename = secure_filename(file.filename)
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
                        return render_template('lesson.html', category_name=category_name, course_name=course_name, lesson_name=lesson_name, files=summaries)
                else:
                    return render_template('error.html')     
            else:
                return render_template('error.html')    
        else:
            return render_template('error.html')   

    @app.route('/delete_a_course', methods=['POST'])
    def delete_a_course():
        course_id = request.form['course_id']
        course_for_delete=Course.query.filter_by(id=course_id).first()
        category_name=course_for_delete.category.name
        try:        
            Course.query.filter_by(id=course_id).delete() 
            db.session.commit()
        except:
            return redirect('/'+category_name)    
        return redirect('/'+category_name) 

    @app.route('/delete_a_lesson', methods=['POST'])
    def delete_a_lesson():
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

    return app