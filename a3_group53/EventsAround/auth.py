from flask import Blueprint, render_template, request,redirect,url_for,flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from . import db

#blueprint
bp = Blueprint('auth', __name__ )

@bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    if (register.validate_on_submit() == True)
            uname =register.user_name.data
            pwd = register.password.data
            email=register.email_id.data
            u1 = User.query.filter_by(name=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            pwd_hash = generate_password_hash(pwd)
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=register, heading='Register')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password_hash, password): 
            error='Incorrect password'
        if error is None:
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))