# Initial setup
from flask import Flask, request, redirect, url_for

import json
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
    return_value = {"message": "Welcome to the Notify-IPL API!"}
    json_string = json.dumps(return_value)
    return json_string


# Notification page
@app.route("/noti")
def noti():
    page = requests.get("http://www.cricbuzz.com/cricket-match/live-scores")
    soup = BeautifulSoup(page.content, 'html.parser')
    productrow = soup.find(class_="cb-schdl").contents[2]
    forecast_items = productrow.find(class_="cb-mtch-lst")

    period = forecast_items.find(class_="cb-lv-scrs-well")
    short_desc = period.find(class_="cb-lv-scrs-col").get_text()
    return (short_desc)


# Score page
@app.route("/score")
def score():
    status = 0
    team = ["CSK", "DD", "KXIP", "KKR", "MI", "RR", "RCB", "SRH","IND","AFG"]
    team_name = ["Chennai Super Kings", "Delhi Daredevils", "Kings XI Punjab", "Kolkata Knight Riders",
                 "Mumbai Indians", "Rajasthan Royals", "Royal Challengers Bangalore", "Sunrisers Hyderabad","India","Afganistan"]
    images = ["https://iplstatic.s3.amazonaws.com/players/284/1.png",
              "https://iplstatic.s3.amazonaws.com/players/210/1563.png",
              "https://iplstatic.s3.amazonaws.com/players/284/8.png",
              "https://iplstatic.s3.amazonaws.com/players/284/102.png",
              "https://iplstatic.s3.amazonaws.com/players/284/107.png",
              "https://iplstatic.s3.amazonaws.com/players/284/135.png",
              "https://iplstatic.s3.amazonaws.com/players/284/164.png",
              "https://iplstatic.s3.amazonaws.com/players/284/440.png",
             "https://upload.wikimedia.org/wikipedia/en/thumb/8/8d/Cricket_India_Crest.svg/1200px-Cricket_India_Crest.svg.png",
             "http://www.cricket.af/public/pictures/1500463538.png"]
    page = requests.get("http://www.cricbuzz.com/cricket-match/live-scores")
    soup = BeautifulSoup(page.content, 'html.parser')
    productrow = soup.find(class_="cb-schdl").contents[2]
    forecast_items = productrow.find(class_="cb-mtch-lst")
    internal_page = "http://www.cricbuzz.com" + forecast_items.find('a')['href']

    period = forecast_items.find(class_="cb-lv-scrs-well")
    if ('cb-lv-scrs-col' in str(period)):
        if('cb-text-complete' not in str(period)):
            page = requests.get(internal_page)
            soup = BeautifulSoup(page.content, 'html.parser')

        short_desc = period.find(class_="cb-lv-scrs-col").get_text()
        short_cap = period.find(class_="cb-scr-wll-chvrn").contents[3].get_text()
        # print(short_desc)
        # print(short_cap)

        team_playing = []
        team_image = []
        list_item = short_desc.split('\xa0•\xa0')
        list_name_score = list_item[0].split(' ')
        scores_team_1 = []
        scores_team_1.append(list_name_score[0])
        scores_team_1.append(list_name_score[1])
        scores_team_1.append(re.search('\(([^)]+)', str(list_item[0])).group(1))
        team_playing.append(team_name[team.index(scores_team_1[0])])
        team_image.append(images[team.index(scores_team_1[0])])

        scores_team_2 = []
        list_name_score = list_item[1].split(' ')
        if ('cb-text-complete' in str(period)):
            print("Anshul i am here")
            scores_team_2.append(list_name_score[1])
            scores_team_2.append(list_name_score[2])
            scores_team_2.append(re.search('\(([^)]+)', str(list_item[1])).group(1))
            team_playing.append(team_name[team.index(scores_team_2[0])])
            team_image.append(images[team.index(scores_team_2[0])])
            status = 101
            data = {
                "scores": {"teams": team_playing, "team1": scores_team_1, "team2": scores_team_2, "images": team_image,
                           "desc": short_cap, "status": status,"batsman":["0","0","0","0","0","0"],"bowler":["0","0","0","0","0","0"],"runs":["0","0","0","0","0","0"]}}
        else:
            runs = []
            batsman_data = []
            bowler_data = []
            print(len(list_name_score))
            if (len(list_name_score) > 4):
                scores_team_2.append(list_name_score[1])
                scores_team_2.append(list_name_score[2])
                scores_team_2.append(re.search('\(([^)]+)', str(list_item[1])).group(1))
                team_playing.append(team_name[team.index(scores_team_2[0])])
                team_image.append(images[team.index(scores_team_2[0])])
                status = 11
                temp = soup.find(class_="cb-min-lv").contents[3].contents[1].get_text()
                runs = temp.strip().split('|')
                ov_ln = len(runs)
                temp = soup.find(class_="cb-min-lv").contents[1].contents[0]
                for j in range(1, len(temp.contents)):
                    temp2 = temp.contents[j]
                    batsman_temp= []
                    temptext = len(temp2.contents)
                    for i in range(0, temptext):
                        batsman_temp.append(temp2.contents[i].get_text())
                    if (len(temp.contents) == 2):
                        batsman_data.append(batsman_temp)
                        batsman_temp = []
                        for i in range(0,6):
                            batsman_temp.append('-')
                        batsman_data.append(batsman_temp)
                    else:
                        batsman_data.append(batsman_temp)
                temp = soup.find(class_="cb-min-lv").contents[1].contents[1]
                for j in range(1, len(temp.contents)):
                    temp2 = temp.contents[j]
                    bowler_temp = []
                    temptext = len(temp2.contents)
                    for i in range(0, temptext):
                        bowler_temp.append(temp2.contents[i].get_text())
                    bowler_data.append(bowler_temp)
                data = {
                    "scores": {"teams": team_playing, "team1": scores_team_1, "team2": scores_team_2, "images": team_image,
                           "desc": short_cap, "status": status, "batsman": batsman_data, "bowler": bowler_data,
                           "recent": [runs[ov_ln-1]]}}

            else:
                scores_team_2.append(list_name_score[1])
                scores_team_2.append("0/0")
                scores_team_2.append("Yet to bat")
                team_playing.append(team_name[team.index(list_name_score[1])])
                team_image.append(images[team.index(scores_team_2[0])])
                status = 10
                temp = soup.find(class_="cb-min-lv").contents[3].contents[1].get_text()
                runs = temp.strip().split('|')
                ov_ln = len(runs)
                temp = soup.find(class_="cb-min-lv").contents[1].contents[0]
                for j in range(1, len(temp.contents)):
                    temp2 = temp.contents[j]
                    batsman_temp= []
                    temptext = len(temp2.contents)
                    for i in range(0, temptext):
                        batsman_temp.append(temp2.contents[i].get_text())
                    if (len(temp.contents) == 2):
                        batsman_data.append(batsman_temp)
                        batsman_temp = []
                        for i in range(0,6):
                            batsman_temp.append('-')
                        batsman_data.append(batsman_temp)
                    else:
                        batsman_data.append(batsman_temp)
                temp = soup.find(class_="cb-min-lv").contents[1].contents[1]
                for j in range(1, len(temp.contents)):
                    temp2 = temp.contents[j]
                    bowler_temp = []
                    temptext = len(temp2.contents)
                    for i in range(0, temptext):
                        bowler_temp.append(temp2.contents[i].get_text())
                    if (len(temp.contents) == 2):
                        bowler_data.append(bowler_temp)
                        bowler_temp = []
                        for i in range(0,6):
                            bowler_temp.append('-')
                        bowler_data.append(bowler_temp)
                    else:
                        bowler_data.append(bowler_temp)
                    
                data = {
                    "scores": {"teams": team_playing, "team1": scores_team_1, "team2": scores_team_2, "images": team_image,
                           "desc": short_cap, "status": status, "batsman": batsman_data, "bowler": bowler_data,
                           "recent": [runs[ov_ln-1]]}}



    else:
        teams_DATA = period.get('href')
        # short_cap = period.find(class_="cb-scr-wll-chvrn").contents[3].get_text()

        team_temp = teams_DATA.split('/')
        team_value = team_temp[3].split('-')
        team_init = []
        team_image = []
        team_init.append(team_value[0].upper())
        team_init.append(team_value[2].upper())
        print(team_init)
        team_playing = []
        team_playing.append(team_name[team.index(team_init[0].upper())])
        team_playing.append(team_name[team.index(team_init[1].upper())])

        scores_team_1 = []
        scores_team_1.append(team_value[0].upper())
        scores_team_1.append(" ")
        scores_team_1.append(" ")
        team_image.append(images[team.index(scores_team_1[0])])

        scores_team_2 = []
        scores_team_2.append(team_value[2].upper())
        scores_team_2.append(" ")
        scores_team_2.append(" ")
        team_image.append(images[team.index(scores_team_2[0])])
        data = {"scores": {"teams": team_playing, "team1": scores_team_1, "team2": scores_team_2, "images": team_image,
                           "initials": team_init, "status": status}}

    return (json.dumps(data))


# Help page
@app.route("/help")
def help():
    return_value = {"message": "The available commands for this API will be visible here :)"}

    json_string = json.dumps(return_value)

    return json_string


# Error page
@app.errorhandler(404)
def page_not_found(e):
    return json.dumps("error"), 404


if __name__ == "__main__":
    app.debug = True
    app.run()
