from flask import Flask, json, request, make_response, jsonify, render_template, url_for, flash, redirect
from utopia.models.users import USER_SCHEMA
from utopia import app
from utopia.user_service import UserService
from utopia.models.users import User
from utopia.forms import RegistrationForm, LoginForm
from datetime import datetime, timedelta, timezone
from flask_bcrypt import Bcrypt

import logging

from flask_jwt_extended import create_access_token, unset_jwt_cookies, get_jwt, get_jwt_identity, set_access_cookies, get_current_user, JWTManager, jwt_required



USER_SERVICE = UserService()

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

##################### GET #####################

ADMIN = 1
AGENT = 2
TRAVELER = 3


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]

    user = USER_SERVICE.find_user_by_username(identity)
    user = USER_SCHEMA.dump(user)
    return user


@app.route('/users/admin/read/users', methods=['GET'])
@jwt_required()
def readUsers():
    current_user = get_current_user()
    if current_user['role_id'] != ADMIN:
        flash("Invalid authorization for this resource")
        return make_response()

    return USER_SERVICE.read_users()

@app.route('/users/admin/read/user/id=<id>', methods=['GET'])
@jwt_required()
def readUser(id):

    return USER_SERVICE.find_user(id)


@app.route('/users/admin/read/user/username=<username>', methods=['GET'])
@jwt_required()
def readUserUsername(username):

    return USER_SERVICE.find_user_by_username(username)


@app.route('/users/admin/read/users/role_id=<id>', methods=['GET'])
@jwt_required()
def readUserByRole(id):

    return USER_SERVICE.read_user_by_role(id)




##################### POST #####################

@app.route('/users/public/add/user', methods=['POST'])
def addUser():

    return USER_SERVICE.add_user(request.json)


@app.route('/users/admin/add/user_role', methods=['POST'])
@jwt_required()
def addUserRole():

    return USER_SERVICE.add_user_role(request.json)



##################### PUT #####################

@app.route('/users/public/update/user', methods=['PUT'])
@jwt_required()
def updateUser():

    return USER_SERVICE.update_user(request.json)


@app.route('/users/admin/update/user_role', methods=['PUT'])
@jwt_required()
def updateUserRole():

    return USER_SERVICE.update_user_role(request.json)


##################### DELETE #####################

@app.route('/users/public/delete/user/id=<id>', methods=['DELETE'])
@jwt_required()
def deleteUser(id):

    return USER_SERVICE.delete_user(id)


@app.route('/users/public/delete/user_role/id=<id>', methods=['DELETE'])
@jwt_required()
def deleteUserRole(id):

    return USER_SERVICE.delete_user_role(id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = USER_SERVICE.find_user_by_username(form.username.data)
        if user:
            flash('Registration Unsuccessful. Username already exists', 'danger')
            return render_template('register.html', title='Register', form=form)
        user = form.data
        user['role_id'] = TRAVELER

        USER_SERVICE.add_user(user)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    

    if form.validate_on_submit():

        if USER_SERVICE.login_user(form['username'].data, form['password'].data):


            flash('You have been logged in!', 'success')
            access_token = create_access_token(identity=form['username'].data)
            response = redirect(url_for('readUsers'))
            set_access_cookies(response, access_token)
  
            return response
        flash('Login Unsuccessful. Please check username and password', 'danger')

    elif request.method == 'POST':
        data = request.json
        if USER_SERVICE.login_user(data['username'], data['password']):
            access_token = create_access_token(identity=data['username'])
            response = make_response('Logged in as %s' %data['username'], 200)
            set_access_cookies(response, access_token)
            return response
        return make_response('Invalid credentials', 401)
            
    return render_template('login.html', title='Login', form=form)





@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response



@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):

        # Case where there is not a valid JWT. Just return the original respone
        return response



    # if request.method == 'POST':
    #     token = USER_SERVICE.login_user(request.json)
    #     if token:
    #         return "token"
    #     else:
    #         return render_template("login.html", credentials=False)
        
    # return render_template("login.html")