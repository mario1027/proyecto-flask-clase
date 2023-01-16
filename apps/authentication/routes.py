
from flask import render_template, redirect, request, url_for
import pathlib
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from apps.authentication.util import hash_pass
from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users,InfoUser,ImageUser,ImageUsercover, ejemplo

from apps.authentication.util import verify_pass

import base64


# Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect('/tabla_pelis.html')

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Sabemos que te encanta ese nombre de usuario pero ya existe.',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='El correo electrónico ya ha sido registrado registrado',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/infouser', methods=['GET', 'POST'])
def submitinfouser():
    username      = current_user.username
    first_name    = str(request.form["first_name"])
    last_name     = str(request.form["last_name"])
    birthday      = str(request.form["birthday"])
    gender        = str(request.form["gender"])
    email         = str(request.form["email"])
    phone         = int(request.form["phone"])

    cond=InfoUser.query.filter_by(username=username).first() 
    if cond:
        cond.username=username
        cond.frist_name=first_name
        cond.last_name=last_name
        cond.birthday=birthday
        cond.gender=gender
        cond.email=email
        cond.phone=phone
    else:     
        info=InfoUser(username=username,
                  frist_name=first_name,
                  last_name=last_name,
                  birthday=birthday,
                  gender=gender,
                  email=email,
                  phone=phone)
        db.session.add(info)
    db.session.commit()
    return redirect("/settings.html")
    
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/moduser', methods=['GET', 'POST'])
def submitmoduser():
    username = request.form['username']
    cond=InfoUser.query.filter_by(username=current_user.username).first()
    if cond:
        cond.username=username
    user = Users.query.filter_by(username=current_user.username).first()
    user1 = ImageUser.query.filter_by(username=current_user.username).first()
    if user1:
        user1.username=username
    user2 = ImageUsercover.query.filter_by(username=current_user.username).first()
    if user2:
        user2.username=username
    user.username=username
   
    

    db.session.commit()
    return redirect("/settings.html")

@blueprint.route('/modpassword', methods=['GET', 'POST'])
def submitmodpass():
    password = request.form['password']
    user = Users.query.filter_by(username=current_user.username).first()
    user.password=hash_pass(password)
    db.session.commit()
    return redirect("/settings.html")
# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

def selec_userinf():
    user = InfoUser.query.filter_by(username=current_user.username).first()
    if user:
        return user
    else:
        user={}
        user["frist_name"]=current_user.username
        user["last_name"]=""
        user["birthday"]=""
        user["gender"]=""
        user["email"]=""
        user["phone"]=""
        return user
@blueprint.route("/deleteuser", methods=['GET', 'POST'])        
def deleteuser():
    user = Users.query.filter_by(username=current_user.username).first()
    user1 = InfoUser.query.filter_by(username=current_user.username).first()
    user2=ImageUser.query.filter_by(username=current_user.username).first()
    db.session.delete(user)
    if user1:
        db.session.delete(user1)
    if user2:
        db.session.delete(user2)
    db.session.commit()
    logout_user
    return redirect(url_for('home_blueprint.index'))    
def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic 
def decode_picture(data):
    decodepic=data.decode('ascii')
    return decodepic
@blueprint.route("/regisuserimage", methods=['GET', 'POST'])
def registrarimagenuser():
    file = request.files['avatar']
    ext = pathlib.Path(file.filename).suffix
    if ext=="":
        None
    else:
        ext=ext.replace('.', '')
        data = file.read()
        avatar= render_picture(data)
        username = current_user.username
        user1 = ImageUser.query.filter_by(username=current_user.username).first()
        if user1:
            user1.avatar=avatar
            user1.formato=ext
        else:
            user=ImageUser(avatar=avatar,username=username,formato=ext)
            db.session.add(user)
        db.session.commit()
  

    return redirect("/settings.html")  

@blueprint.route("/deleimageperfil", methods=['GET', 'POST'])
def deleteimageperfil():
    user=ImageUser.query.filter_by(username=current_user.username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect("/settings.html")
@blueprint.route("/regisimagencover", methods=['GET', 'POST'])   
def registrarimagencover():
    file = request.files['cover']
    ext = pathlib.Path(file.filename).suffix
    if ext=="":
        None
    else:
        ext=ext.replace('.', '')
        data = file.read()
        cover= render_picture(data)
        username = current_user.username
        user1 = ImageUsercover.query.filter_by(username=current_user.username).first()
        if user1:
            user1.cover=cover
            user1.formato=ext
        else:
            user=ImageUsercover(cover=cover,username=username,formato=ext)
            db.session.add(user)
        db.session.commit()   
    return redirect("/settings.html") 

@blueprint.route('/formularioresp', methods=['GET', 'POST'])
def formulariorespuesta():
    nombres       =   request.form["nombres"]
    apellidos     =   request.form["apellidos"]
    data=ejemplo(nombres=nombres,apellidos=apellidos)
    db.session.add(data)
    db.session.commit()
    return render_template('home/mensaje.html',msg="Los datos se han guardado con exito")

