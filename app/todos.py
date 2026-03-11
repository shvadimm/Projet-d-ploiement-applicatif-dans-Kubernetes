from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Todo

todos_bp = Blueprint('todos', __name__)


@todos_bp.route('/')
def index():
    if current_user.is_authenticated:
        todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.desc()).all()
        return render_template('todos/index.html', todos=todos)
    return render_template('todos/landing.html')


@todos_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Le titre est obligatoire.', 'error')
        return redirect(url_for('todos.index'))
    todo = Todo(title=title, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    flash('Tâche ajoutée.', 'success')
    return redirect(url_for('todos.index'))


@todos_bp.route('/toggle/<int:todo_id>', methods=['POST'])
@login_required
def toggle(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash('Accès refusé.', 'error')
        return redirect(url_for('todos.index'))
    todo.completed = not todo.completed
    db.session.commit()
    flash('Tâche mise à jour.', 'success')
    return redirect(url_for('todos.index'))


@todos_bp.route('/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash('Accès refusé.', 'error')
        return redirect(url_for('todos.index'))
    db.session.delete(todo)
    db.session.commit()
    flash('Tâche supprimée.', 'success')
    return redirect(url_for('todos.index'))
