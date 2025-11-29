from .init import app
from flask import render_template, url_for, redirect
from .forms import registro

@app.route('/')
@app.route('/home')
def home():
    print('Hello Autenticator')
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registro()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return redirect(url_for("home"))


