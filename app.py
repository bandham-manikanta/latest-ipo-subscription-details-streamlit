import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from routes import get_ipo_subscription_details
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, event

st.write("Hello Streamlit..")

active_ipos_df, upcoming_ipos_df, past_ipos_df = get_ipo_subscription_details()
st.write('Active IPOs:\n')
st.write(active_ipos_df)
st.write('Upcoming IPOs:\n')
st.write(upcoming_ipos_df)
st.write('Past IPOs:\n')
st.write(past_ipos_df)