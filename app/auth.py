from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models import User
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('todos.index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if not username or not email or not password:
            flash('Tous les champs sont obligatoires.', 'error')
            return render_template('auth/register.html')

        if password != confirm:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('auth/register.html')

        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'error')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'error')
            return render_template('auth/register.html')

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès. Connectez-vous.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todos.index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')

        if not username or not password:
            flash('Nom d\'utilisateur et mot de passe requis.', 'error')
            return render_template('auth/login.html')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Bienvenue !', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('todos.index'))
        flash('Identifiants incorrects.', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))
