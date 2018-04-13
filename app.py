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

# Notification page
@app.route("/noti")

def noti():
	page = requests.get("http://www.cricbuzz.com/cricket-match/live-scores")
	soup = BeautifulSoup(page.content, 'html.parser')
	productrow = soup.find(class_="cb-lv-main")
	forecast_items = productrow.find(class_="cb-mtch-lst")

	period = forecast_items.find(class_="cb-lv-scrs-well")
	short_desc = period.find(class_="cb-lv-scrs-col").get_text()
	return(short_desc)


# Score page
@app.route("/score")

def score():
	
	team = ["CSK","DD","KXIP","KKR","MI","RR","RCB","SRH"]
	team_name = ["Chennai Super Kings","Delhi Daredevils","Kings XI Punjab","Kolkata Knight Riders","Mumbai Indians","Rajasthan Royals","Royal Challengers Bangalore","Sunrisers Hyderabad"]    

	page = requests.get("http://www.cricbuzz.com/cricket-match/live-scores")
	soup = BeautifulSoup(page.content, 'html.parser')
	productrow = soup.find(class_="cb-lv-main")
	forecast_items = productrow.find(class_="cb-mtch-lst")

	period = forecast_items.find(class_="cb-lv-scrs-well")
	if('cb-lv-scrs-col' in str(period)):
		short_desc = period.find(class_="cb-lv-scrs-col").get_text()
		#short_cap = period.find(class_="cb-text-complete").get_text() 
		#print(short_desc)
		#print(short_cap)
		
		team_playing = []
    
		list_item = short_desc.split('\xa0•\xa0')
		list_name_score = list_item[0].split(' ')
		scores_team_1 = []
		scores_team_1.append(list_name_score[0])
		scores_team_1.append(list_name_score[1])
		scores_team_1.append(re.search('\(([^)]+)', str(list_item[0])).group(1))
		team_playing.append(team_name[team.index(scores_team_1[0])])

		scores_team_2 = []
		list_name_score = list_item[1].split(' ')
		print(len(list_name_score))
		if(len(list_name_score)>6):
			scores_team_2.append(list_name_score[0])
			scores_team_2.append(list_name_score[1])
			scores_team_2.append(re.search('\(([^)]+)',str(list_item[1])).group(1))    
			team_playing.append(team_name[team.index(scores_team_2[0])])
		else:
			scores_team_2.append(" ")
			scores_team_2.append(" ")
			scores_team_2.append(" ")    
			team_playing.append(team_name[team.index(list_name_score[1])])
			
	
	
		data = {"scores": {"teams" : team_playing,"team1" : scores_team_1,"team2" : scores_team_2,"status" : 10}}

	else:
		teams_DATA = period.get('href')
		team_temp = teams_DATA.split('/')
		team_value = team_temp[3].split('-')
		team_init = []
		team_init.append(team_value[0].upper())
		team_init.append(team_value[2].upper())
		print(team_init)
		team_playing = []
		team_playing.append(team_name[team.index(team_init[0].upper())])
		team_playing.append(team_name[team.index(team_init[1].upper())])
		data = {"scores": {"teams" : team_playing,"initials" : team_init,"status" : 0}}

	return(json.dumps(data))
	

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
