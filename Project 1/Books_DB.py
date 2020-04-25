from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from tqdm import tqdm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)

def upload():
	
	# db.drop_all()
	db.create_all()
	db.session.commit()

	data = open('books.csv','rt')
	data = list(csv.reader(data))
	for a in tqdm(data[1:]):
		db.session.add( Book(isbn = a[0] , title = a[1] ,author = a[2] ,  year = int(a[3]) ))
	db.session.commit()


class Book(db.Model):
	__tablename__ = 'Books'
	isbn = db.Column(db.String, primary_key = True)
	title = db.Column(db.String)
	year = db.Column(db.Integer)
	author = db.Column(db.String)

if __name__ == "__main__":
	upload()