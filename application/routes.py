from flask import redirect, url_for
from application import app, db
from application.models import Todolist

# As a user, I want to add a new todo task, so I know I have a task to be completed (no description)
# As a user, I want to view my todo tasks, so that I know what I need to do
# As a user, I want to change the description of the task, so I can update its contents after creating it
# As a user, I want to delete a task, in case I don't need to do that task anymore	
# As a user, I want to set a todo task as completed, so I know which tasks I've already done
# As a user, I want to set a todo task as incomplete, in case a complete task still needs doing

@app.route('/addtask/<task>')
def addtask(task):
    new_task = Todolist(name=task)
    db.session.add(new_task)
    db.session.commit()
    return f'You have added {task} to your list'

@app.route('/home')
def home():
    all_tasks = Todolist.query.all()
    list_of_things_to_do = ""
    for tasks in all_tasks:
        list_of_things_to_do += f'{tasks.id} | {tasks.name} | {tasks.description} | {tasks.done}<br>'
    return str(list_of_things_to_do)

@app.route('/update/<int:id>/<new_description>')
def update(id, new_description):
    current_entry = Todolist.query.get(id)
    current_entry.description = new_description
    db.session.add(current_entry)
    db.session.commit()
    return f'you have updated the description for this task!<br>description: {new_description}'

@app.route('/delete_task/<int:id>')
def delete_task(id):
    selected_task = Todolist.query.get(id)
    db.session.delete(selected_task)
    db.session.commit()
    return f'you have deleted task {selected_task.name}'

@app.route('/completed/<int:id>')
def completed(id):
    selected_task = Todolist.query.get(id)
    selected_task.done = True
    db.session.add(selected_task)
    db.session.commit()
    return f'you have marked {selected_task.name} as completed'

@app.route('/incomplete/<int:id>')
def incomplete(id):
    selected_task = Todolist.query.get(id)
    selected_task.done = False
    db.session.add(selected_task)
    db.session.commit()
    return f'you have marked {selected_task.name} as incomplete'
