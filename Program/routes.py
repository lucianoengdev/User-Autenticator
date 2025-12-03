from .init import app, db
from flask import render_template, url_for, redirect, flash
from .forms import registro
from .models import User

@app.route('/')
@app.route('/home')
def home():
    print('Hello Autenticator')
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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return redirect(url_for("home"))


