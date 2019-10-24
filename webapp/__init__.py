from flask import flash, Flask
from flask_login import current_user, LoginManager,  login_required
from webapp.admin.views import blueprint as admin_blueprint
from webapp.category.models import Category
from webapp.category.views import blueprint as category_blueprint
from webapp.content.models import Audio, Image, TextLecture, Video
from webapp.course.models import Course
from webapp.course.views import blueprint as course_blueprint
from webapp.s3.filters import file_type
from webapp.s3.filters import create_presigned_url
from webapp.homepage.views import blueprint as homepage_blueprint
from webapp.lesson.models import Lesson
from webapp.lesson.views import blueprint as lesson_blueprint
from webapp.login.models import User
from webapp.login.views import blueprint as login_blueprint
from webapp.db.db import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(homepage_blueprint)
    app.register_blueprint(lesson_blueprint)
    app.register_blueprint(login_blueprint)

    app.jinja_env.filters['file_type'] = file_type
    app.jinja_env.filters['create_presigned_url'] = create_presigned_url

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
 
    return app
