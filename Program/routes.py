from .init import app
from flask import render_template, url_for, redirect

@app.route('/')
@app.route('/home')
def home():
    print('Hello Autenticator')
    return render_template("home.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return redirect(url_for("home"))


