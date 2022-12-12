import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
import pandas as pd
import numpy as np
import sqlite3
import csv


def percent(x):
        return "{:.0%}".format(x/1)

def no_dec(x):
        return "{:.0f}".format(x)

def money(x):
        return "${:,.0f}".format(x/1)

################################################################# Pulls in data #######################################################################
# Original Dataset
print("Cleaning Data.....")
shipments = pd.read_excel('/Users/DavidAarhus/Documents/GCL - Analytics/Data_Sheets/Transit_Performance.xlsx')
shipments = pd.DataFrame(shipments)
shipments['Carrier'] = shipments['Carrier'].str.upper()
shipments['Gross Margin'] = shipments['Gross Margin'].replace('[\$,)]','',regex=True).replace('[(]','-',regex=True).astype(float)

billing= pd.read_excel('/Users/DavidAarhus/Documents/GCL - Analytics/Data_Sheets/gcl_billing.xlsx')
quotes = pd.read_excel('/Users/DavidAarhus/Documents/GCL - Analytics/Data_Sheets/90day_quotereport.xlsx')
monthlyquotes = quotes
monthlyquotes = monthlyquotes.dropna()
carriers = pd.read_excel('/Users/DavidAarhus/Documents/GCL - Analytics/Data_Sheets/carrier_contacts.xlsx')

################# show new custys to add #################
# custys = billing["Customer"].unique()
# print(custys)
##########################################################
billing = pd.DataFrame(billing)
quotes = pd.DataFrame(quotes)
carriers = pd.DataFrame(carriers)


billing['Gross Margin'] = billing['Gross Margin'].replace('[\$,)]','',regex=True).replace('[(]','-',regex=True).astype(float)
billing['Margin Percent'] = billing['Margin Percent'].replace('[\%,)]','',regex=True).replace('[(]','-',regex=True).astype(float)
billing["Loads"] = billing["Customer"]
billing["Modes"] = billing["Mode"]

quotes = quotes.loc[~quotes['QuoteDetails'].str.contains("Quote ID", na=False)]
quotes = quotes.loc[~quotes['Customer'].str.contains("Total", na=False)]

carriers['Origin_City_State'] = carriers['Origin_City_State'].str.upper()
carriers['Service'] = carriers['Service'].str.upper()
carriers.to_csv('/Users/davidaarhus/lane_grader/csv_files/carrier_list.csv',index=False)

custy_lane = billing[["Customer","Margin Percent","Origin City","Destination City","Mode","Modes","Loads"]]
custy_lane.to_csv('/Users/davidaarhus/lane_grader/csv_files/custy_lanes.csv',index=False)

#######################################################################################################################################################

########################################################## Quotes (monthly) -- Data Wrangling / Cleaning ##############################################

dates = []
def is_date(date_string):
    try:
        pd.to_datetime(date_string, format='%Y-%m-%d')
        return True
    except Exception:
        return False

for i,row in monthlyquotes.iterrows():
    details = str(row["QuoteDetails"]).split('\n')
    date = str(details[1:2])[15:-5]
    # print(date)
    if len(details)>2:
        dates.append(date)
    else:
        dates.append("NaN")

monthlyquotes["Quote Date"] = dates
monthlyquotes=monthlyquotes.dropna(subset=['Quote Date'])
monthlyquotes = monthlyquotes[~monthlyquotes['Quote Date'].str.contains("NaN", na=False)]
monthlyquotes = monthlyquotes[['Customer', 'Total Quotes', 'Quotes Won', 'Quote Date']]
monthlyquotes.to_csv('/Users/davidaarhus/lane_grader/csv_files/quote_history.csv',index=False)

#######################################################################################################################################################

########################################################## Billing -- Data Wrangling / Cleaning #######################################################
dfshipments = billing
dfshipments["loads"] = dfshipments["Customer"]
dfshipments = pd.pivot_table(dfshipments, index=["Customer","Sales Rep"],sort=True, aggfunc={'Gross Margin': np.sum,
                                                                            "loads": 'count',
                                                                            "Margin Percent": np.mean,
                                                                            "Variance Count": np.sum}).round(2)
