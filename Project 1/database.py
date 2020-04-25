from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
class User(db.Model):
	__tablename__ = 'registeredUsers'
	mail = db.Column(db.String,primary_key = True)
	name = db.Column(db.String)
	password = db.Column(db.String)
	created_data  = db.Column(db.DateTime, default = datetime.datetime.utcnow)
	user_ratings = db.relationship('Ratings', lazy='select',backref= "rating_users" )

class Book(db.Model):
	__tablename__ = "Books"
	isbn = db.Column(db.String,primary_key = True )
	title = db.Column(db.String)
	year = db.Column(db.Integer)
	author = db.Column(db.String)
	book_ratings = db.relationship('Ratings', lazy='select',backref= "rating_book" )
	

class Ratings(db.Model):
    __tablename__ = "Ratings"
    isbn = db.Column(db.String,db.ForeignKey('Books.isbn'),primary_key = True)
    mail = db.Column(db.String, db.ForeignKey('registeredUsers.mail'), primary_key = True)
    star = db.Column(db.Float)
    description = db.Column(db.String)
