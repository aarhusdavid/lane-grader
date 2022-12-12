
### Source - https://realpython.com/python-web-applications/
##############################################                FOR TESTING                    ##############################################
############################################## TO ACTIVATE VIRTUAL ENVIRONMENT FROM TERMINAL ##############################################
#   - navigate to project folder
#   - type: "source venv/bin/activate" into command line
#   - ready to install flask: "python3 -m pip install -r requirements.txt"
#   - run script: "python3 main.py"
#   - deactivate venv when done: "deactivate"
############################################## TO ACTIVATE VIRTUAL ENVIRONMENT FROM TERMINAL ##############################################
##############################################                FOR TESTING                    ##############################################

############################################## ERROR LOG ##############################################
######## Problem
#   (gcloud.app.deploy) Error Response: [9] Cloud build b041699a-3941-49fa-bb5d-cdfa2892c634 status: FAILURE
#   An unexpected error occurred. Refer to build logs: https://console.cloud.google.com/cloud-build/builds;region=us-central1/b041699a-3941-49fa-bb5d-cdfa2892c634?project=1090635318632
#   Full build logs: https://console.cloud.google.com/cloud-build/builds;region=us-central1/b041699a-3941-49fa-bb5d-cdfa2892c634?project=1090635318632
# Solution
#   Execution succeed with downgrading setuptools to 60.2.0
#   python3 -m pip install --upgrade setuptools==60.2.0

######### Problem
#   502 Bad Gateway
#       nginx
# Progress: https://serverfault.com/questions/1056138/modulenotfounderror-no-module-named-main
#   added: entrypoint: gunicorn -b:$PORT app:app to app.yaml
#   New Problem - Error: Server Error
#                               The server encountered an error and could not complete your request.
#                                  Please try again in 30 seconds.
# Solution
#   changed "app.py" to "main.py"
#   full answer - https://stackoverflow.com/questions/73532069/gcloud-app-engine-502-bad-gateway-server-error/73548624?noredirect=1#comment129918612_73548624
######### Problem
#   502 Bad Gateway
#       nginx
#
#Solution
#     return render_template('/fak.html')
#           Needed the '/' before the html page for it to POST properly, server couldn't locate the page without it.   
#
######### Problem ( when trying to connect to mysql database on google cloud platform)
#   502 Bad Gateway
#     nginix
#Solution
#     tbd
### Temporary solution
#### using sqlite



############################################## ERROR LOG ##############################################

# You can stream logs from the command line by running:
#   $ gcloud app logs tail -s default

# To view your application in the web browser run:
#   $ gcloud app browse

############################################## PROJECT SPECS ##############################################
#  Project ID: "lane-grader-359817"
# gcloud auth login - login into gcloud account
# gcloud config set project [project] - selects what project to run
############################################## PROJECT SPECS ##############################################

# app.config['user'] = 'root'
# app.config['password'] = 'Snakshak12!'
# app.config['host'] = '34.174.50.222'
# app.config['client_flags'] = [ClientFlag.SSL]
# app.config['ssl_ca'] = 'ssl/server-ca.pem'
# app.config['ssl_cert'] = 'ssl/client-cert.pem'
# app.config['ssl_key'] = 'ssl/client-key.pem'
# app.config['database'] = 'testdb'

# config = {
#             'user': 'root',
#             'password': 'Snakshak12!',
#             'host': '34.174.50.222',
#             'client_flags': [ClientFlag.SSL],
#             'ssl_ca': 'ssl/server-ca.pem',
#             'ssl_cert': 'ssl/client-cert.pem',
#             'ssl_key': 'ssl/client-key.pem',
#             'database': 'testdb'
#         }


#### Turned off
# Ring Central Sandbox Account - 	+19293784980
# Password - 	Freight1!


from flask import Flask, render_template, request
import datetime
import math
import sqlite3
import re



app = Flask(__name__, template_folder="templates")


@app.route("/", methods=['GET','POST'])
def index():
    # If you're just opening your home page
    if request.method == 'GET':
        return render_template('/index.html')
    # If you submitted one of the forms
    elif request.method == 'POST':
        if request.values.get("action0", None) == 'Home':
            return render_template('/index.html')
        elif request.values.get("action1", None) == 'Calculator':
            return render_template('/densitycalc.html')
        elif request.values.get("action2", None) == 'Linear Feet':
            return render_template('/linearFeet.html')
        elif request.values.get("action3", None) == 'Insurance':
            return render_template('/insurance.html')
        elif request.values.get("action5", None) == 'Services':
            return render_template('/services.html')
        elif request.values.get("action6", None) == 'Logins':
            return render_template('/logins.html')
        elif request.values.get("action7", None) == 'Freight Class':
            return render_template('/density.html')
        elif request.values.get("action8", None) == 'Lane Grader':
            return render_template('/laneGrader.html')
        elif request.values.get("action9", None) == 'Billing':
            return render_template('/billing.html')
        elif request.values.get("action10", None) == 'Services':
            return render_template('/services.html')

