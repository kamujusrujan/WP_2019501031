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
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://birawtnmsapodw:678f377d616ec505fb180996a6ecab8f3a3aaa51e47ab7719590df97ce7872ae@ec2-18-233-32-61.compute-1.amazonaws.com:5432/dad3mt6v6b5qe4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)

def upload():
	
	# db.drop_all()
	# db.create_all()
	# db.session.commit()

	data = open('books.csv','rt')
	data = list(csv.reader(data))
	for a in tqdm(data[1:]):
		# print(a[0], a[1] ,a[2] ,int(a[3]))
		db.session.add( Book(isbn = a[0] , title = a[1] ,author = a[2] ,  year = int(a[3]) ))
	print('added')
	db.session.commit()


class Book(db.Model):
	__tablename__ = 'Books'
	isbn = db.Column(db.String, primary_key = True)
	title = db.Column(db.String)
	year = db.Column(db.Integer)
	author = db.Column(db.String)

if __name__ == "__main__":
	upload()