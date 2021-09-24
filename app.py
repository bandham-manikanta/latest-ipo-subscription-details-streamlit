import streamlit as st

st.write("Hello Streamlit..")
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
st.write(add_selectbox)


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, event


def connect_mysql():
	
	engine = create_engine('sqlite:///data_base.db', echo = True)
	Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	return Session
	

conn = connect_mysql()

Model = declarative_base(name='Model')
Model.query = conn.query_property()


class User(Model):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    openid = Column('openid', String(200))
    name = Column(String(200))

query = "SELECT * FROM users"
result = conn.execute(query)
df = pd.DataFrame(result.fetchall())
if df.empty:
	df = pd.DataFrame(columns=result.keys())
else:
	df.columns = result.keys()

st.write(df)

