from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import datetime, date
from app.extensions import db
from app.models import Todo

todos_bp = Blueprint('todos', __name__)


def _get_todos_query(filter_type='all', sort_by='created_at', sort_order='desc'):
    """Retourne la requête filtrée et triée des todos de l'utilisateur."""
    q = Todo.query.filter_by(user_id=current_user.id)
    if filter_type == 'active':
        q = q.filter_by(completed=False)
    elif filter_type == 'completed':
        q = q.filter_by(completed=True)
    # Tri (priority trié en Python)
    if sort_by != 'priority':
        order_col = getattr(Todo, sort_by, Todo.created_at)
        if sort_order == 'desc':
            q = q.order_by(order_col.desc())
        else:
            q = q.order_by(order_col.asc())
    return q


@todos_bp.route('/')
def index():
    if current_user.is_authenticated:
        filter_type = request.args.get('filter', 'all')
        sort_by = request.args.get('sort', 'created_at')
        sort_order = request.args.get('order', 'desc')
        if sort_by not in ('created_at', 'due_date', 'priority', 'title'):
            sort_by = 'created_at'
        if sort_order not in ('asc', 'desc'):
            sort_order = 'desc'
        todos = _get_todos_query(filter_type, sort_by, sort_order).all()
        # Ordre des priorités pour le tri
        priority_order = {p: i for i, p in enumerate(Todo.PRIORITIES)}
        if sort_by == 'priority':
            todos = sorted(todos, key=lambda t: priority_order.get(t.priority or 'medium', 1),
                          reverse=(sort_order == 'desc'))
        return render_template('todos/index.html', todos=todos, filter_type=filter_type,
                              sort_by=sort_by, sort_order=sort_order)
    return render_template('todos/landing.html')


@todos_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Le titre est obligatoire.', 'error')
        return redirect(url_for('todos.index'))
    description = request.form.get('description', '').strip() or None
    priority = request.form.get('priority', 'medium')
    if priority not in Todo.PRIORITIES:
        priority = 'medium'
    due_date_str = request.form.get('due_date', '').strip() or None
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    todo = Todo(title=title, description=description, priority=priority, due_date=due_date, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    flash('Tâche ajoutée.', 'success')
    return redirect(url_for('todos.index'))


@todos_bp.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        flash('Accès refusé.', 'error')
        return redirect(url_for('todos.index'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Le titre est obligatoire.', 'error')
            return redirect(url_for('todos.edit', todo_id=todo_id))
        todo.title = title
        todo.description = request.form.get('description', '').strip() or None
        todo.priority = request.form.get('priority', 'medium')
        if todo.priority not in Todo.PRIORITIES:
            todo.priority = 'medium'
        due_date_str = request.form.get('due_date', '').strip() or None
        todo.due_date = None
        if due_date_str:
            try:
                todo.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        db.session.commit()
        flash('Tâche modifiée.', 'success')
        return redirect(url_for('todos.index'))
    return render_template('todos/edit.html', todo=todo)


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
    return redirect(request.referrer or url_for('todos.index'))


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
    return redirect(request.referrer or url_for('todos.index'))
