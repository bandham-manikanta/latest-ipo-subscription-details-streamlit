import pandas as pd
import requests as reqs
from app_main import db
from datetime import date
from pytz import timezone
from datetime import datetime
from bs4 import BeautifulSoup
from collections import Counter
from models import Subscription

# exception_list = ['Pavna Industries Limited IPO', 'Party Cruisers Limited IPO']

def get_ipos_data():
    all_ipos_page_response = reqs.get('https://www.chittorgarh.com/report/ipo-in-india-list-main-board-sme/82/')
    all_pages_soup = BeautifulSoup(all_ipos_page_response.content, 'html.parser')
    parent_div_table = all_pages_soup.find('div', {'id':'report_data'})
    table_tag = parent_div_table.find('table')
    thead_tag = table_tag.find('thead')
    th_tags = thead_tag.findAll('th')
    column_names = list()
    for th in th_tags:
        column_names.append(th.text.strip().replace('  ', ' '))

    tbody_tag = table_tag.find('tbody')
    tr_tags = tbody_tag.findAll('tr')
    ipo_page_links = list()
    issuer_company_names = list()
    exchange_names = list()
    open_dates = list()
    close_dates = list()
    lot_sizes = list()
    issue_prices = list()
    issue_sizes = list()

    for tr in tr_tags:
        link = tr.find('a').get('href')
        ipo_page_links.append(link.strip())
        tds = tr.findAll('td')
        issuer_company_names.append(tds[0].text.strip())
        exchange_names.append(tds[1].text.strip())
        open_dates.append(tds[2].text.strip())
        close_dates.append(tds[3].text.strip())
        lot_sizes.append(tds[4].text.strip())
        issue_prices.append(tds[5].text.strip())
        issue_sizes.append(tds[6].text.strip())

    dict_for_df = dict()

    for index, values in enumerate([issuer_company_names,exchange_names,open_dates,close_dates,lot_sizes,issue_prices,issue_sizes,ipo_page_links]):
        dict_for_df[index] = values

    column_names.append('URL')
    df = pd.DataFrame(dict_for_df)
    df.columns = column_names

    df = df[~((df['Close']=='') | (df['Close'].isna()))]
    df['Close'] = pd.to_datetime(df['Close'])
    df['Close'] = pd.to_datetime(df['Close'].dt.strftime("%Y-%m-%d 23:59:59"))

    df = df[~((df['Open']=='') | (df['Open'].isna()))]
    df['Open'] = pd.to_datetime(df['Open'])
    df['Open'] = pd.to_datetime(df['Open'].dt.strftime("%Y-%m-%d 00:00:00"))

    df['Qualified Institutional Subscription'] = None
    df['Non Institutional Subscription'] = None
    df['Retail Individual Subscription'] = None
    df['Employee Subscription'] = None
    df['Others Subscription'] = None
    df['Total Subscription'] = None
    df['Recommendations Statistics'] = None

    df['ipo_name'] = df['URL'].apply(lambda x: x.split('/')[4].strip())
    df['ipo_id'] = df['URL'].apply(lambda x: x.split('/')[5].strip())
    df['subscription_data_url'] = df.apply(lambda row: format_subscription_url(row), axis=1)

    # print(df.columns)

    format = "%Y-%m-%d %H:%M:%S"
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    today = now_asia.strftime(format)

    active_ipos_df = df[df['Close'] >= today]
    active_ipos_df = active_ipos_df[active_ipos_df['Open'] <= today]

    upcomingz_ipos_df = df[df['Open'] > today]
    past_ipos_df = df[df['Close'] < today]

    return active_ipos_df, upcomingz_ipos_df, past_ipos_df

def get_subscription_data(url:str) -> pd.DataFrame():
    sub_response = reqs.get(url)
    sup_soup = BeautifulSoup(sub_response.content, 'html.parser')
    print('url:', url)
    
    sub_table = sup_soup.find('table')
    sub_thead_tag = sub_table.find('thead')
    sub_th_tags = sub_thead_tag.findAll('th')
    sub_table_col_names = [x.text.strip() for x in sub_th_tags]

    institution_names = list()
    subscription_times = list()
    
    sub_tbody_tag = sub_table.find('tbody')
    sub_tr_tags = sub_tbody_tag.findAll('tr')
    for tr in sub_tr_tags:
        td_tags = tr.findAll('td')
        values = [td.text.strip() for td in td_tags]
        institution_names.append(values[0])
        subscription_times.append(values[1])
    sub_dict_for_df = {'0': institution_names, '1': subscription_times}
    sub_df = pd.DataFrame(sub_dict_for_df)
    sub_df.columns = sub_table_col_names
    return sub_df

