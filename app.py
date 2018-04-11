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
	return_value = {"message":"Scores here guys:)"}

	json_string = json.dumps(return_value)
	print("This is good maybe")
	return json_string

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
