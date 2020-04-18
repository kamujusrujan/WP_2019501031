
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

import csv

engine = create_engine("postgres://birawtnmsapodw:678f377d616ec505fb180996a6ecab8f3a3aaa51e47ab7719590df97ce7872ae@ec2-18-233-32-61.compute-1.amazonaws.com:5432/dad3mt6v6b5qe4")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
	__tablename__ = "Books"
	isbn = Column(String, primary_key = True)
	title = Column(String)
	year = Column(Integer)
	author = Column(String)


data = open('books.csv','rt')
Base.metadata.create_all(engine)
data = list(csv.reader(data))
for a in tqdm(data[1:]):
	session.add( Book(isbn = a[0] , title = a[1] ,author = a[2] ,  year = int(a[3]) ))
session.commit()

