from app_main import db, Model
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, event

@dataclass
class Subscription(Model):
    __tablename__ = 'IPO_SUBSCRIPTION_DATA'

    # company_name: str
    # open: str
    # close: str
    # issue_price: str
    # issue_size: str
    # qualified_inst_sub: str
    # non_inst_sub: str
    # retail_indv_sub: str
    # employee_sub: str
    # others_sub: str
    # total_sub: str
    # sub_page: str
    # main_page: str

    # company_name = db.Column(db.String, primary_key=True)
    company_name = Column('company_name', String, primary_key=True)
    # open = db.Column(db.String)
    open = Column('open', String)
    # close = db.Column(db.String)
    close = Column('close', String(200))
    # issue_price = db.Column(db.String)
    issue_price = Column('issue_price', String(200))
    # issue_size = db.Column(db.String)
    issue_size = Column('issue_size', String(200))
    # qualified_inst_sub = db.Column(db.String)
    qualified_inst_sub = Column('qualified_inst_sub', String(200))
    # non_inst_sub = db.Column(db.String)
    non_inst_sub = Column('non_inst_sub', String(200))
    # retail_indv_sub = db.Column(db.String)
    retail_indv_sub = Column('retail_indv_sub', String(200))
    # employee_sub = db.Column(db.String)
    employee_sub = Column('employee_sub', String(200))
    # others_sub = db.Column(db.String)
    others_sub = Column('others_sub', String(200))
    # total_sub = db.Column(db.String)
    total_sub = Column('total_sub', String(200))
    # sub_page = db.Column(db.String)
    sub_page = Column('sub_page', String(200))
    # main_page = db.Column(db.String)
    main_page = Column('main_page', String(200))