<p>1. Set credentials for access AWS S3 bucket. <br><br>
~/.aws/credentials <br>
=========================================<br>
[default]<br>
aws_access_key_id = YOUR_ACCESS_KEY<br>
aws_secret_access_key = YOUR_SECRET_KEY<br>
=========================================<br><br></p>

<p>~/.aws/config:<br>
==========================================<br>
[default]<br>
region=eu-north-1<br>
==========================================<br></p>

<p>2. Create project<br>
mkdir -p educational_platform/webapp<br>
cd educational_platform<br>
python3 -m venv env<br>
source env/bin/activate<br>
    For Windows:<br>
    env\Scripts\activate<br>
pip install -r requirements.txt<br></p>
<p>3. Configuration file config.py<br>
===========================================<br>
from datetime import timedelta<br>
import os<br>
<br>
basedir = os.path.abspath(os.path.dirname(__file__))<br>
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'YOUR_DATABASE_NAME')<br>
SQLALCHEMY_TRACK_MODIFICATIONS = False<br>
<br>
REMEMBER_COOKIE_DURATION = timedelta(days=1)<br>
SECRET_KEY = YOUR_RANDOMLY_GENERATED_SECRET_KEY<br>
S3_BUCKET = YOUR_BUCKET_NAME<br>
============================================<br><br>
<p>4. Start application<br>
export FLASK_APP=webapp && export FLASK_ENV=development && flask run<br>
    For Windows:<br>
    set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run<br></p>
<p>5. Create file at the root of the project (educational_platform/create_db.py) for create database<br>
Run create_db.py and make sure database was created<br>
python create_db.py<br></p>
<p>6. Enabling migrations mechamism.<br>
Linux & Mac: export FLASK_APP=webapp && flask db init<br>
Windows: set FLASK_APP=webapp && flask db init<br>
After doing changes in the models of db execute<br>
export FLASK_APP=webapp && flask db migrate -m "comment"<br>
flask db upgrade<br>
