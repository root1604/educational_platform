<p>1. Пропишем в переменные данные для доступа к S3. <br><br>
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

<p>2. Создадим проект<br>
mkdir -p educational_platform/webapp<br>
cd educational_platform<br>
python3 -m venv env<br>
source env/bin/activate<br>
    For Windows:<br>
    env\Scripts\activate<br>
pip install flask boto3 flask-sqlalchemy<br></p>
<p>3. Configuration file config.py<br>
===========================================<br>
from datetime import timedelta<br>
import os<br>
<br>
basedir = os.path.abspath(os.path.dirname(__file__))<br>
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'YOUR_DATABASE_NAME')<br>
<br>
REMEMBER_COOKIE_DURATION = timedelta(days=1)<br>
SECRET_KEY = YOUR_RANDOMLY_GENERATED_SECRET_KEY<br>
S3_BUCKET = YOUR_BUCKET_NAME<br>
============================================<br><br>
<p>4. Запускаем приложение<br>
export FLASK_APP=webapp && export FLASK_ENV=development && flask run<br>
    For Windows:<br>
    set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run<br></p>
<p>5. Создадим в корне проекта файл (educational_platform/create_db.py) для создания базы данных<br>
Запустим файл create_db.py и убедимся, что база создалась<br>
python create_db.py<br></p>
