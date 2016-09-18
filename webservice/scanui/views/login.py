from scanui import login_manager
#from scanui.models import Users
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required

appmodule = Blueprint('loginui', __name__)

@appmodule.route('/cloudsafe', methods=['GET'])
def index():
    return redirect(url_for('loginui.login'))

'''
@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)
'''

@appmodule.route("/cloudsafe/login", methods=["GET", "POST"])
def login():
    if (request.method == 'POST' and 'username' in request.form and
       'password' in request.form):
        app_user = None
        username = request.form['username']
        password = request.form['password']
        if 'username' in request.form and len(request.form['username']):
            '''
            app_users = Users.find(username=username)
            if len(app_users) != 1:
                flash("login failed: check username and password")
                app_user = None
            else:
                app_user = app_users[0]
            '''
            #TODO check login auth
            pass
        #if app_user and app_user.credentials_valid(password):
        if True:
            #login_user(app_user)
            pass

    return render_template('/handleui/results.html')
    #return render_template("/handleui/login.html")

@appmodule.route("/cloudsafe/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('loginui.index'))
