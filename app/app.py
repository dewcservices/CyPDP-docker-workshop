import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
db = os.getenv('MYSQL_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:3306/{db}'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

@app.route('/')
def home():
    db.create_all()
    todo_list = Todo.query.all()
    return render_template('home.html', todo_list=todo_list)

@app.post('/add')
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/update/<int:todo_id>')
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('home'))

@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))
