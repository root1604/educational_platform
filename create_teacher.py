from getpass import getpass
import sys

from webapp import create_app
from webapp.model import User, db

app = create_app()
        
with app.app_context():
    username = input('Username: ')

    if User.query.filter(User.username == username).count():
        print('Username ' + username + ' already exists')
        sys.exit(0)

    password = getpass('Password: ')
    password2 = getpass('Retype the password: ')
    if not password == password2:
        sys.exit(0)
    new_user = User(username=username, role='teacher')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))
