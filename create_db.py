from webapp import create_app
from webapp.db.db import db

db.create_all(app=create_app())