def get_sub_data(row):
    sub = Subscription.query.get(row['Issuer Company'])

    if sub == None:
        try:
            sub_data = get_subscription_data(row['subscription_data_url'])
            row['Qualified Institutional Subscription'] = sub_data.iloc[0, :]['Subscription Status']
            row['Non Institutional Subscription'] = sub_data.iloc[1, :]['Subscription Status']
            row['Retail Individual Subscription'] = sub_data.iloc[2, :]['Subscription Status']
            row['Employee Subscription'] = sub_data.iloc[3, :]['Subscription Status']
            row['Others Subscription'] = sub_data.iloc[4, :]['Subscription Status']
            row['Total Subscription'] = sub_data.iloc[5, :]['Subscription Status']
        except:
            row['Qualified Institutional Subscription'] = 'NA'
            row['Non Institutional Subscription'] = 'NA'
            row['Retail Individual Subscription'] = 'NA'
            row['Employee Subscription'] = 'NA'
            row['Others Subscription'] = 'NA'
            row['Total Subscription'] = 'NA'

        sub = Subscription(company_name=row['Issuer Company'],open=str(row['Open']),close=str(row['Close']),issue_price=row['Issue Price (Rs)'],issue_size=row['Issue Size (Rs Cr)'],
        qualified_inst_sub=row['Qualified Institutional Subscription'],non_inst_sub=row['Non Institutional Subscription'],retail_indv_sub=row['Retail Individual Subscription'],
        employee_sub=row['Employee Subscription'],others_sub=row['Others Subscription'],total_sub=row['Total Subscription'],sub_page=row['subscription_data_url'],main_page=row['URL'])
        db.session.add(sub)
        db.session.commit()
    else:
        row['Qualified Institutional Subscription'] = sub.qualified_inst_sub
        row['Non Institutional Subscription'] = sub.non_inst_sub
        row['Retail Individual Subscription'] = sub.retail_indv_sub
        row['Employee Subscription'] = sub.employee_sub
        row['Others Subscription'] = sub.others_sub
        row['Total Subscription'] = sub.total_sub

    return row

def get_ipo_subscription_details():
    active_ipos_df, upcomings_ipos_df, past_ipos_df = get_ipos_data()

    active_ipos_df = active_ipos_df.apply(lambda row: get_sub_data(row), axis=1)
    past_ipos_df = past_ipos_df.apply(lambda row: get_sub_data(row), axis=1)

    # get ipo recommendation statistics for upcoming ipos

    active_ipos_df = active_ipos_df.apply(lambda row: get_recommendations_statistics(row), axis=1)

    active_ipos_df = active_ipos_df.sort_values(by='Open').reset_index()
    upcomings_ipos_df = upcomings_ipos_df.sort_values(by='Open').reset_index()
    past_ipos_df = past_ipos_df.sort_values(by='Open', ascending= False).reset_index()

    return active_ipos_df, upcomings_ipos_df, past_ipos_df

def format_subscription_url(row):
    ipo_name = row['ipo_name'].replace('-','%20')
    ipo_id = row['ipo_id']
    url = 'https://www.chittorgarh.com/ajax/ajax.asp?AjaxCall=GetSubscriptionPageIPOBiddingStatus&AjaxVal={ipo_id}&CompanyShortName={ipo_name}'.format(ipo_name=ipo_name,ipo_id=ipo_id)
    return url

def extract_sub_data(sub, row):
    row['Issuer Company'] = sub.company_name
    row['Open'] = sub.open
    row['Close'] = sub.close
    row['Issue Price (Rs)'] = sub.issue_price
    row['Issue Size (Rs Cr)'] = sub.issue_size
    row['Total Subscription'] = sub.total_sub
    row['Subscription Page'] = sub.sub_page
    row['Main Page'] = sub.main_page
    return row

def get_recommendations_statistics(row):
    print('row: ==>', row['URL'])
    ipo_home_page_response = reqs.get(row['URL'])
    home_page_soup = BeautifulSoup(ipo_home_page_response.content, 'html.parser')
    recomms_list = list()
    for i in home_page_soup.find_all('div'):
        if 'IPO Reviews / Ratings' in i.text:
            if len(i.find_all('div')) == 2:
                for j in i.find_all('li'):
                    rat_rev = j.text.split('-')
                    recomms_list.append(rat_rev[1].strip())
    counter = Counter(recomms_list)
    counter = sorted(counter.items(), key=lambda i: i[1], reverse=True)
    total_revs = 0
    for i in counter:
        total_revs = total_revs + i[1]
        
    final_string = ''
    for i in counter:
        perc = round((i[1]/total_revs) * 100, 2)
        final_string = final_string + i[0] + ' - ' + str(perc) + '%(' + str(i[1]) + '/' + str(total_revs) + ');\n'
    print(final_string)
    row['Recommendations Statistics'] = final_string
    return row