###################################################################################################################
###################################################################################################################
####################### Page functions / Navigation ###############################################################


@app.route("/laneGrader/", methods=['GET', 'POST'])
def laneGrader():
    if request.method == 'GET':
        return render_template('/laneGrader.html')
    elif request.method == 'POST':
        # return render_template('/laneGrader.html')
        pick = request.form["pickzip"]
        pick = pick[:2]
        dest = request.form["destzip"]
        dest = dest[:2]
        ########################## SQL COMMAND GRABS LANE ####################################
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT Carrier,ROUND(AVG(act_transit_days),0),ROUND(AVG(est_transit_days),0), COUNT(Loads)
                FROM lane_data
                WHERE SUBSTR(origin_zip, 1, 2)=? AND SUBSTR(dest_zip, 1, 2)=?
                GROUP BY Carrier
                ORDER BY COUNT(Loads) DESC""", (pick,dest,))
        data = cursor.fetchall()
        if data:
            headings = ("Carrier", "Actual", "Estimated", "Load Count")
            connection.close()
            return render_template('/laneGrader.html',headings=headings, data=data)
        else:
            headings = (["Not Enough Data on this lane"])
            connection.close()
            return render_template('/laneGrader.html', headings=headings)
        
@app.route("/carrierLane/", methods=['GET', 'POST'])
def carrierLane():
    if request.method == 'GET':
        return render_template('/laneGrader.html')
    elif request.method == 'POST':
        # return render_template('/laneGrader.html')
        pick = request.form["carrier_pickzip"]
        pick = pick[:2]
        dest = request.form["carrier_destzip"]
        dest = dest[:2]
        carrier = request.form["carrier"]
        carrier = str(carrier).upper()
        ########################## SQL COMMAND GRABS LANE ####################################
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT bol,carrier,act_transit_days,est_transit_days,act_del_day
                FROM lane_data
                WHERE SUBSTR(origin_zip, 1, 2)=? AND SUBSTR(dest_zip, 1, 2)=? and Carrier=?
                """, (pick,dest,carrier,))
        data = cursor.fetchall()
        if data:
            headings = ("BOL", "Carrier", "Transit Days", "Estimated Days","Actual Delivery Date")
            connection.close()
            return render_template('/laneGrader.html',headings=headings, data=data)
        else:
            headings = (["Not Enough Data on this lane"])
            connection.close()
            return render_template('/laneGrader.html', headings=headings)

# @app.route("/quotehist/", methods=['GET', 'POST'])
# def quotehist():
#     if request.method == 'GET':
#         return render_template('/billing.html')
#     elif request.method == 'POST':
#         connection = sqlite3.connect('database.db')
#         cursor = connection.cursor()
#         cursor.execute("""SELECT DISTINCT customer FROM custy_data""")
#         quotes = cursor.fetchall()
#         if customers:
#             connection.close()
#             return render_template('/billing.html',customers=customers)
#         else:
#             customers = (["NULLL", "NULLL", "NULLL","NULLL","NULLL"])
#             connection.close()
#             return render_template('/billing.html', customers=customers)


@app.route("/billing/", methods=['GET', 'POST'])
def billing():
    if request.method == 'GET':
        return render_template('/billing.html')
    elif request.method == 'POST':
        # return render_template('/billing.html')
        # return render_template('/laneGrader.html')
        custy = request.form["custy"]
        ########################## SQL COMMAND GRABS LANE ####################################
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        ####################### summary stats #################
        cursor.execute("""SELECT customer, margin_perc, gross_profit, variance_perc, quote_win, quote_total, total_loads
                FROM custy_data
                WHERE customer=?""", (custy,))
        data = cursor.fetchall()
        #######################################################

        ####################### top 5 lanes #################
        cursor.execute("""SELECT customer, mode, ROUND(AVG(margin_perc),2), origin_city, dest_city, COUNT(loads)
                FROM custy_lane
                WHERE customer=?
                GROUP BY origin_city, dest_city
                ORDER BY COUNT(loads) DESC
                LIMIT 5""", (custy,))
        custylane = cursor.fetchall()
        #######################################################

        ####################### modes #################
        cursor.execute("""SELECT mode, ROUND(AVG(margin_perc),2), COUNT(modes)
                FROM custy_lane
                WHERE customer=?
                GROUP BY mode
                ORDER BY COUNT(modes) DESC
               """, (custy,))
        modes = cursor.fetchall()
        #######################################################

        ####################### quotes #################
        editcusty = custy
        editcusty=re.sub("\(.*?\)","",editcusty)
        editcusty = str(editcusty).upper().strip()
        # print(editcusty)
        cursor.execute("""SELECT customer, quote_date, ((ROUND((SUM(quotes_won)/SUM(total_quotes)* 100)))) || '%', COUNT(total_quotes)
                FROM quotes_list
                WHERE customer=?
                GROUP BY quote_date""", (editcusty,))
        quotes = cursor.fetchall()

        # print(quotes)
        #######################################################

        if data and custylane:
            headings = ("Customer", "Avg. Margin %", "Gross Profit $", "Variance %", "Total Shipments", "Quote/Win Ratio", "Total Quotes")
            data_title = "Summary Statistics"
            lane_headings = ("Customer", "Mode","Avg. Margin %", "Origin City", "Destination City", "Total Shipments")
            lane_title = "Lane Analytics (Top 5)"
            mode_headings = ("Mode", "Avg. Margin %","Total Shipments")
            mode_title = "Mode Summary"
            quote_headings = ("Customer", "Month","Quote/Win%", "Total Quotes")
            quote_title = "Quote Summary"

            connection.close()
            return render_template('/billing.html',headings=headings, data=data, data_title=data_title,
                                                custylane=custylane, lane_headings=lane_headings, lane_title=lane_title,
                                                modes=modes, mode_headings=mode_headings,mode_title=mode_title,
                                                quotes=quotes, quote_headings=quote_headings, quote_title=quote_title)
        else:
            data = (["NULLL", "NULLL", "NULLL", "NULLL","NULLL","NULLL"])
            headings = ("Customer", "Avg. Margin %", "Gross Profit $", "Variance %", "Quote/win Ratio", "Total Quotes", "Total Shipments")
            connection.close()
            return render_template('/billing.html', headings=headings, data=data)




