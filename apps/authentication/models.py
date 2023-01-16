
from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

import base64



class InfoUser(db.Model):
    
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    frist_name    = db.Column(db.String(128), unique=True)
    last_name     = db.Column(db.String(128), unique=True)
    birthday      = db.Column(db.String(64), unique=True)
    gender        = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(128), unique=True)
    phone         = db.Column(db.BIGINT, unique=True)
    
    
    
class ImageUser(db.Model):
    
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    avatar        = db.Column(db.Text, nullable=False)
    formato       = db.Column(db.String(64), unique=True) 


class ImageUsercover(db.Model):
    
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    cover         = db.Column(db.Text, nullable=False)
    formato       = db.Column(db.String(64), unique=True) 
    
class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)

   

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username) 



@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

    
class ejemplo(db.Model):
    id          =   db.Column(db.Integer, primary_key=True)
    nombres     =   db.Column(db.String(128))
    apellidos   =   db.Column(db.String(128))