from flask import Flask
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('users.db')
cur = con.cursor()
cur.execute('''CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL, 
                                email TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL)''')
cur.close()
con.close()


app.config['SECRET_KEY'] = '123456'


from Program import forms
from Program import routes