@app.route("/densitycalc/", methods=['GET', 'POST'])
def densitycalc():
    # If you're just opening your calculator page
    if request.method == 'GET':
        return render_template('/density.html')
    # If you're submitting a form
    elif request.method == 'POST':
        units_1 = request.form["unit_count"]
        length_1 = request.form["unit_length"]
        width_1 = request.form["unit_width"]
        height_1 = request.form["unit_height"]
        weight_1 = request.form["unit_weight"]
        try:
            if length_1 and width_1 and height_1 and weight_1 and units_1:
                # print(length)
                cubic_Feet = (float(length_1) * float(width_1) * float(height_1))/1728
                density = round(float(weight_1)/cubic_Feet,2)
                # min_length = max(float(length_1),float(width_1))
                # max_length = max(float(length_1),float(width_1))
                # base_linear_feet = float(length_1)/12
                if float(units_1) > 1:
                    density = round(density/float(units_1),2)
                    density = str(density)
                    base_linear_feet = float(length_1)/12
                    if float(width_1) <= 48:
                        final_linear_feet = base_linear_feet/2
                        final_linear_feet = math.ceil(final_linear_feet*float(units_1))
                        # weight_linear_feet = final_linear_feet*float(units_1)
                    else:
                        final_linear_feet = base_linear_feet/1
                        final_linear_feet = math.ceil(final_linear_feet*float(units_1))
                        # weight_linear_feet = final_linear_feet*float(units_1)

                else:
                    density = str(density)
                    base_linear_feet = float(length_1)/12
                    if float(width_1) < 12:
                        final_linear_feet = 1
                    elif float(width_1) > 12 and float(width_1) <= 48:
                        final_linear_feet = math.ceil(round(base_linear_feet/2))
                        # weight_linear_feet = final_linear_feet*float(base_linear_feet/2)
                    else:
                        final_linear_feet = math.ceil(round(base_linear_feet/1))
                        # weight_linear_feet = final_linear_feet*float(base_linear_feet/1)


                linear_weight_threshold = math.ceil(float(weight_1)/1000)
                if final_linear_feet >= linear_weight_threshold:
                    final_linear_feet = final_linear_feet
                else:
                    final_linear_feet = linear_weight_threshold

                ###### Defines Freight class based on density ######
                if float(density) >= 30:
                    ship_class="60"
                elif 30 > float(density) >= 22.5:
                    ship_class="65"
                elif 22.5 > float(density) >= 15:
                    ship_class="70"
                elif 15 > float(density) >= 12:
                    ship_class="85"
                elif 12 > float(density) >= 10:
                    ship_class="92.5"
                elif 10 > float(density) >= 8:
                    ship_class="100"
                elif 8 > float(density) >= 6:
                    ship_class="125"
                elif 6 > float(density) >= 4:
                    ship_class="175"
                elif 4 > float(density) >= 2:
                    ship_class="250"
                elif 2 > float(density) >= 1:
                    ship_class="300"
                elif 1 > float(density):
                    ship_class="400"

                messages = [{'title': 'Density: ' + density + " lb/cubic ft",
                            'content': 'Suggested Class: ' + ship_class,
                            'content2': 'Linear Feet: ' + str(final_linear_feet)}]
                return render_template('/density.html', messages=messages)
            else:
                density = "Error"
                messages = [{'title': 'Density: ' + density}]
                return render_template('/density.html', messages=messages)
        except ValueError:
            density = "Error"
            messages = [{'title': 'Density: ' + density}]
            return render_template('/density.html', messages=messages)

