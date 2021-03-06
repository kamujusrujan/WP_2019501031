import os
from functools import wraps
from flask import Flask, session,render_template,request,url_for,redirect,flash, jsonify
import random 
from sqlalchemy import create_engine, cast
from sqlalchemy.types import String
from sqlalchemy.orm import scoped_session, sessionmaker
from database import *
import json
# from Books_DB import *
# from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
# from Books_DB import *



app = Flask(__name__)
app.secret_key = 'srujan_123'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)



# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:52416300@localhost:5432/test'

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://birawtnmsapodw:678f377d616ec505fb180996a6ecab8f3a3aaa51e47ab7719590df97ce7872ae@ec2-18-233-32-61.compute-1.amazonaws.com:5432/dad3mt6v6b5qe4"
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'log' not in session :
            flash('Login required','danger')
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/") 
def index():
    db.create_all()
    db.session.commit()
    if 'log' in session and 'name' in session :
        return render_template('mainpage.html',name = session['name'])
    return render_template('mainpage.html', name = '')
  

# @app.route('/rating',methods = ['GET','POST'])
# @login_required
# def rating():
#     isbn = '62049879';
#     if(request.method == 'GET'):
#         return render_template('rating.html',list = Ratings.query.filter_by( isbn = isbn).all() )
    

#     desc,stars = request.form.get('description'), request.form.get('rating')
#     db.session.add( Ratings(isbn = '62049879',mail = session['name'],star = stars,description = desc))
#     db.session.commit()
#     # userlist = Ratings.query.all()
#     return render_template('rating.html',list = Ratings.query.filter_by(isbn = isbn ).all() )



@app.route('/auth', methods = ['GET','POST'])
def auth():
    if(request.method == 'GET'):
        return render_template('loginpage.html')
    mail,password = (request.form.get('mailid'), request.form.get('password'))
    u = User.query.filter_by(mail = mail).first()        
    
    if u is not None and  check_password_hash(u.password,password)  :
        session['log'] = True
        session['name'] = u.mail
        # flash('Logged In')
        return redirect(url_for('home'))
    else:
        flash('Wrong Crendentials, Please Enter with your Eyes Open','danger')
        return render_template('loginpage.html')





@app.route('/home')
@login_required
def home():
    global book_list
    book_list = []
    return render_template('mainpage.html', name = 'to the dashboard ' + session['name'])

@app.route('/register', methods = ['GET','POST'])
def register():
    if (request.method == "GET"):
        return render_template('registerpage.html')

    mail,password = (request.form.get('mailid'), generate_password_hash(str(request.form.get('password'))) )
    if User.query.filter_by(mail = mail).first() is not None:
        flash('User name already exsists','danger')
        return redirect(url_for('register'))   
    db.session.add(User(mail = mail, name = mail.split('@')[0],password = password))
    db.session.commit()
    # session['log'] = True
    flash('Registration successfull, Please login','success')
    return redirect(url_for('auth'))


@app.route('/logout')
def logout():
    session.clear()
    global book_list
    book_list = []
    flash('success logged out','success')
    return redirect(url_for('auth'))


@app.route('/admin')
def admin():
    userlist = User.query.order_by(User.created_data).all()
    return render_template('admin.html',list = userlist)



@app.route('/book/<id>', methods=['GET','POST'])
def book(id):
    if(request.method == 'POST'):
        desc,stars = request.form.get('description'), request.form.get('rating')
        duplicate = Ratings.query.filter_by(isbn = id,mail = session['name']).first() 
        if duplicate is not None:
            flash("You have already reviewed this book",'danger')
        else:
            db.session.add( Ratings(isbn = id,mail = session['name'],star = stars,description = desc))
            db.session.commit()

    flag = False
    book_data = Book.query.filter_by(isbn = id).first()
    review_list  = Ratings.query.filter_by(isbn = id).all()
    if(len(review_list) == 0):
        flag = True
    return render_template('book.html', book=book_data , reviews = review_list,flag = flag)



