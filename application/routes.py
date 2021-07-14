
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
        list_of_things_to_do += '<br>'+ tasks.name + ' | '+tasks.completed
    return str(list_of_things_to_do)

@app.route('/update/<task_name>/<new_description>')
def update(task_name, new_description):
    current_entry = Todolist(name=task_name)
    current_entry.description = new_description
    db.session.commit()
    return 'you have updated the description for this task!\n' + f'description: {new_description}'

@app.route('/delete_task/<task_name>')
def delete_task(task_name):
    selected_task = task_name
    db.session.delete(selected_task)
    db.session.commit()
    return f'you have deleted task {selected_task}'

@app.route('/<task_name>/setto/<word>')
def setto(task_name, word):
    selected_task = Todolist(name=task_name)
    if word == 'completed':
        selected_task.done = True
        return f'You have marked {task_name} as completed'

    if word == 'incomplete':
        selected_task.done == False
        return f'You have marked {task_name} as incomplete. Get back to work!!!'

@app.route('/whatsdone/<word>')
def whatsdone(word):
    answer = ''
    if word == 'complete':
        completed = Todolist.query.filter_by(done=True).all()
        for task in completed:
            answer += '<br>' + task.name
        return answer
    if word == 'incomplete':
        incomplete = Todolist.query.fiter_by(done=False).all()
        for task in incomplete:
            answer += '<br>' + task.name
        return answer