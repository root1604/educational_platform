import boto3
from flask import Flask, render_template, request, redirect, Response
from werkzeug.utils import secure_filename
from webapp.upload_file_to_s3 import upload_file_to_s3
from webapp.filters import file_type
from webapp.filters import create_presigned_url
from webapp.model import db, Category, Course, Lesson, Video, Image, TextLecture
from sqlalchemy import exc

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'avi', 'mp4', 'mp3'])

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.jinja_env.filters['file_type'] = file_type
    app.jinja_env.filters['create_presigned_url'] = create_presigned_url

    bucket = app.config["S3_BUCKET"]

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if "user_file" not in request.files:
                return "No user_file key in request.files"
            file = request.files["user_file"]
            if file.filename == "":
                return "Please select a file"
            if file and allowed_file(file.filename):
                file.filename = secure_filename(file.filename)
                upload_file_to_s3(file, bucket)
                my_bucket = get_bucket_from_s3()
                if my_bucket == None:
                    return render_template('error.html') 
                else:
                    categories = Category.query.all()
                    summaries = my_bucket.objects.all()
                    return render_template('index.html', files=summaries, categories=categories)
            else:
                return redirect("/")    
        else:
            my_bucket = get_bucket_from_s3()
            if my_bucket == None:
                return render_template('error.html') 
            else:  
                categories = Category.query.all()  
                summaries = my_bucket.objects.all()
                return render_template('index.html', files=summaries, categories=categories)
    
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
        key = request.form['key']
        my_bucket = get_bucket_from_s3()
        if my_bucket != None:
            my_bucket.Object(key).delete()
        return redirect('/')

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

    @app.route('/<category_name>', methods=['GET', 'POST'])
    def page(category_name):
        category_exists = Category.query.filter_by(name=category_name).first()
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
                return redirect('/'+category_name) 
            else:
                courses = Course.query.filter(Course.category_id==category_exists.id).all()    
                return render_template('category.html', category_name=category_name, courses=courses)  
        else:
            return render_template('error.html')     

    return app
    # if __name__ == "__main__":
    #     app.run()