dfshipments["Variance %"] = (dfshipments["Variance Count"]/dfshipments["loads"]).round(2)                                                                   
dfshipments = dfshipments.reset_index()
dfshipments = dfshipments[["Customer","Margin Percent","Gross Margin","Variance Count","Variance %","loads"]]
dfshipments[['Customer_name', 'ID']] = dfshipments['Customer'].str.split('(', 1, expand=True)
del dfshipments["ID"]
data = quotes[["Customer","Win Ratio","Total Quotes"]]
data['Customer_name'] = data['Customer']
del data['Customer']
data['Win Ratio'] = data['Win Ratio'].round(2)
data['Total Quotes'] = data['Total Quotes'].apply(no_dec)
data['Win Ratio'] = data['Win Ratio'].astype(object)

dfshipments["Customer_name"] = dfshipments['Customer_name'].str.strip()
data["Customer_name"] = data['Customer_name'].str.strip()

dfshipments['Variance %'] = dfshipments['Variance %'].apply(percent)
data['Win Ratio'] = data['Win Ratio'].apply(percent)
dfshipments['Gross Margin'] = dfshipments['Gross Margin'].apply(money)



merged_df = dfshipments.merge(data,on=["Customer_name"],how='left')
del merged_df['Customer_name']

merged_df.to_csv('/Users/davidaarhus/lane_grader/csv_files/gcl_billing.csv',index=False)
#######################################################################################################################################################

########################################################## Lane Grader -- Data Wrangling / Cleaning ###################################################
days = []
weeks = []
months = []
est_transit_days = []
transit_days = []
date_format = "%Y-%m-%d"
total_days = 0;
for i,row in shipments.iterrows():
        estdelivery = str(row['Est. Delivery Date'])[0:10] 
        delivery = str(row['Act. Delivery Date'])[0:10]
        pickup = str(row['Pickup Date'])[0:10]
#         print(pickup) troubleshooting -- DONT DELETE
        e = datetime.strptime(estdelivery, date_format)
        a = datetime.strptime(delivery, date_format)
        b = datetime.strptime(pickup, date_format)
#         print(a) troubleshooting -- DONT DELETE
#         print(b) troubleshooting -- DONT DELETE
        diff = abs(a.date() - b.date())
        ediff = abs(e.date() - b.date())
#         print(diff.days, "days in transit", " -- ", row['Link'], ' -- ', row['Carrier'])
        transit_days.append(diff.days)
        est_transit_days.append(ediff.days)
        months.append(a.month)
        days.append(a.weekday())
        # weeks.append(a.)

#         months.append(calendar.month_name[a.month])
#         total_days+=diff.days

shipments["Act_Transit_days"] = transit_days
shipments["Est_Transit_days"] = est_transit_days
shipments["Transit_Score"] = abs(shipments["Est_Transit_days"] - shipments["Act_Transit_days"])
# shipments["Cost/mile-cents"] = shipments["Carrier Charge"]/shipments["Total Miles"]
shipments["Loads"] = shipments["Carrier"]
shipments["Month"] = months
shipments["Day"] = days
dfshipments = shipments
dfshipments = dfshipments[~(dfshipments['Act. Delivery Date'] < dfshipments['Pickup Date'])]
dfshipments = dfshipments[(dfshipments["Act_Transit_days"]<=20)]
dfshipments = dfshipments[(dfshipments["Est_Transit_days"]<=20)]
dfshipments = dfshipments[["BOL", "Carrier","Origin Zip","Destination Zip","Act_Transit_days","Est_Transit_days","Loads","Act. Delivery Date"]]
dfshipments.to_csv('/Users/davidaarhus/lane_grader/csv_files/sql_data.csv',index=False)
print("Done Cleaning.....")
print(str(len(dfshipments)) + " Shipments")
########################################################## Lane Grader -- Data Wrangling / Cleaning ########################################################



