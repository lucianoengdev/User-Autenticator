from .init import app, db, login_manager
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from .forms import registro
from .models import User



@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registro()
    if form.validate_on_submit():

        if db.session.query(User).filter_by(email=form.email.data).first():
            flash("Esse email já existe!")
            return render_template("register.html", form=form)
        
        user_to_create = User(name = form.name.data,
                              email = form.email.data,
                              password = form.password1.data
        )

        db.session.add(user_to_create)
        db.session.commit()
        db.create_all()
        
         
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        user_data = User.query.filter_by(email=user_email).first()
        if user_data and user_data.password == user_password:
            login_user(user_data)
            flash('Você está logado!')
            return redirect(url_for('home'))
        else:
            flash('Login inválido ou senha incorreta')     
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    return redirect(url_for("login"))


