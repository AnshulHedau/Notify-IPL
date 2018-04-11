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
	
	return_value  = "Valid"
        return return_value




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
