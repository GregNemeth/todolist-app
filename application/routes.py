from flask.templating import render_template
from application.forms import TaskForm
from flask import redirect, url_for, request
from application import app, db
from application.models import Tasks

    # As a user, I want to view all my todo tasks on the home page of the application, so that I can know what tasks still need completing as soon as I navigate to the website
	# As a user, I want to view all my completed todo tasks from the web page, so I can see how much I've achieved
	# As a user, I want to add a new todo task with a description using a web form, so I can keep track of things I need to do via a GUI
	# As a user, I want to change the description of the task using a web form, so I can update its contents after creating it via a GUI
	# As a user, I want to delete a task with a click of a button, so that I can quickly and easily delete a task


@app.route('/')
def home():
    alltasks = Tasks.query.all()
    
        

    return render_template("home.html", alltasks=alltasks)

@app.route('/create', methods=["GET", "POST"])
def create():
    form = TaskForm()

    if request.method == 'POST':
        new_task = Tasks(name=form.name.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('create.html', form=form)
        
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    current_entry = Tasks.query.get(id)
    form = TaskForm()
    
    if request.method == 'POST':
        current_entry.name = form.name.data
        db.session.add(current_entry)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        return render_template('create.html', form=form)

@app.route('/delete_task/<int:id>')
def delete_task(id):
    selected_task = Tasks.query.get(id)
    db.session.delete(selected_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/completed/<int:id>')
def completed(id):
    selected_task = Tasks.query.get(id)
    selected_task.done = True
    db.session.add(selected_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/incomplete/<int:id>')
def incomplete(id):
    selected_task = Tasks.query.get(id)
    selected_task.done = False
    db.session.add(selected_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/donedem')
def donedem():
    all_tasks_done = Tasks.query.filter_by(done=True).all()
    
    return render_template("alldone.html", alltasks=all_tasks_done)