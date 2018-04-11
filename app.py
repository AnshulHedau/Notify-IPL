# Initial setup

from flask import Flask, request, redirect, url_for

import json
import pyrebase
import requests
import time
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Flask object creation
app = Flask(__name__)


# Index page
@app.route("/")

def index():
	return_value = {"message":"Welcome to the Edu-Buddy API!"}
	json_string = json.dumps(return_value)
	return json_string

# Score page
@app.route("/score")

def score():
	
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

	team = ["CSK","DD","KXIP","KKR","MI","RR","RCB","SRH"]
	team_name = ["Chennai Super Kings","Delhi Daredevils","Kings XI Punjab","Kolkata Knight Riders","Mumbai Indians","Rajasthan Royals","Royal Challengers Bangalore","Sunrisers Hyderabad"]
	team_playing = []
	team_playing.append(team_name[team.index(scores[0])])
	team_playing.append(team_name[team.index(scores[3])])

	courses = {"scores": {"details" : scores,"teams" : team_playing}}
	return json.dumps(courses)
	

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
