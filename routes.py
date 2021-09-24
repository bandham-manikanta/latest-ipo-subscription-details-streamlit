import numpy as np
import pandas as pd
from pytz import timezone
from datetime import datetime
from models import Subscription
from utility_functions import get_ipo_subscription_details, extract_sub_data
from app_main import db

# Get datetime for today: start
format = "%Y-%m-%d %H:%M:%S"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
today = now_asia.strftime(format)
# Get datetime for today: end

def get_all_subscriptions():
    sql = 'select * from IPO_SUBSCRIPTION_DATA'
    result = db.execute(sql)
    df1 = pd.DataFrame(result.fetchall())
    return df1

def get_ipos_data():
    active_ipos_df, upcoming_ipos_df, past_ipos_df = get_ipo_subscription_details()
    active_ipo_columns = ['Issuer Company', 'Open', 'Close', 'Issue Price (Rs)', 
        'Issue Size (Rs Cr)', 'Qualified Institutional Subscription',
       'Non Institutional Subscription', 'Retail Individual Subscription',
       'Employee Subscription', 'Others Subscription', 'Total Subscription', 'Recommendations Statistics', 'subscription_data_url', 'URL',]
    active_ipos_df = active_ipos_df[active_ipo_columns]
    active_ipos_df.columns = ['Issuer Company', 'Open', 'Close', 'Issue Price (Rs)', 
        'Issue Size (Rs Cr)', 'Qualified Institutional Subscription',
       'Non Institutional Subscription', 'Retail Individual Subscription',
       'Employee Subscription', 'Others Subscription', 'Total Subscription', 'Recommendations Statistics', 'Subscription Page', 'Main Page']
    
    upcoming_ipo_columns = ['Issuer Company', 'Open', 'Close', 'Issue Price (Rs)', 'Issue Size (Rs Cr)', 'URL']
    upcoming_ipos_df = upcoming_ipos_df[upcoming_ipo_columns]
    upcoming_ipos_df.columns = ['Issuer Company', 'Open', 'Close', 'Issue Price (Rs)', 'Issue Size (Rs Cr)', 'Main Page']

    sql = 'Select * from IPO_SUBSCRIPTION_DATA'
    results = db.execute(sql)
    subs = results.fetchall()
    subs = [sub for sub in subs if not ((sub.close >= today) and (sub.open <= today))]

    past_ipos_columns = ['Issuer Company', 'Open', 'Close', 'Issue Price (Rs)', 'Issue Size (Rs Cr)', 'Total Subscription', 'Subscription Page', 'Main Page']
    past_ipos_df = pd.DataFrame(index=np.arange(len(subs)), columns=past_ipos_columns)

    for index, sub in enumerate(subs):
        past_ipos_df.iloc[index, :] = extract_sub_data(sub, past_ipos_df.iloc[index, :])

    # return render_template("response.html", active_ipos_df=active_ipos_df, upcoming_ipos_df=upcoming_ipos_df, past_ipos_df=past_ipos_df)
    return active_ipos_df, upcoming_ipos_df, past_ipos_df