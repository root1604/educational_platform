<p>1. Пропишем в переменные данные для доступа к S3. <br><br>
~/.aws/credentials <br>
=========================================<br>
[default]<br>
aws_access_key_id = YOUR_ACCESS_KEY<br>
aws_secret_access_key = YOUR_SECRET_KEY<br>
=========================================<br><br>

 <p>~/.aws/config:<br>
==========================================<br>
[default]<br>
region=eu-north-1<br>
==========================================<br>
</p>
2. Создадим проект<br>
mkdir -p educational_platform/webapp<br>
cd educational_platform<br>
python3 -m venv env<br>
source env/bin/activate<br>
pip install flask boto3<br>
3. Файлы приложения создаем в папке webapp<br>
__init__.py<br>
config.py<br>
templates/index.html<br>
upload_file_to_s3.py<br>
4. Запускаем приложение<br>
export FLASK_APP=webapp && export FLASK_ENV=development && flask run</p>