@app.route("/ctdensity/", methods=['GET', 'POST'])
def ctdensity():
    # If you're just opening your calculator page
    if request.method == 'GET':
        return render_template('/density.html')
    # If you're submitting a form
    elif request.method == 'POST':
        # units_1 = request.form["unit_count"]
        # length_1 = request.form["unit_length"]
        # width_1 = request.form["unit_width"]
        # height_1 = request.form["unit_height"]
        # weight_1 = request.form["unit_weight"]
        try:
            headings = ("Freight Class", "Density lbs/cubic_ft")
            data = [["50","50 pcf or greater"],
                    ["55","35 pcf but less than 50 pcf"],
                    ["60","30 pcf but less than 35 pcf"],
                    ["65","22.5 pcf but less than 30 pcf"],
                    ["70","15 pcf but less than 22.5 pcf"],
                    ["77.5","13.5 pcf but less than 15 pcf"],
                    ["85","12 pcf but less than 13.5 pcf"],
                    ["92.5","10.5 pcf but less than 12 pcf"],
                    ["100","9 pcf but less than 10.5 pcf"],
                    ["110","8 pcf but less than 9 pcf"],
                    ["125","7 pcf but less than 8 pcf"],
                    ["150","6 pcf but less than 7 pcf"],
                    ["175","5 pcf but less than 6 pcf"],
                    ["200","4 pcf but less than 5 pcf"],
                    ["250","3 pcf but less than 4 pcf"],
                    ["300","2 pcf but less than 3 pcf"],
                    ["400","1 pcf but less than 2 pcf"],
                    ["500","Less than 1 pcf"]]

            return render_template('/density.html', headings=headings, data=data)
        except ValueError:
            density = "Error"
            messages = [{'title': 'Density: ' + density}]
            return render_template('/density.html', messages=messages)


@app.route("/datepicker/", methods=['GET', 'POST'])
def datepicker():
    # If you're just opening your calculator page
    if request.method == 'GET':
        return render_template('/densitycalc.html')
    # If you're submitting a form
    elif request.method == 'POST':
        try:
            input_date = request.form["date"][0:10]
            today = str(datetime.datetime.today())[0:10]
            # convert string to date object
            present = datetime.datetime.strptime(today, "%Y-%m-%d")
            past = datetime.datetime.strptime(input_date, "%Y-%m-%d")

            # difference between dates in timedelta
            delta = present - past
            messages = [{'title': 'Past Due: ' + str(delta.days)+" Days",
                        'content': 'Invoice Date: ' + str(input_date)}]
            return render_template('/densitycalc.html', messages=messages)
        except ValueError:
            error_message = "Error"
            messages = [{'title': error_message}]
            return render_template('/densitycalc.html', messages=messages)


######## Questions on calculations #########
# 28' PUPS
# Max Length 180
# Max Width (2 unit) 96
# Max Width (1 unit) 72
# Max Height 96

@app.route("/linearFeet/", methods=['GET', 'POST'])
def linearFeet():
    # If you're just opening your linearFeet page
    if request.method == 'GET':
        return render_template('/linearFeet.html')
    # If you're submitting a form
    elif request.method == 'POST':
        length = request.form["length"]
        width = request.form["width"]
        height = request.form["height"]
        units = request.form["units"]
        # """Convert pallet specs to freight density."""
        try:
            if length and width and height and units:
                # linear feet calculation
                if float(units) == 1 and float(length) <= 72 and float(width) <= 72:
                    # max_length = max(float(length),float(width))
                    min_length = min(float(length),float(width))
                    linear_Feet = math.ceil(round(min_length/12,))
                    linear_Feet = str(linear_Feet)
                    mode = "LTL"
                elif float(units) > 1:
                    if round(float(units)%2,2) > 0 and float(length) <= 48 and float(width) <= 48:
                        #unit count is odd and length and width add up to/less than 96
                        min_length = min(float(length),float(width))

                    else:
                        #unit count is even and length and width add up to/less than 96
                        min_length = min(float(length),float(width))
                        ttl_length = float(min_length)*(float(units)/2)
                        linear_Feet = math.ceil(round(ttl_length/12,2))
                        linear_Feet = str(linear_Feet)
                        if float(linear_Feet) > 12:
                            mode = "Volume"
                        else:
                            mode = "LTL"
                        #unit count is even
                    # linear_Feet = round(float(units)%2,4)
                    # linear_Feet = "calc"
                    # mode = "Volume"
                    # linear feet calculation
                else:
                    linear_Feet = "Error"
                    mode = "NULL"

                messages = [{'title': 'Linear Feet: ' + str(linear_Feet),
                            'content': 'Mode: ' + mode}]
                return render_template('/linearFeet.html', messages=messages)
            else:
                density = "Error"
                messages = [{'title': 'Linear Feet: ' + str(density)}]
                return render_template('/linearFeet.html', messages=messages)
        except ValueError:
            density = "Error"
            messages = [{'title': 'Linear Feet: ' + density}]
            return render_template('/linearFeet.html', messages=messages)

