from apps.home import blueprint
from flask import render_template, request,redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import InfoUser,ImageUser,ImageUsercover
from flask_login import current_user
import pandas as pd
import os

csv=pd.read_csv("movie.csv")
csv=csv.head(100)
def decode_picture(data):
    decodepic=data.decode('ascii')
    return decodepic

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
def selec_useravatar():
    user = ImageUser.query.filter_by(username=current_user.username).first()
    if user:
        
        return 'data:image/{};base64,{}'.format((user.formato).lower(),user.avatar)
    else:
        
         
        return "/static/assets/img/team/profile-picture-3.jpg"
def selec_usercover():
    user = ImageUsercover.query.filter_by(username=current_user.username).first()
    if user:
        
        return 'data:image/{};base64,{}'.format((user.formato).lower(),user.cover)
    else:
        
         
        return "/static/assets/img/profile-cover.jpg"
        
@blueprint.route('/')
def route_default():
    return redirect('/index')

@blueprint.route('/index')

def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
      
        
        return render_template("home/" + template, segment=segment,info=selec_userinf(),infoimage=selec_useravatar(),infocover=selec_usercover(), column_names = csv.columns.values, row_data = list(csv.values.tolist()),
   link_column = "Patient ID", zip = zip)
        

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
