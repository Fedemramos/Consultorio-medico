from flask import Blueprint, render_template, request, redirect, url_for,flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .extensions import db

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash('Complete correctamente los campos solicitados.', 'error')
            return render_template('register.html')

        if not password:
            flash('Complete correctamente los campos solicitados.', 'error')
            return render_template('register.html')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return render_template('login.html')

        new_user = User(username=username, password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        #validar datos
        user = User.query.filter_by(username = username).first()
        
        if user is None or not check_password_hash(user.password, password):
            error = "Usuario o contraseña incorrecta"

        #iniciar sesion
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('views.pacientes'))
        
        flash(error)
    
    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view