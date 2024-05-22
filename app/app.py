from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

todo_list = {}
id_val = 0

@app.route('/')
def home():
    global todo_list
    return render_template('home.html', todo_list=todo_list)

@app.post('/add')
def add():
    title = request.form.get('title')
    global id_val, todo_list
    new_todo = {'title':title, 'completed':False, 'id':id_val}
    print(todo_list)
    todo_list[id_val] = new_todo
    print(todo_list)
    id_val += 1
    return redirect(url_for('home'))

@app.get('/update/<int:todo_id>')
def update(todo_id):
    todo = todo_list[todo_id]
    todo['completed'] = not todo['completed']
    return redirect(url_for('home'))

@app.get('/delete/<int:todo_id>')
def delete(todo_id):
    del todo_list[todo_id]
    return redirect(url_for('home'))
