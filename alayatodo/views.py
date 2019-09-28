from alayatodo import app, db, login
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash # Message flashing will be used for invalid input
    )
from flask_login import (
    current_user, 
    login_user, 
    logout_user, 
    login_required
    )
from werkzeug.urls import url_parse
from datetime import datetime
from alayatodo.models import User, Todo

# Load current_user
@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        #readme = "".join(l.decode('utf-8') for l in f)
        readme = "".join(l for l in f) # str object is already decoded, drop utf-8
        return render_template('index.html', readme=readme)

### AUTHENTICATION
### LOGIN
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    # A logged-in user cannot view the login page
    if current_user.is_authenticated:
        return redirect('/todo')

    # Set form data vars
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None: #or not user.password != password:
        flash('These credentials are invalid. Please try again.')
        return redirect('/login')
    login_user(user)
    return redirect('/todo')


### LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
# Authenticate
@login_required
def todos():
    # Paginate todos
    page = request.args.get('page', 1, type=int)
    todos = current_user.todos.order_by(
        Todo.timestamp.desc()).paginate(page, 5, False)

    next_url = url_for('todos', page=todos.next_num) \
        if todos.has_next else None
    prev_url = url_for('todos', page=todos.prev_num) \
        if todos.has_prev else None

    # return the html page and make the todos var accessible
    return render_template(
        'todos.html', 
        todos=todos.items,
        next_url=next_url,
        prev_url=prev_url
        )


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
# Authenticate
@login_required
def todos_POST():
    # Redirect with flash if no description entered.
    if request.form.get('description') == '':
        flash('Please enter a description of your task.')
        return redirect('/todo')
    # Insert into db and redirect if description given.
    else:
        todo = Todo(
            user_id=current_user.id, 
            description=request.form.get('description')
            )
        db.session.add(todo)
        db.session.commit()
        flash('Your task has been added to the list.')
        return redirect('/todo')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo/<id>', methods=['POST'])
# Authenticate
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash('Your task has been deleted.')
    return redirect('/todo')
