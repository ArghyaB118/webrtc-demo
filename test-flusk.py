#!/usr/bin/env python
from flask import Flask
import time
from flask_apscheduler import APScheduler
app = Flask(__name__)
global counter


@app.route("/")
#def hello():
#	global counter
#	time.sleep(1)
#	counter += 1
#	return str(counter)
	#for i in range(200):
	#	time.sleep(1)
	#	return str(i)
	#return "end"

#function executed by scheduled job
def my_job(text):
	counter = counter + 1
	num = int(text) 
	print(str(num+1))

if (__name__ == "__main__"):
	counter = 0
	scheduler = APScheduler()
	scheduler.add_job(func=my_job, args=[str(counter)], trigger='interval', id='job', seconds=1)
	scheduler.start()
	app.run(port = 8080)