##################################################################### Connects to SQlite Database ##############################################################

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS custy_lane")
cursor.execute("DROP TABLE IF EXISTS lane_data")
cursor.execute("DROP TABLE IF EXISTS custy_data")
cursor.execute("DROP TABLE IF EXISTS carrier_list")
cursor.execute("DROP TABLE IF EXISTS quotes_list")

############# Creates data table ################################
cursor.execute("CREATE TABLE IF NOT EXISTS lane_data ("
               "bol VARCHAR(255),"
               "carrier VARCHAR(255),"
               "origin_zip VARCHAR(255),"
               "dest_zip VARCHAR(255),"
               "act_transit_days VARCHAR(255),"
               "est_transit_days VARCHAR(255),"
               "loads VARCHAR(255),"
               "act_del_day VARCHAR(255) )")


cursor.execute("CREATE TABLE IF NOT EXISTS custy_data ("
"customer VARCHAR(255),"
"margin_perc VARCHAR(255),"
"gross_profit VARCHAR(255),"
"variance_count VARCHAR(255),"
"variance_perc VARCHAR(255),"
"quote_win VARCHAR(255),"
"quote_total VARCHAR(255),"
"total_loads VARCHAR(255) )")


cursor.execute("CREATE TABLE IF NOT EXISTS custy_lane ("
"customer VARCHAR(255),"
"margin_perc VARCHAR(255),"
"origin_city VARCHAR(255),"
"dest_city VARCHAR(255),"
"mode VARCHAR(255),"
"modes VARCHAR(255),"
"loads VARCHAR(255) )")


cursor.execute("CREATE TABLE IF NOT EXISTS carrier_list ("
"carrier VARCHAR(255),"
"contact VARCHAR(255),"
"email VARCHAR(255),"
"service VARCHAR(255),"
"origin_city_state VARCHAR(255) )")


cursor.execute("CREATE TABLE IF NOT EXISTS quotes_list ("
"customer VARCHAR(255),"
"total_quotes VARCHAR(255),"
"quotes_won VARCHAR(255),"
"quote_date VARCHAR(255) )")

custysLanes = open('csv_files/custy_lanes.csv')
shipments = open('csv_files/sql_data.csv')
custys = open('csv_files/gcl_billing.csv')
carriers = open('csv_files/carrier_list.csv')
quotes = open('csv_files/quote_history.csv')

lanes = csv.reader(custysLanes)
loads = csv.reader(shipments)
shippers = csv.reader(custys)
carriers = csv.reader(carriers)
quotes = csv.reader(quotes)


lane_records = "INSERT INTO custy_lane (customer, margin_perc, origin_city, dest_city, mode, modes, loads) VALUES(?, ?, ?, ?, ?, ?, ?)"
shipment_records = "INSERT INTO lane_data (bol, carrier, origin_zip, dest_zip, act_transit_days, est_transit_days, loads, act_del_day) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
customer_records = "INSERT INTO custy_data (customer, margin_perc, gross_profit, variance_count, variance_perc, quote_win, quote_total, total_loads) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
carrier_records = "INSERT INTO carrier_list (carrier, contact, email, service, origin_city_state) VALUES(?, ?, ?, ?, ?)"
quote_records = "INSERT INTO quotes_list (customer, total_quotes, quotes_won, quote_date) VALUES(?, ?, ?, ?)"

cursor.executemany(lane_records, lanes)
connection.commit()
cursor.executemany(shipment_records, loads)
connection.commit()
cursor.executemany(customer_records, shippers)
connection.commit()
cursor.executemany(carrier_records, carriers)
connection.commit()
cursor.executemany(quote_records, quotes)
connection.commit()


##################################################################### Connects to SQlite Database ########################################################################

################### Troubleshooting ###################
# select_all = "SELECT * FROM lane_data LIMIT 100"
# rows = cursor.execute(select_all).fetchall()
# # Output to the console screen
# for r in rows:
#     print(r)
# Committing the changes
# connection.commit()
################### Troubleshooting ###################

 
# closing the database connection
connection.close()