@app.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    if request.method == 'GET':
        return render_template('search.html', book_len=0, book_list=[], page_num=0)
    else:
        # 380795272
        global book_list
        book_list = []

        book_isbn = request.form.get('isbn')
        book_title = request.form.get('title')
        book_author = request.form.get('author')
        book_year = request.form.get('year')
        # print(dict(request.form))
        page_num = 0
        flag = False

        book_list = Book.query.filter(Book.isbn.like('%'+book_isbn+'%') & Book.title.like('%'+book_title+'%') & Book.author.like('%'+book_author+'%') & cast(Book.year,String).like('%'+str(book_year)+'%')).all()
        book_list.sort(key=lambda x: x.title)

        if len(book_list) == 0:
            flash('No Books Found with the given parameters.','danger')

        if len(book_list) < 10 * (page_num + 1):
            flag = True
        
        page_cnt = len(book_list) // 10
        if len(book_list) % 10 != 0:
            page_cnt += 1


        return render_template('search.html', book_len=len(book_list), book_list=book_list, page=page_num, flag=flag, page_num=page_cnt)




@app.route('/page/<num>', methods = ['GET'])
@login_required
def page(num):
    num = int(num)
    flag = False
    if len(book_list) < 10 * (num):
        flag = True
    page_cnt = len(book_list) // 10
    if len(book_list) % 10 != 0:
        page_cnt += 1
    return render_template('search.html', book_len=len(book_list), book_list=book_list, page=num-1, flag=flag, page_num=page_cnt)



@app.route('/api/submit_review',methods = ['POST'])
def submit_review():
    data = dict(request.args)
    desc,stars,mail,isbn = data['description'],data['stars'],data['mailid'],data['isbn']
    if Book.query.filter_by(isbn = isbn).first() is None:
        return jsonify({'status':400})
    try:
        db.session.add( Ratings(isbn = isbn ,mail = mail ,star = stars ,description = desc))
        db.session.commit()
        return jsonify({'status':200})
    except:
        return jsonify({'status' : 500})

@app.route('/api/book_details', methods=['POST'])
def book_api():
    isbn_num = dict(request.args)["isbn"]
    try:
        book_data = Book.query.filter_by(isbn = isbn_num).first()
        if(book_data == None):
            return jsonify({"status":400})
        dict_book_api = {"isbn":book_data.isbn,"title":book_data.title,
        "author":book_data.author,"year":book_data.year,"status":200}

        review_list  = Ratings.query.filter_by(isbn = isbn_num).all()
        if(len(review_list) == 0):
            dict_book_api["reviews"] = None
        else:
            reviewers = []
            for reviewer in review_list:
                reviewers.append({"name":reviewer.rating_users.name,"rating":reviewer.star,
                    "description":reviewer.description})
            dict_book_api["reviews"] = reviewers
        return jsonify(dict_book_api)
    except:
        return jsonify({"status":500})

@app.route('/api/search', methods=['POST'])
def api_search():
    data = dict(request.args)

    loc_data = {'isbn':'', 'title':'', 'author':'', 'year':''}
    for each in data:
        loc_data[each] = data[each]
    try:
        book_list = Book.query.filter(Book.isbn.like('%'+loc_data['isbn']+'%') & Book.title.like('%'+loc_data['title']+'%') & Book.author.like('%'+loc_data['author']+'%') & cast(Book.year,String).like('%'+str(loc_data['year'])+'%')).all()
        
        ret_list = []
        ret_data = {}
        if len(book_list) == 0:
            return jsonify({'status': 400})
        for each in book_list:
            ret_list.append({'isbn':each.isbn, 'title':each.title, 'author':each.author, 'year':each.year})
        ret_data['books'] = ret_list
        ret_data['status'] = 200

        
        return jsonify(ret_data)
    except:
        return jsonify({'status': 500})
