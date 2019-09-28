from alayatodo import app, db
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash # Message flashing will be used for invalid input
    )

from alayatodo.models import User, Todo


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        #readme = "".join(l.decode('utf-8') for l in f)
        readme = "".join(l for l in f) # str object is already decoded, drop utf-8
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    # Authenticate
    if not session.get('logged_in'):
        return redirect('/login')
    # Pull all todos from db
    todos = Todo.query

    # Paginate todos
    # page = request.args.get('page', 1, type=int)
    # todos_paginated = todos.paginate(page, app.config['TODOS_PER_PAGE'], False)

    # return the html page and make the todos var accessible
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    # Redirect with flash if no description entered.
    if request.form.get('description') == '':
        flash('Please enter a description of your task.')
        return redirect('/todo')
    # Insert into db and redirect if description given.
    else:
        todo = Todo(user_id = session['user']['id'], description = request.form.get('description'))
        db.session.add(todo)
        db.session.commit
        flash('Your task has been added to the list.')
        return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash('Your task has been deleted.')
    return redirect('/todo')
