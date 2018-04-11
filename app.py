# Initial setup

from flask import Flask, request, redirect, url_for

import json
import pyrebase
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import requests
import time
import re
from datetime import datetime, timedelta
from autocorrect import spell
from bs4 import BeautifulSoup

# Flask object creation
app = Flask(__name__)

# Firebase configuration
config = {
    "apiKey": "AIzaSyDNio_QK2oYeytYQ_6H1I4yQYzgFEuSWPg",
    "authDomain": "edubuddy-b7f29.firebaseapp.com",
    "databaseURL": "https://edubuddy-b7f29.firebaseio.com",
    "storageBucket": "edubuddy-b7f29.appspot.com",
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()

# Index page
@app.route("/")

def index():
	return_value = {"message":"Welcome to the Edu-Buddy API!"}
	json_string = json.dumps(return_value)
	return json_string

# Courses Query page
@app.route("/courses",methods = ["GET"])

def courses():
	query_string = request.args.get('query')
	page = requests.get("https://www.coursera.org/courses?languages=en&query="+query_string)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	data = soup.find_all('h2',class_="color-primary-text headline-1-text flex-1",limit=10)
	list_data = []
	
	for i in range(10):
		list_data.append(str(data[i])[73:-5])
	list_url = []
 
	for link in soup.findAll('a', class_="rc-OfferingCard nostyle",limit=10):
		list_url.append('https://www.coursera.org' + link.get('href'))
		
	courses = {"courses": {"names" : list_data, "url" : list_url}}
	return json.dumps(courses)


# Score page
@app.route("/score")

def score():
	'''
        page = requests.get("http://www.cricbuzz.com/cricket-match/live-scores")
        soup = BeautifulSoup(page.content, 'html.parser')
        productrow = soup.find(class_="cb-lv-main")
        forecast_items = productrow.find(class_="cb-mtch-lst")

        period = forecast_items.find(class_="cb-lv-scrs-well")
        short_desc = period.find(class_="cb-lv-scrs-col").get_text()
        print(short_desc)
        list_item = short_desc.split('\xa0•\xa0')
        list_name_score = list_item[0].split(' ')
        scores = []
        scores.append(list_name_score[0])
        scores.append(list_name_score[1])
        scores.append(re.search('\(([^)]+)', list_item[0]).group(1))
        list_name_score = list_item[1].split(' ')
        scores.append(list_name_score[1])
        scores.append(list_name_score[2])
        scores.append(re.search('\(([^)]+)', list_item[1]).group(1))
        print(scores)
	json_string = json.dumps(scores)
	return json_string
	'''
	print("True")
        return "true"




# Help page
@app.route("/help")

def help():
	return_value = {"message":"The available commands for this API will be visible here :)"}

	json_string = json.dumps(return_value)

	return json_string

# Error page
@app.errorhandler(404)

def page_not_found(e):
	return json.dumps(data_repository["error"]), 404

if __name__ == "__main__":
	app.debug = True
	app.run()
