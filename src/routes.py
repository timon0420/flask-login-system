from src import app, db, csrf, bcrypt
from flask import render_template, redirect
from src.models import User
from src.form import RegistrationForm, LoginForm
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

@app.route('/userpage')
def userpage():
    try: 
        return render_template('userpage.html', name=current_user.name)
    except Exception as e:
        return f'<h1>{e}</h1>'

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')