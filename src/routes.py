from src import app, db, csrf, bcrypt
from flask import render_template, redirect
from src.models import User, Task
from src.form import RegistrationForm, LoginForm, TaskForm
from flask_login import login_user, login_required, logout_user, current_user
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=name, surname=surname, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return redirect('/')
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect('/userpage')
    return render_template('login.html', form=form)

@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    try: 
        form = TaskForm()
        if form.validate_on_submit():
            title = form.title.data
            task = form.content.data
            new_task = Task(user_id=current_user.id, title=title, task=task)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/userpage')
            except Exception as e:
                return f'<h1>{e}</h1>'
        return render_template('userpage.html', user=current_user, form=form, Task=Task)
    except Exception as e:
        return f'<h1>{e}</h1>'

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try: 
        task = Task.query.filter_by(id=id, user_id=current_user.id).first()
        db.session.delete(task)
        db.session.commit()
        return redirect('/userpage')
    except:
        return redirect('/userpage')