######## Qualifications on calculations #########
# no 3 digit dims
# have to be seperated by a single char element ( #,x,/,etc)
# weight has to followed by 'lbs' or '#'
# each row has to be one unit

@app.route("/linearFeetbulk/", methods=['GET', 'POST'])
def linearFeetbulk():
    # If you're just opening your linearFeet page
    if request.method == 'GET':
        return render_template('/linearFeet.html')
    # If you're submitting the bulk  form
    elif request.method == 'POST':
        shipment = request.form['text']
        ###### per line item ######
        ### dims = [7], weight = [8,X], 'lbs'=[X+1,X+3]
        shipment_length = len(shipment)
        # length=shipment[0:2]
        # width=shipment[4:5]
        # height=shipment[7:8]

        return render_template('/linearFeet.html', messages=str(shipment_length))
        # """Convert pallet specs to freight density."""


@app.route("/insurance/", methods=['GET', 'POST'])
def insurance():
    tl_floor = 23077 
    tl_min = 30
    ltl_floor = 10000
    min = 37
    # If you're just opening your insurance page
    if request.method == 'GET':
        return render_template('/insurance.html')
    # If you're submitting a form
    elif request.method == 'POST':
        value = request.form["value"]
        # """Converts to ins cost"""
        try:
            tl_cost = tl_floor-float(value)
            cost = ltl_floor-float(value)
            if cost >= 0:
                tl_cost = str(tl_min)
                ins_cost = str(min)
                messages = [{'title': 'LTL/Volume Insurance Cost: ' + "$" + ins_cost,
                            'content': 'Dedicated Insurance Cost: ' + "$" + tl_cost}]
                return render_template('/insurance.html', messages=messages)
            elif cost < 0 and float(value) > 23077:
                diff_cost = ((float(value)-ltl_floor)*.0037)+min
                tl_diff_cost = ((float(value)-tl_floor)*.0013)+tl_min
                tl_diff_cost = round(tl_diff_cost,2)
                ins_cost = round(diff_cost,2)
                messages = [{'title': 'LTL/Volume Insurance Cost: ' + "$" + str(ins_cost),
                            'content': 'Dedicated Insurance Cost: ' + "$" + str(tl_diff_cost)}]
                return render_template('/insurance.html', messages=messages)
            elif cost < 0 and float(value) <= 23077:
                diff_cost = ((float(value)-ltl_floor)*.0037)+min
                ins_cost = round(diff_cost,2)
                messages = [{'title': 'LTL/Volume Insurance Cost: ' + "$" + str(ins_cost),
                            'content': 'Dedicated Insurance Cost: ' + "$" + str(tl_min)}]
                return render_template('/insurance.html', messages=messages)
            else:
                ins_cost = "Error"
                messages = [{'title': 'LTL/Volume Insurance Cost: ' + ins_cost}]
                return render_template('/insurance.html', messages=messages)
        except ValueError:
            ins_cost = "Error"
            messages = [{'title': 'LTL/Volume Insurance Cost: ' + ins_cost}]
            return render_template('/insurance.html', messages=messages)

@app.route("/freightclass/", methods=['GET', 'POST'])
def freightclass():
    if request.method == 'GET':
        return render_template('/freightclass.html')
    elif request.method == 'POST':
        return render_template('/freightclass.html')

