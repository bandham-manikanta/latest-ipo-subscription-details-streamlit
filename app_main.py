from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, event

def connect_mysql():
	engine = create_engine('sqlite:///data_base.db', echo = True)
	Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	return Session
	
db = connect_mysql()
Model = declarative_base(name='Model')
Model.query = db.query_property()