@app.route("/services/", methods=['GET', 'POST'])
def services():
    if request.method == 'GET':
        return render_template('/services.html')
    elif request.method == 'POST':
        # return render_template('/laneGrader.html')
        origin = request.form["origin"]
        service = request.form["service"]
        ########################## SQL COMMAND GRABS LANE ####################################
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT carrier,contact,email,service,origin_city_state 
                FROM carrier_list
                WHERE service=? AND origin_city_state=? """, (service,origin,))
        data = cursor.fetchall()
        if data:
            headings = ("Carrier", "Contact", "Email", "Service", "Origin")
            connection.close()
            return render_template('/services.html',headings=headings, data=data)
        else:
            data = (["NULL", "NULL", "NULL", "NULL"])
            headings = ("Carrier", "Contact", "Email", "Service", "Origin")
            connection.close()
            return render_template('/services.html', headings=headings, data=data)




@app.route("/fak/", methods=['GET', 'POST'])
def fak():
    if request.method == 'GET':
        return render_template('/density.html')
    elif request.method == 'POST':
        service = request.form["selection"]
        try:
            if service:
                 ###### Defines Product nmfc, description, class ######
                if service == "Lighting Fixtures":
                    items = [{'Product': "Lighting",
                            'Description': 'Bodies, Pans or Strips, fluorescent lighting fixtures',
                            'Class': '85',
                            'NMFC': '109060'}]
                elif service == "Lights":
                    items = [{'Product': "Lights",
                            'Description': 'Lights, floor, roof, sidewalk or vault, consisting of metal or concrete frames containing glass bricks or blocks, but not sheet or plate glass, for daylighting purposes, in boxes or crates',
                            'Class': '60',
                            'NMFC': '34960'}]
                elif service == "Containers":
                    items = [{'Product': "Containers",
                            'Description': 'Containers - NOI',
                            'Class': '70',
                            'NMFC': '152605'}]
                elif service == "Chairs":
                    items = [{'Product': "Chairs",
                            'Description': 'Chair Seats or Backs',
                            'Class': '70',
                            'NMFC': '82890'}]
                elif service == "Filters":
                    items = [{'Product': "Filters",
                            'Description': 'Filters',
                            'Class': '85',
                            'NMFC': '69060'}]
                elif service == "Grills":
                    items = [{'Product': "Grills",
                            'Description': 'Grills, Outdoor Fireplace',
                            'Class': '70',
                            'NMFC': '69450-01'}]
                elif service == "Tools":
                    items = [{'Product': "Tools",
                            'Description': 'Tools - NOI',
                            'Class': '77.5',
                            'NMFC': '186630'}]
                elif service == "Toys":
                    items = [{'Product': "Toys",
                            'Description': 'Toys - NOI',
                            'Class': '85',
                            'NMFC': '84270'}]
                elif service == "Trade Show":
                    items = [{'Product': "Trade Show",
                            'Description': 'Paraphernalia, exhibition or trade show, NOI',
                            'Class': '125',
                            'NMFC': '83340'}]
                elif service == "Couch/Sofa":
                    items = [{'Product': "Couch/Sofa",
                            'Description': 'Couch or Sofa Arms or Ends',
                            'Class': '100',
                            'NMFC': '82970'}]
                elif service == "Apparel":
                    items = [{'Product': "Apparel",
                            'Description': 'Cloth or Fabric',
                            'Class': '85',
                            'NMFC': '49270'}]
                elif service == "Furniture":
                    items = [{'Product': "Furniture",
                            'Description': 'Furniture Parts',
                            'Class': '70',
                            'NMFC': '83340'}]
                elif service == "Home Furnishing":
                    items = [{'Product': "Home Furnishing",
                            'Description': 'Kits, craft, home furnishing',
                            'Class': '85',
                            'NMFC': '14557'}]
                elif service == "Buckles":
                    items = [{'Product': "Buckles - NOI",
                            'Description': 'Buckles, baling tie, NOI, in packages',
                            'Class': '50',
                            'NMFC': '104640'}]
                elif service == "Pillows":
                    items = [{'Product': "Pillows - NOI",
                            'Description': 'Mattresses; Pillows; or Cushions, NOI',
                            'Class': '70',
                            'NMFC': '16870'}]
                else:
                    items = [{'Product': "Error",
                            'Description': 'Error',
                            'Class': 'Error',
                            'NMFC': 'Error'}]
               
                return render_template('/density.html', items=items)
        except ValueError:
            density = "Error"
            items = [{'title':density}]
            return render_template('/density.html', items=items)

################### API PAGE ###################
# @app.route("/api/",  methods=['GET', 'POST'])
# def api():
#     # KEY="DemoOnly003gbBlwNX0SPKxGfooM3zaKTsPwHnJPkbHT0DLHL1GReEwIutZKseyU"
#     # pick = str(request.form["Pickup"])
#     # dest = str(request.form["Destination"])
#     if request.method == 'GET':
#         # jsonurl = url_for("https://"+"www.zipcodeapi.com/rest/"+KEY+"/distance.json/"+pick+"/"+dest+"/mile")
#         # jwks = json.loads(jsonurl.read())
#         return render_template('/api.html')
#     elif request.method == 'POST':
#         # jsonurl = url_for("https://"+"www.zipcodeapi.com/rest/"+KEY+"/distance.json/"+pick+"/"+dest+"/mile")
#         # jwks = json.loads(jsonurl.read())
#         return render_template('/api.html')
# return request.args.get("https://www.zipcodeapi.com/rest/<DemoOnly003gbBlwNX0SPKxGfooM3zaKTsPwHnJPkbHT0DLHL1GReEwIutZKseyU>/distance.<format>/<" + pick + ">/<" + dest + ">/<units>").data


# you can connect to your instance using the following command:
# mysql -uroot -p -h 34.174.50.222 --ssl-ca=server-ca.pem --ssl-cert=client-cert.pem --ssl-key=client-key.pem

# -----BEGIN RSA PRIVATE KEY-----
# MIIEpAIBAAKCAQEAyutIfQiHAF8t4QFJNkHkvRsJRWQQRXZ4VdAd+l7aJGoDy1in
# kJDfvqVZdRB+/3Ex7bNheglGJvSybYCE5lk252/r1NPdqTAy5CDFQLSOhFAcfVT7
# yRqGBYEEVEy5C18TzVHvLOmfyvxLsrLAY/86tfNhGGJbVFDcnkfTV7ViE45BDKnW
# LGlNtna0pEn3cbEykrugF01vb/zFi5yc85TKqZI9vpIAwRgcj7Y4I++rOJgNiNQT
# e7E0QngTenr5/ZOZu7EIYO+bBH6INSaDCJmm9oVX+UzYagClFZM4D01M6u8l+PlA
# OcqVUcVAoPTXDRbOb15LW0PHcRZCZtNbOxSj6wIDAQABAoIBAQC1pEHiMsTuL0UZ
# WhZYLEn+gXoeFIGAPJlhb4e2PDwXRpMY7sYoYZb3yHm4kcitDn28IsvJ+w1CB97E
# qLvOmuPL7mLzw6dzMMMNdMw9rKK6jB/EjVNJ5KU9vgzLDVbDeBt4urRXxtWUVZ3J
# W7teh/TdNPygYEMSycODKBZmN+aQSzmaHPIZ6uYWz+uP1YUJgOCLK3O9WLBZWeF1
# q9OcgCNi24NqTbAOECRfZ50mFNsr5H3C06N7QJ3eEkEtBTfzYRfFa6wwt1pA/chH
# vREVU7XM9kSkjK3W6ZctKQpC56YgYkLX1TRoYQjFkQKLzluNscXAGXCdjHhiFZ5l
# s2q5RWnZAoGBAOago6OCYj3z8bjklaZtGh/ZZGOoV7hUryWlM8Dx+I2wgztdNoGl
# ADHjeMCENi6U/8N0bAawTB0iq9mgkT5Qj8WvVNnKW3+mGoURak7VEpV6D+qYEbA8
# iuCtJstzOuV+gkdeQ2cfkH86mCbtRzbzsn0oEW0p+Bm1WW3T6mkq/Lk1AoGBAOE+
# RI4bfEAUvcxEkUIy0NlgEAdTzWHh2nLGvrKcOCxcLXIBjzAk66K+GL+JIQU1WJAB
# 8Q6//NJ2OLQgf95QERE69o5ahIqgKlyHaSG8irdCFHvTHFjba2GOhce9AW3ICU8y
# mpmFGQsRxTq0rqvOkuK26C8j7vQSBJPEKh3QtqyfAoGBAKF1Crq42ABZXPu9A8us
# i+KKNg7S1v6UQr4PJulIPWMslOMlgbhHhJhokKvuo2P/KgNy6QHRwKeRE1BbafN/
# QPf7pGKImYAHEH/iTlN8NfNxrdzls1R3Ph7G+ebq9+ucoqZGJtf2MBnyMnzmFrow
# 599ZAsIy5J9S55XNC0mvL5iVAoGAQnZnMC94CEiWgJGy8v+flKS91guqTLmiBcAT
# QQzLnntMhZlkMOaUCR9imhHShoDpMwT/pkSMS2XK8Yutb2Hcx2LIodSfy2/bUBY8
# tVG29MAw3yC5+pY0J0MwwnFI3KXr6UybRbV6YEPMGLh72gJIYVFrTY2i0q4GX7vA
# Wa/eVy0CgYAw7kU0x/VKh+vbT+nVKTMGgp4NpAPx6ljJ2pHk+Kb/rLiWnIcQAdAy
# igAI4wNmMjRzEwrI1tze0YgQg7Y3vc+5TpwqaYE3cbh61tRGJOnCxdke4fRxRgna
# ftt0nTmUO17KScZAG4WXWjbCt1V6nzSLNBwnCz8EXnPMuwzoAf3Jbw==
# -----END RSA PRIVATE KEY-----

# -----BEGIN CERTIFICATE-----
# MIIDeTCCAmGgAwIBAgIETf23FjANBgkqhkiG9w0BAQsFADCBhDEtMCsGA1UELhMk
# MjM1OTk0NDktODc0MC00OWU3LWJhYzktZGY3ZDU1OWI2ODQzMTAwLgYDVQQDEydH
# b29nbGUgQ2xvdWQgU1FMIENsaWVudCBDQSBteXNxbC1jbGllbnQxFDASBgNVBAoT
# C0dvb2dsZSwgSW5jMQswCQYDVQQGEwJVUzAeFw0yMjEwMDQxMzUxMTlaFw0zMjEw
# MDExMzUyMTlaMDoxFTATBgNVBAMTDG15c3FsLWNsaWVudDEUMBIGA1UEChMLR29v
# Z2xlLCBJbmMxCzAJBgNVBAYTAlVTMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
# CgKCAQEAyutIfQiHAF8t4QFJNkHkvRsJRWQQRXZ4VdAd+l7aJGoDy1inkJDfvqVZ
# dRB+/3Ex7bNheglGJvSybYCE5lk252/r1NPdqTAy5CDFQLSOhFAcfVT7yRqGBYEE
# VEy5C18TzVHvLOmfyvxLsrLAY/86tfNhGGJbVFDcnkfTV7ViE45BDKnWLGlNtna0
# pEn3cbEykrugF01vb/zFi5yc85TKqZI9vpIAwRgcj7Y4I++rOJgNiNQTe7E0QngT
# enr5/ZOZu7EIYO+bBH6INSaDCJmm9oVX+UzYagClFZM4D01M6u8l+PlAOcqVUcVA
# oPTXDRbOb15LW0PHcRZCZtNbOxSj6wIDAQABozwwOjAJBgNVHRMEAjAAMC0GA1Ud
# EQQmMCSBImRldmVsb3BtZW50QGdvbGRjb2FzdGxvZ2lzdGljcy5uZXQwDQYJKoZI
# hvcNAQELBQADggEBAHRGZH16qEUFItHfBBMvQB0bPsdoZi5HAJEkh1P1QMhkGunu
# 7kiJX1PWLahCZWHkumvtT8nODhbqraCEbuc5GRxFtKc1ks+WQaaYrPpjLWS9HbFy
# u8o0tecqvd/d7zStKqkCx1zs62g2B98plvWR0QUyftkrnCEv7ANTORFgB+ghYhbm
# tTMuPKaqaSYI1p5badhUU7HdJpAdNKJfVBlgg0uK+Syp+S9uLWS0VErgJXFD9Hrp
# zoOdQjak447BQZy03Bo0lTuTjO9ZQ5Qp259T64VllqlFwapdjJ97Bf5aBSgZcCzM
# N05ShQ0uBmu7aKXbxHg1MJzueSHg8L9iwz0GomM=
# -----END CERTIFICATE-----

# -----BEGIN CERTIFICATE-----
# MIIDfzCCAmegAwIBAgIBADANBgkqhkiG9w0BAQsFADB3MS0wKwYDVQQuEyRjN2U1
# MTJmOC1mZTYxLTQ5NTYtYjc1OS1kYTk1ZmI1YTBlZGIxIzAhBgNVBAMTGkdvb2ds
# ZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUsIEluYzELMAkG
# A1UEBhMCVVMwHhcNMjIxMDA0MTM0MjM4WhcNMzIxMDAxMTM0MzM4WjB3MS0wKwYD
# VQQuEyRjN2U1MTJmOC1mZTYxLTQ5NTYtYjc1OS1kYTk1ZmI1YTBlZGIxIzAhBgNV
# BAMTGkdvb2dsZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUs
# IEluYzELMAkGA1UEBhMCVVMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
# AQCfcVZiSfxAiRzRbCTnmMxrj2gTueEInRvWKyu7Gha6OskH0Zoj051ygWwng4JV
# rItTYYE1rP4vILoX0lZ3op/hbClnUlcEtm8l+k228UDDyGeztO18iImnlAZF7akF
# 9iaKN1jct6nlniFoXeXlZKUUi/Hqtt40QlP4dosyEIkZS2DUOgdMRjEXZhKfmcpg
# 3bLJEyoejf4EE0FhGl4l6CPFO1gd6KnCLb7sl5Wk3zplZxog2qpL/lvCFnqS2bb0
# Lwx0b0PVs2imbOBydf3whIcXTWOIlwq+Yqie29dJ+iDALsNXZQREWsNRmgoTfaNL
# SRR3iPVuFUcbtfqQm2saA2yDAgMBAAGjFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAw
# DQYJKoZIhvcNAQELBQADggEBAJQF1fVG7zosYL9GZUslTK9OSlXBOb+Azq/bji1Q
# HQ0Zj1IZ+IYRO2UX2Usop52dXERCJ6exrUJxx0JyaqPmM62ozHbb+N/nmOA9lJTY
# OHuLfAjbr4CRyiQ3pNbDluZsfCx1Xh4vd72APnRxWRTBI6WnV0ZhjA5hYP22GTFi
# Vngl5y4ZAVsUrH34fAh8Xk+kUev8pix9XsxgqkbKAZ1X4765750viF6kYrI4HP72
# UlGv+9q4yp7zswip5pJuCMW/2k7CRP9Iz9CsvfzWWjq5JX2mgR75DeC9SVP4oR40
# GXL8Z85O2vE7X32UaA0AQ+Buk8hKl9OjuYyKV5D6968uXzw=
# -----END CERTIFICATE-----

# Public IP - 34.174.50.222


if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8080,debug=True)